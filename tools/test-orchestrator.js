#!/usr/bin/env node
/**
 * Test Orchestrator - Complete API Testing Workflow
 * 
 * This orchestrates the full testing process:
 * 1. Runs payload generator to create fresh test data
 * 2. Executes comprehensive API tests
 * 3. Provides unified results and reporting
 * 
 * Usage:
 *   node test-orchestrator.js [--production] [--local]
 */

const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');

// Configuration
const CONFIG = {
  local: {
    backend: 'http://localhost:3001',
    description: 'Local Development'
  },
  production: {
    backend: 'https://chessboard-vanilla-v2.onrender.com', 
    description: 'Render Production'
  }
};

class TestOrchestrator {
  constructor() {
    this.environment = this.parseEnvironment();
    this.config = CONFIG[this.environment];
    this.payloadGeneratorPath = path.join(__dirname, 'backend-tools', 'payload-generator');
    this.testScriptPath = path.join(__dirname, 'test-render-api-connectivity.js');
    this.results = {
      payloadGeneration: null,
      apiTests: null,
      startTime: new Date(),
      endTime: null
    };
  }

  parseEnvironment() {
    const args = process.argv.slice(2);
    if (args.includes('--production') || args.includes('--prod')) {
      return 'production';
    }
    return 'local'; // Default to local
  }

