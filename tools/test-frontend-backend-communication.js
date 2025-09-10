#!/usr/bin/env node

/**
 * Frontend-to-Backend Communication Test Script
 * Tests all endpoints from frontend (5173) to backend (3001)
 * Verifies 100% successful communication
 */

const frontendUrl = 'http://localhost:5173';
const backendUrl = 'http://localhost:3001';

// Test configuration from backend_config.json
const testEndpoints = {
  auth: [
    { method: 'GET', path: '/api/auth/health', description: 'Health check' },
    { method: 'POST', path: '/api/auth/login', description: 'Demo user login', body: { email: 'chessdemo@example.com', password: 'ChessDemo2024' } },
    { method: 'POST', path: '/api/auth/check-email', description: 'Check email availability', body: { email: 'newemail@example.com' } },
    { method: 'POST', path: '/api/auth/check-username', description: 'Check username availability', body: { username: 'newuser' } },
  ],
  users: [
    { method: 'GET', path: '/api/users/profile', description: 'Get user profile', requiresAuth: true },
    { method: 'GET', path: '/api/users/preferences', description: 'Get user preferences', requiresAuth: true },
    { method: 'GET', path: '/api/users/settings', description: 'Get user settings', requiresAuth: true },
  ],
  puzzles: [
    { method: 'GET', path: '/api/puzzles/next', description: 'Get next puzzle', requiresAuth: true },
    { method: 'GET', path: '/api/puzzles/categories', description: 'Get puzzle categories', requiresAuth: true },
    { method: 'GET', path: '/api/puzzles/history', description: 'Get puzzle history', requiresAuth: true },
    { method: 'GET', path: '/api/puzzles/custom', description: 'Get custom puzzles', requiresAuth: true },
  ],
  games: [
    { method: 'GET', path: '/api/games', description: 'Get games list', requiresAuth: true },
    { method: 'GET', path: '/api/games/reviews', description: 'Get game reviews', requiresAuth: true },
  ],
  stats: [
    { method: 'GET', path: '/api/stats/overview', description: 'Get overview stats', requiresAuth: true },
    { method: 'GET', path: '/api/stats/puzzles', description: 'Get puzzle stats', requiresAuth: true },
    { method: 'GET', path: '/api/stats/games', description: 'Get game stats', requiresAuth: true },
    { method: 'GET', path: '/api/stats/progress', description: 'Get progress stats', requiresAuth: true },
    { method: 'GET', path: '/api/stats/performance', description: 'Get performance stats', requiresAuth: true },
    { method: 'GET', path: '/api/stats/ratings', description: 'Get rating stats', requiresAuth: true },
  ],
  learning: [
    { method: 'GET', path: '/api/learning/paths', description: 'Get learning paths', requiresAuth: true },
  ],
  tutorials: [
    { method: 'GET', path: '/api/tutorials', description: 'Get tutorials list', requiresAuth: true },
  ]
};

class CommunicationTester {
  constructor() {
    this.results = {
      total: 0,
      passed: 0,
      failed: 0,
      errors: []
    };
    this.authToken = null;
  }

