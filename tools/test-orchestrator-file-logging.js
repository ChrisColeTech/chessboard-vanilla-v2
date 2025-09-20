#!/usr/bin/env node
/**
 * Test Orchestrator - Complete API Testing Workflow (File Logging Version)
 * 
 * This orchestrates the full testing process:
 * 1. Runs payload generator to create fresh test data
 * 2. Executes comprehensive API tests
 * 3. Provides unified results and reporting
 * 
 * This version writes all output to a log file instead of the console.
 * 
 * Usage:
 *   node test-orchestrator-file-logging.js [--production] [--local] [--log-file=path]
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
    this.logFile = this.parseLogFile();
    this.logStream = null;
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

  parseLogFile() {
    const args = process.argv.slice(2);
    const logFileArg = args.find(arg => arg.startsWith('--log-file='));
    if (logFileArg) {
      return logFileArg.split('=')[1];
    }
    
    // Default log file - simple, consistent name
    return path.join(__dirname, 'api_test_output.log');
  }

  initializeLogging() {
    // Create log file and stream
    this.logStream = fs.createWriteStream(this.logFile, { flags: 'w' });
    
    // Write initial header
    this.log('='.repeat(80));
    this.log('TEST ORCHESTRATOR LOG');
    this.log('='.repeat(80));
    this.log(`Started: ${new Date().toISOString()}`);
    this.log(`Log File: ${this.logFile}`);
    this.log(`Environment: ${this.config.description}`);
    this.log(`Backend URL: ${this.config.backend}`);
    this.log('='.repeat(80));
    this.log('');
  }

  log(message) {
    if (this.logStream) {
      this.logStream.write(message + '\n');
    }
  }

  async runPayloadGenerator() {
    this.log('🔧 Step 1: Generating fresh test payloads...');
    this.log('   📁 Payload Generator: ' + this.payloadGeneratorPath);
    
    try {
      const startTime = Date.now();
      
      // Run the Python payload generator
      const result = execSync('python3 payload_generator.py', {
        cwd: this.payloadGeneratorPath,
        encoding: 'utf8',
        timeout: 30000 // 30 second timeout
      });
      
      const duration = Date.now() - startTime;
      
      this.log('   ✅ Payload generation completed');
      this.log(`   ⏱️  Duration: ${duration}ms`);
      
      // Log the generator output
      if (result) {
        this.log('   📝 Generator Output:');
        result.split('\n').forEach(line => {
          if (line.trim()) this.log('     ' + line);
        });
      }
      
      // Verify the generated payloads file exists and is recent
      const payloadsFile = path.join(this.payloadGeneratorPath, 'generated_payloads.json');
      if (fs.existsSync(payloadsFile)) {
        const stats = fs.statSync(payloadsFile);
        const age = Date.now() - stats.mtime.getTime();
        this.log(`   📄 Generated payloads file: ${Math.round(age / 1000)}s old`);
        
        // Quick validation - check if file has content
        const content = fs.readFileSync(payloadsFile, 'utf8');
        const payloads = JSON.parse(content);
        const entityCount = Object.keys(payloads).length;
        this.log(`   📊 Generated payloads for ${entityCount} entity groups`);
        
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
      this.log('   ❌ Payload generation failed: ' + error.message);
      if (error.stdout) {
        this.log('   📝 Stdout: ' + error.stdout);
      }
      if (error.stderr) {
        this.log('   📝 Stderr: ' + error.stderr);
      }
      this.results.payloadGeneration = {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
      throw error;
    }
  }

  async runApiTests() {
    this.log(`\n🧪 Step 2: Running API tests against ${this.config.description}...`);
    this.log('   🌐 Backend URL: ' + this.config.backend);
    this.log('   📝 Test Script: ' + this.testScriptPath);
    
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
        // Log to file instead of console, preserving original formatting
        output.split('\n').forEach(line => {
          if (line.trim()) this.log(line);
        });
      });

      testProcess.stderr.on('data', (data) => {
        const output = data.toString();
        stderr += output;
        // Log stderr to file
        output.split('\n').forEach(line => {
          if (line.trim()) this.log('[STDERR] ' + line);
        });
      });

      testProcess.on('close', (code) => {
        const duration = Date.now() - startTime;
        
        this.log(`\n   ⏱️  Test Duration: ${Math.round(duration / 1000)}s`);
        this.log(`   🏁 Test Process Exit Code: ${code}`);
        
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
        this.log('   ❌ Failed to start test process: ' + error.message);
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
      const summaryMatch = output.match(/Total Endpoints Tested: (\d+)/);
      if (summaryMatch) {
        results.totalEndpoints = parseInt(summaryMatch[1]);
      }

      const successMatch = output.match(/✅ Successful: (\d+)/);
      if (successMatch) {
        results.successful = parseInt(successMatch[1]);
      }

      const failedMatch = output.match(/❌ Failed: (\d+)/);
      if (failedMatch) {
        results.failed = parseInt(failedMatch[1]);
      }

      const rateMatch = output.match(/Overall Success Rate: ([\d.]+)%/);
      if (rateMatch) {
        results.successRate = parseFloat(rateMatch[1]);
      }

      // Extract error details
      const errorSection = output.match(/🔍 ERROR DETAILS:([\s\S]*?)(?:\n🌐|$)/);
      if (errorSection) {
        const errorText = errorSection[1];
        const errorBlocks = errorText.split(/\n\d+\./);
        results.errors = errorBlocks.slice(1).map(block => {
          const lines = block.trim().split('\n');
          return {
            endpoint: lines[0]?.trim(),
            entity: lines.find(l => l.includes('Entity:'))?.replace('Entity:', '').trim(),
            status: lines.find(l => l.includes('Status:'))?.replace('Status:', '').trim()
          };
        }).filter(error => error.endpoint);
      }

    } catch (parseError) {
      this.log('   ⚠️  Could not parse test results: ' + parseError.message);
    }

    return results;
  }

  async cleanup() {
    // Clean up any temporary files or processes
    this.log('\n🧹 Cleaning up...');
    
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

    this.log('\n' + '='.repeat(80));
    this.log('📊 TEST ORCHESTRATOR SUMMARY REPORT');
    this.log('='.repeat(80));
    this.log(`Environment: ${this.config.description}`);
    this.log(`Backend URL: ${this.config.backend}`);
    this.log(`Total Duration: ${Math.round(totalDuration / 1000)}s`);
    this.log(`Timestamp: ${this.results.endTime.toISOString()}`);

    // Payload Generation Results
    this.log('\n🔧 Payload Generation:');
    if (this.results.payloadGeneration?.success) {
      this.log(`   ✅ Success (${this.results.payloadGeneration.entityCount} entity groups)`);
      this.log(`   ⏱️  Duration: ${this.results.payloadGeneration.duration}ms`);
    } else {
      this.log('   ❌ Failed');
      if (this.results.payloadGeneration?.error) {
        this.log(`   🔍 Error: ${this.results.payloadGeneration.error}`);
      }
    }

    // API Test Results
    this.log('\n🧪 API Tests:');
    if (this.results.apiTests?.success) {
      const r = this.results.apiTests.results;
      this.log(`   ✅ Success (${r.successRate}% pass rate)`);
      this.log(`   📊 ${r.successful}/${r.totalEndpoints} endpoints passed`);
      this.log(`   ⏱️  Duration: ${Math.round(this.results.apiTests.duration / 1000)}s`);
      
      if (r.errors.length > 0) {
        this.log(`   ⚠️  ${r.errors.length} endpoints had issues:`);
        r.errors.forEach((error, i) => {
          this.log(`     ${i + 1}. ${error.endpoint} (${error.status})`);
        });
      }
    } else {
      this.log('   ❌ Failed');
      if (this.results.apiTests?.error) {
        this.log(`   🔍 Error: ${this.results.apiTests.error}`);
      }
    }

    // Overall Assessment
    this.log('\n🎯 Overall Assessment:');
    const allSuccessful = this.results.payloadGeneration?.success && this.results.apiTests?.success;
    if (allSuccessful) {
      const successRate = this.results.apiTests.results.successRate;
      if (successRate >= 95) {
        this.log('   🎊 Excellent! All systems operational.');
      } else if (successRate >= 85) {
        this.log('   👍 Good! Minor issues detected.');
      } else {
        this.log('   ⚠️  Significant issues need attention.');
      }
    } else {
      this.log('   💥 Critical failure in test orchestration.');
    }

    this.log('='.repeat(80));
    
    return allSuccessful;
  }

  async run() {
    try {
      // Initialize logging first
      this.initializeLogging();
      
      this.log('🚀 Starting Test Orchestrator');
      this.log(`🎯 Target: ${this.config.description} (${this.config.backend})`);
      this.log('='.repeat(80));

      // Step 1: Generate fresh payloads
      await this.runPayloadGenerator();

      // Step 2: Run API tests
      await this.runApiTests();

      // Generate summary report
      const success = this.generateSummaryReport();

      this.log(`\n🏁 Orchestrator completed: ${success ? 'SUCCESS' : 'FAILURE'}`);
      
      // Close log stream and wait for it to finish
      if (this.logStream) {
        await new Promise((resolve) => {
          this.logStream.end(resolve);
        });
      }
      
      // Print final status to console
      console.log(`Test completed. Results written to: ${this.logFile}`);
      console.log(`Status: ${success ? 'SUCCESS' : 'FAILURE'}`);

      return success;

    } catch (error) {
      this.log('\n💥 Orchestrator Error: ' + error.message);
      this.generateSummaryReport();
      
      if (this.logStream) {
        await new Promise((resolve) => {
          this.logStream.end(resolve);
        });
      }
      
      console.log(`Test failed. Results written to: ${this.logFile}`);
      console.log(`Error: ${error.message}`);
      
      throw error;
    } finally {
      await this.cleanup();
    }
  }
}

// Usage instructions
function showUsage() {
  console.log(`
Test Orchestrator - Complete API Testing Workflow (File Logging Version)

Usage:
  node test-orchestrator-file-logging.js [options]

Options:
  --local, --dev              Test against local development server (default)
  --production, --prod        Test against production Render deployment
  --log-file=path             Specify custom log file path
  --help, -h                 Show this help message

Examples:
  node test-orchestrator-file-logging.js                           # Test local, auto log file
  node test-orchestrator-file-logging.js --production              # Test production, auto log file
  node test-orchestrator-file-logging.js --log-file=./tests.log    # Custom log file
  
Default log file: test-orchestrator-[timestamp].log

The orchestrator will:
1. Generate fresh test payloads with unique credentials
2. Run comprehensive API tests against the target environment  
3. Write detailed results and performance metrics to the log file
4. Print only final status to console
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
      process.exit(success ? 0 : 1);
    })
    .catch((error) => {
      console.error('Orchestrator failed:', error.message);
      process.exit(1);
    });
}

module.exports = { TestOrchestrator };