  async runPayloadGenerator() {
    console.log('🔧 Step 1: Generating fresh test payloads...');
    console.log('   📁 Payload Generator:', this.payloadGeneratorPath);
    
    try {
      const startTime = Date.now();
      
      // Run the Python payload generator
      const result = execSync('python3 payload_generator.py', {
        cwd: this.payloadGeneratorPath,
        encoding: 'utf8',
        timeout: 30000 // 30 second timeout
      });
      
      const duration = Date.now() - startTime;
      
      console.log('   ✅ Payload generation completed');
      console.log(`   ⏱️  Duration: ${duration}ms`);
      
      // Verify the generated payloads file exists and is recent
      const payloadsFile = path.join(this.payloadGeneratorPath, 'generated_payloads.json');
      if (fs.existsSync(payloadsFile)) {
        const stats = fs.statSync(payloadsFile);
        const age = Date.now() - stats.mtime.getTime();
        console.log(`   📄 Generated payloads file: ${Math.round(age / 1000)}s old`);
        
        // Quick validation - check if file has content
        const content = fs.readFileSync(payloadsFile, 'utf8');
        const payloads = JSON.parse(content);
        const entityCount = Object.keys(payloads).length;
        console.log(`   📊 Generated payloads for ${entityCount} entity groups`);
        
        this.results.payloadGeneration = {
          success: true,
          duration,
          entityCount,
          timestamp: new Date().toISOString()
        };
      } else {
        throw new Error('Generated payloads file not found');
      }
      
    } catch (error) {
      console.log('   ❌ Payload generation failed:', error.message);
      this.results.payloadGeneration = {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
      throw error;
    }
  }

  async runApiTests() {
    console.log(`\\n🧪 Step 2: Running API tests against ${this.config.description}...`);
    console.log('   🌐 Backend URL:', this.config.backend);
    console.log('   📝 Test Script:', this.testScriptPath);
    
    return new Promise((resolve, reject) => {
      const startTime = Date.now();
      
      // Set environment variable for backend URL
      const env = { 
        ...process.env, 
        BACKEND_URL: this.config.backend 
      };
      
      // Run the API test script
      const testProcess = spawn('node', [this.testScriptPath], {
        env,
        stdio: ['inherit', 'pipe', 'pipe']
      });

      let stdout = '';
      let stderr = '';

      testProcess.stdout.on('data', (data) => {
        const output = data.toString();
        stdout += output;
        // Real-time output
        process.stdout.write(output);
      });

      testProcess.stderr.on('data', (data) => {
        const output = data.toString();
        stderr += output;
        process.stderr.write(output);
      });

      testProcess.on('close', (code) => {
        const duration = Date.now() - startTime;
        
        console.log(`\\n   ⏱️  Test Duration: ${Math.round(duration / 1000)}s`);
        console.log(`   🏁 Test Process Exit Code: ${code}`);
        
        // Parse results from stdout
        const results = this.parseTestResults(stdout);
        
        this.results.apiTests = {
          success: code === 0,
          exitCode: code,
          duration,
          results,
          timestamp: new Date().toISOString()
        };

        if (code === 0) {
          resolve(results);
        } else {
          reject(new Error(`API tests failed with exit code ${code}`));
        }
      });

      testProcess.on('error', (error) => {
        console.log('   ❌ Failed to start test process:', error.message);
        this.results.apiTests = {
          success: false,
          error: error.message,
          timestamp: new Date().toISOString()
        };
        reject(error);
      });
    });
  }

  parseTestResults(output) {
    // Extract key metrics from test output
    const results = {
      totalEndpoints: 0,
      successful: 0,
      failed: 0,
      successRate: 0,
      errors: []
    };

    try {
      // Look for the results summary
      const summaryMatch = output.match(/Total Endpoints Tested: (\\d+)/);
      if (summaryMatch) {
        results.totalEndpoints = parseInt(summaryMatch[1]);
      }

      const successMatch = output.match(/✅ Successful: (\\d+)/);
      if (successMatch) {
        results.successful = parseInt(successMatch[1]);
      }

      const failedMatch = output.match(/❌ Failed: (\\d+)/);
      if (failedMatch) {
        results.failed = parseInt(failedMatch[1]);
      }

      const rateMatch = output.match(/Overall Success Rate: ([\\d.]+)%/);
      if (rateMatch) {
        results.successRate = parseFloat(rateMatch[1]);
      }

      // Extract error details
      const errorSection = output.match(/🔍 ERROR DETAILS:([\\s\\S]*?)(?:\\n🌐|$)/);
      if (errorSection) {
        const errorText = errorSection[1];
        const errorBlocks = errorText.split(/\\n\\d+\\./);
        results.errors = errorBlocks.slice(1).map(block => {
          const lines = block.trim().split('\\n');
          return {
            endpoint: lines[0]?.trim(),
            entity: lines.find(l => l.includes('Entity:'))?.replace('Entity:', '').trim(),
            status: lines.find(l => l.includes('Status:'))?.replace('Status:', '').trim()
          };
        }).filter(error => error.endpoint);
      }

    } catch (parseError) {
      console.log('   ⚠️  Could not parse test results:', parseError.message);
    }

    return results;
  }

  async cleanup() {
    // Clean up any temporary files or processes
    console.log('\\n🧹 Cleaning up...');
    
    // Kill local backend if we started it
    try {
      execSync('pkill -f "ts-node src/app.ts" || true', { stdio: 'ignore' });
    } catch (error) {
      // Ignore cleanup errors
    }
  }

  generateSummaryReport() {
    this.results.endTime = new Date();
    const totalDuration = this.results.endTime - this.results.startTime;

    console.log('\\n' + '='.repeat(80));
    console.log('📊 TEST ORCHESTRATOR SUMMARY REPORT');
    console.log('='.repeat(80));
    console.log(`Environment: ${this.config.description}`);
    console.log(`Backend URL: ${this.config.backend}`);
    console.log(`Total Duration: ${Math.round(totalDuration / 1000)}s`);
    console.log(`Timestamp: ${this.results.endTime.toISOString()}`);

    // Payload Generation Results
    console.log('\\n🔧 Payload Generation:');
    if (this.results.payloadGeneration?.success) {
      console.log(`   ✅ Success (${this.results.payloadGeneration.entityCount} entity groups)`);
      console.log(`   ⏱️  Duration: ${this.results.payloadGeneration.duration}ms`);
    } else {
      console.log('   ❌ Failed');
      if (this.results.payloadGeneration?.error) {
        console.log(`   🔍 Error: ${this.results.payloadGeneration.error}`);
      }
    }

    // API Test Results
    console.log('\\n🧪 API Tests:');
    if (this.results.apiTests?.success) {
      const r = this.results.apiTests.results;
      console.log(`   ✅ Success (${r.successRate}% pass rate)`);
      console.log(`   📊 ${r.successful}/${r.totalEndpoints} endpoints passed`);
      console.log(`   ⏱️  Duration: ${Math.round(this.results.apiTests.duration / 1000)}s`);
      
      if (r.errors.length > 0) {
        console.log(`   ⚠️  ${r.errors.length} endpoints had issues:`);
        r.errors.slice(0, 3).forEach((error, i) => {
          console.log(`     ${i + 1}. ${error.endpoint} (${error.status})`);
        });
        if (r.errors.length > 3) {
          console.log(`     ... and ${r.errors.length - 3} more`);
        }
      }
    } else {
      console.log('   ❌ Failed');
      if (this.results.apiTests?.error) {
        console.log(`   🔍 Error: ${this.results.apiTests.error}`);
      }
    }

    // Overall Assessment
    console.log('\\n🎯 Overall Assessment:');
    const allSuccessful = this.results.payloadGeneration?.success && this.results.apiTests?.success;
    if (allSuccessful) {
      const successRate = this.results.apiTests.results.successRate;
      if (successRate >= 95) {
        console.log('   🎊 Excellent! All systems operational.');
      } else if (successRate >= 85) {
        console.log('   👍 Good! Minor issues detected.');
      } else {
        console.log('   ⚠️  Significant issues need attention.');
      }
    } else {
      console.log('   💥 Critical failure in test orchestration.');
    }

    console.log('='.repeat(80));
    
    return allSuccessful;
  }

  async run() {
    try {
      console.log('🚀 Starting Test Orchestrator');
      console.log(`🎯 Target: ${this.config.description} (${this.config.backend})`);
      console.log('='.repeat(80));

      // Step 1: Generate fresh payloads
      await this.runPayloadGenerator();

      // Step 2: Run API tests
      await this.runApiTests();

      // Generate summary report
      const success = this.generateSummaryReport();

      return success;

    } catch (error) {
      console.log('\\n💥 Orchestrator Error:', error.message);
      this.generateSummaryReport();
      throw error;
    } finally {
      await this.cleanup();
    }
  }
}

// Usage instructions
function showUsage() {
  console.log(`
Test Orchestrator - Complete API Testing Workflow

Usage:
  node test-orchestrator.js [options]

Options:
  --local, --dev        Test against local development server (default)
  --production, --prod  Test against production Render deployment
  --help, -h           Show this help message

Examples:
  node test-orchestrator.js                    # Test local development
  node test-orchestrator.js --production       # Test production deployment
  node test-orchestrator.js --local            # Test local (explicit)

The orchestrator will:
1. Generate fresh test payloads with unique credentials
2. Run comprehensive API tests against the target environment  
3. Provide detailed results and performance metrics
`);
}

// Main execution
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    showUsage();
    process.exit(0);
  }

  const orchestrator = new TestOrchestrator();
  
  orchestrator.run()
    .then((success) => {
      console.log(`\\n🏁 Orchestrator completed: ${success ? 'SUCCESS' : 'FAILURE'}`);
      process.exit(success ? 0 : 1);
    })
    .catch((error) => {
      console.error('\\n💥 Orchestrator failed:', error.message);
      process.exit(1);
    });
}

module.exports = { TestOrchestrator };