  async delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async makeRequest(method, url, options = {}) {
    try {
      const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers
      };

      if (this.authToken && options.requiresAuth) {
        headers['Authorization'] = `Bearer ${this.authToken}`;
        console.log(`   🔐 Using auth token for request`);
      }

      const fetchOptions = {
        method,
        headers,
        mode: 'cors',
        credentials: 'include'
      };

      if (options.body && (method === 'POST' || method === 'PUT')) {
        fetchOptions.body = JSON.stringify(options.body);
      }

      const response = await fetch(url, fetchOptions);
      
      return {
        status: response.status,
        ok: response.ok,
        statusText: response.statusText,
        data: response.ok ? await response.json().catch(() => null) : null,
        error: !response.ok ? await response.text().catch(() => response.statusText) : null
      };
    } catch (error) {
      return {
        status: 0,
        ok: false,
        statusText: 'Network Error',
        data: null,
        error: error.message
      };
    }
  }

  async testEndpoint(endpoint) {
    const url = `${backendUrl}${endpoint.path}`;
    console.log(`\n🧪 Testing: ${endpoint.method} ${endpoint.path}`);
    console.log(`   Description: ${endpoint.description}`);
    if (endpoint.requiresAuth) {
      console.log(`   🔐 Requires authentication: ${this.authToken ? 'Token available' : 'No token available'}`);
    }

    const result = await this.makeRequest(endpoint.method, url, {
      body: endpoint.body,
      requiresAuth: endpoint.requiresAuth,
      headers: endpoint.headers
    });

    this.results.total++;

    if (result.status === 200) {
      // Only status 200 is considered successful
      this.results.passed++;
      console.log(`   ✅ Status: ${result.status} ${result.statusText}`);
      if (result.data) {
        console.log(`   📋 Response type: ${typeof result.data}`);
      }
      
      // Extract token for auth tests
      if (endpoint.path.includes('/login') && result.data) {
        console.log(`   📋 Login response:`, JSON.stringify(result.data, null, 2));
        // Try different possible token locations in response
        const token = result.data.token || result.data.data?.token || result.data.accessToken || result.data.access_token;
        if (token) {
          this.authToken = token;
          console.log(`   🔑 Auth token obtained for future requests`);
        } else {
          console.log(`   ⚠️  No token found in login response`);
        }
      }
    } else {
      this.results.failed++;
      console.log(`   ❌ Status: ${result.status} ${result.statusText}`);
      console.log(`   Error: ${result.error || 'Non-200 status code'}`);
      this.results.errors.push({
        endpoint: `${endpoint.method} ${endpoint.path}`,
        error: result.error || `Status ${result.status}`,
        status: result.status
      });
    }

    // Small delay between requests
    await this.delay(100);
  }

  async testFrontendAccess() {
    console.log('\n🌐 Testing frontend accessibility...');
    try {
      // Just check if the port is responding, not expecting JSON
      const response = await fetch(frontendUrl, { method: 'HEAD' });
      if (response.status === 200 || response.status === 404) {
        console.log('   ✅ Frontend is accessible');
        return true;
      } else {
        console.log('   ❌ Frontend is not accessible');
        return false;
      }
    } catch (error) {
      console.log('   ❌ Frontend is not accessible');
      console.log(`   Error: ${error.message}`);
      return false;
    }
  }

  async testBackendAccess() {
    console.log('\n🌐 Testing backend accessibility...');
    const result = await this.makeRequest('GET', `${backendUrl}/api/auth/health`);
    
    if (result.ok || result.status === 200 || result.status === 404) {
      console.log('   ✅ Backend is accessible');
      return true;
    } else {
      console.log('   ❌ Backend is not accessible');
      console.log(`   Error: ${result.error}`);
      return false;
    }
  }

  async runAllTests() {
    console.log('🚀 Starting Frontend-to-Backend Communication Tests');
    console.log('================================================\n');
    
    // Test basic connectivity
    const frontendOk = await this.testFrontendAccess();
    const backendOk = await this.testBackendAccess();
    
    if (!frontendOk || !backendOk) {
      console.log('\n❌ Basic connectivity failed. Servers may not be running.');
      return false;
    }

    console.log('\n📡 Testing all API endpoints...');
    console.log('================================');

    // Test all endpoints by domain
    for (const [domain, endpoints] of Object.entries(testEndpoints)) {
      console.log(`\n📂 Testing ${domain.toUpperCase()} domain:`);
      for (const endpoint of endpoints) {
        await this.testEndpoint(endpoint);
      }
    }

    // Print final results
    this.printResults();
    return this.results.failed === 0;
  }

  printResults() {
    console.log('\n📊 TEST RESULTS');
    console.log('================');
    console.log(`Total endpoints tested: ${this.results.total}`);
    console.log(`✅ Successful: ${this.results.passed}`);
    console.log(`❌ Failed: ${this.results.failed}`);
    
    const successRate = ((this.results.passed / this.results.total) * 100).toFixed(1);
    console.log(`📈 Success rate: ${successRate}%`);

    if (this.results.failed > 0) {
      console.log('\n❌ Failed endpoints:');
      this.results.errors.forEach(error => {
        console.log(`   • ${error.endpoint}: ${error.error} (${error.status})`);
      });
    }

    if (successRate === '100.0') {
      console.log('\n🎉 100% SUCCESSFUL COMMUNICATION VERIFIED! 🎉');
    } else {
      console.log(`\n⚠️  Communication success rate: ${successRate}%`);
    }
  }
}

// Run the tests
async function main() {
  const tester = new CommunicationTester();
  const success = await tester.runAllTests();
  
  process.exit(success ? 0 : 1);
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = CommunicationTester;