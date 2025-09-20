#!/usr/bin/env node
/**
 * Render API Connectivity Test Script - Comprehensive Backend Testing
 * 
 * This script tests the deployed Render API at https://chessboard-vanilla-v2.onrender.com
 * using the same comprehensive testing approach as the local v3 test.
 * 
 * Features:
 * - Uses generated payloads from payload_generator.py
 * - Enhanced error reporting and debugging for production environment
 * - Production-specific authentication handling
 * - Comprehensive endpoint testing against deployed backend
 * - Health check validation
 * - Performance monitoring for production responses
 */

const fs = require('fs');
const path = require('path');

// Optional fetch polyfill for Node < 18
if (typeof fetch === 'undefined') {
  global.fetch = (...args) =>
    import('node-fetch').then(({ default: fetch }) => fetch(...args));
}

// Configuration - Flexible Environment (can be local or production)
const RENDER_API_URL = process.env.BACKEND_URL || process.env.RENDER_API_URL || 'http://localhost:3001';
const PAYLOADS_PATH = path.join(__dirname, 'backend-tools', 'payload-generator', 'generated_payloads.json');

// Global state
let authToken = null;
let testUserId = null;
let generatedPayloads = null;
let performanceMetrics = {
  requests: [],
  averageResponseTime: 0,
  slowestEndpoint: null,
  fastestEndpoint: null
};

// Load generated payloads
function loadGeneratedPayloads() {
  try {
    if (!fs.existsSync(PAYLOADS_PATH)) {
      console.error(`❌ Generated payloads file not found: ${PAYLOADS_PATH}`);
      console.log('💡 Please run the payload generator first:');
      console.log('   cd tools/backend-tools/payload-generator');
      console.log('   python3 payload_generator.py');
      process.exit(1);
    }
    
    const payloadsData = fs.readFileSync(PAYLOADS_PATH, 'utf8');
    return JSON.parse(payloadsData);
  } catch (error) {
    console.error('❌ Failed to load generated payloads:', error.message);
    process.exit(1);
  }
}

// Enhanced HTTP request handler with performance tracking
async function makeRequest(method, url, data = null, requireAuth = true) {
  const startTime = Date.now();
  
  try {
    const options = {
      method: method.toUpperCase(),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'ChessBoard-Test-Client/1.0'
      },
    };

    if (authToken && requireAuth) {
      options.headers['Authorization'] = `Bearer ${authToken}`;
    }

    if (data && ['POST', 'PUT', 'PATCH'].includes(options.method)) {
      options.body = JSON.stringify(data);
    }

    // Log request details for debugging
    if (options.body) {
      try {
        const parsedBody = JSON.parse(options.body);
        console.log('    ⤷ Request body:', JSON.stringify(parsedBody, null, 2));
      } catch {
        console.log('    ⤷ Request body (raw):', options.body);
      }
    }

    const response = await fetch(url, options);
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    // Track performance metrics
    performanceMetrics.requests.push({
      url,
      method,
      responseTime,
      status: response.status
    });

    const result = {
      status: response.status,
      ok: response.ok,
      statusText: response.statusText,
      url,
      responseTime,
      headers: Object.fromEntries(response.headers.entries()),
    };

    // Parse response
    try {
      const text = await response.text();
      if (text) {
        result.data = JSON.parse(text);
      }
    } catch (parseError) {
      // Handle non-JSON responses
      result.rawText = await response.text();
    }

    return result;
  } catch (error) {
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    return { 
      error: error.message, 
      url, 
      responseTime,
      status: 'NETWORK_ERROR',
      code: error.code || 'UNKNOWN'
    };
  }
}

// Build full URL for endpoint
function buildEndpointUrl(entityName, endpoint) {
  let basePath;
  
  if (entityName === 'auth') {
    basePath = '/api/auth';
  } else {
    // Convert underscores to kebab-case for URL paths (backend uses kebab-case routes)
    const kebabCaseEntity = entityName.replace(/_/g, '-');
    basePath = `/api/${kebabCaseEntity}`;
  }

  let fullPath = basePath + endpoint.path;

  // Substitute URL parameters with test values
  if (endpoint.url_params) {
    for (const [param, value] of Object.entries(endpoint.url_params)) {
      fullPath = fullPath.replace(`:${param}`, encodeURIComponent(value));
    }
  }

  // Fallback substitutions for any remaining parameters
  fullPath = fullPath
    .replace(/:id/g, 'test-render-id-123')
    .replace(/:userId/g, testUserId || 'test-render-user-123')
    .replace(/:puzzleId/g, 'test-render-puzzle-123')
    .replace(/:gameId/g, 'test-render-game-123')
    .replace(/:fen/g, 'rnbqkbnr-pppppppp-8-8-8-8-PPPPPPPP-RNBQKBNR')
    .replace(/:level/g, 'beginner')
    .replace(/:category/g, 'endgame')
    .replace(/:player/g, 'kasparov')
    .replace(/:pathId/g, 'test-render-path-123')
    .replace(/:tutorialId/g, 'test-render-tutorial-123')
    .replace(/:token/g, 'test-render-token-123')
    .replace(/:code/g, 'A00');

  return RENDER_API_URL + fullPath;
}

// Generate fresh credentials for auth endpoints
function generateFreshAuthCredentials() {
  const timestamp = Date.now();
  const randomStr = Math.random().toString(36).substring(2, 8);
  const username = `rendertest_${timestamp.toString().slice(-6)}_${randomStr}`;
  const email = `${username}@example.com`;
  
  console.log(`  🆕 Generated fresh Render credentials: ${username}`);
  
  // Update auth endpoints with fresh credentials
  for (const entityName in generatedPayloads) {
    if (entityName === 'auth') {
      const endpoints = generatedPayloads[entityName];
      for (const endpoint of endpoints) {
        if (endpoint.path === '/register' && endpoint.payload) {
          endpoint.payload.username = username;
          endpoint.payload.email = email;
          endpoint.payload.password = 'password123';
          console.log(`  🔄 Updated register payload with: ${username}`);
        }
        else if (endpoint.path === '/login' && endpoint.payload) {
          endpoint.payload.email = email;
          endpoint.payload.password = 'password123';
          console.log(`  🔄 Updated login payload with: ${email}`);
        }
        else if (endpoint.handler === 'forgotPassword' && endpoint.payload) {
          const forgotEmail = `forgot_${username}@example.com`;
          endpoint.payload.email = forgotEmail;
        }
        else if (endpoint.handler === 'checkEmailAvailability' && endpoint.payload) {
          const checkEmail = `check_${username}@example.com`;
          endpoint.payload.email = checkEmail;
        }
        else if (endpoint.handler === 'checkUsernameAvailability' && endpoint.payload) {
          const checkUsername = `check_${username}`;
          endpoint.payload.username = checkUsername;
        }
        else if (endpoint.handler === 'logout' && endpoint.payload) {
          const logoutUsername = `logout_${username}`;
          const logoutEmail = `${logoutUsername}@example.com`;
          endpoint.payload.username = logoutUsername;
          endpoint.payload.email = logoutEmail;
        }
        else if (endpoint.handler === 'resetPassword' && endpoint.payload) {
          endpoint.payload.email = email;
          endpoint.payload.currentPassword = 'password123';
          endpoint.payload.newPassword = 'newpassword123';
          console.log(`  🔄 Updated reset-password payload with: ${email}`);
        }
      }
    }
  }
}

// Enhanced authentication for production environment
async function authenticate() {
  console.log('🔐 Setting up authentication for Render production environment...');

  // Generate a unique test user for production testing
  const timestamp = Date.now();
  const testUser = {
    username: `rendertest_${timestamp}`,
    email: `rendertest_${timestamp}@example.com`,
    password: 'password123',
  };

  try {
    // Register the test user
    console.log('  📝 Registering test user on Render...');
    const registerResult = await makeRequest(
      'POST',
      `${RENDER_API_URL}/api/auth/register`,
      testUser,
      false
    );

    if (registerResult.error) {
      console.log('  ❌ Registration failed:', registerResult.error);
      console.log(`  📊 Response time: ${registerResult.responseTime}ms`);
      return false;
    }

    console.log('  ✅ User registered successfully');
    console.log(`  📊 Registration response time: ${registerResult.responseTime}ms`);

    // Login with the same user
    console.log('  🔑 Logging in to Render API...');
    const loginResult = await makeRequest(
      'POST',
      `${RENDER_API_URL}/api/auth/login`,
      { email: testUser.email, password: testUser.password },
      false
    );

    if (loginResult.error) {
      console.log('  ❌ Login failed with error:', loginResult.error);
      console.log(`  📊 Response time: ${loginResult.responseTime}ms`);
      return false;
    }

    // Extract token from various possible response structures
    const payload = loginResult.data || {};
    const token = payload.token || 
                 (payload.data && payload.data.token) ||
                 (payload.access && payload.access.token) ||
                 (payload.auth && payload.auth.token);

    if (!token) {
      console.log('  ⚠️  No token found in login response:', JSON.stringify(payload, null, 2));
      return false;
    }

    authToken = token;
    console.log('  ✅ Authentication successful! Token acquired.');
    console.log(`  📊 Login response time: ${loginResult.responseTime}ms`);

    // Get user information
    console.log('  👤 Fetching user information from Render...');
    const meResult = await makeRequest('GET', `${RENDER_API_URL}/api/auth/me`, null, true);
    
    if (meResult.data) {
      const userData = meResult.data;
      console.log(`  📋 User data received:`, JSON.stringify(userData, null, 2));
      
      testUserId = userData.id || 
                  (userData.data && userData.data.id) ||
                  (userData.user && userData.user.id) ||
                  userData.user_id;

      if (testUserId) {
        console.log(`  ℹ️  Test user ID: ${testUserId}`);
        console.log(`  📊 User info response time: ${meResult.responseTime}ms`);
        
        // Update payloads with the actual user ID
        console.log(`  🔄 Updating payloads with userId: ${testUserId}`);
        updatePayloadsWithUserId(testUserId);
      } else {
        console.log(`  ⚠️  Could not extract user ID from response`);
      }
    } else {
      console.log(`  ⚠️  No user data in /me response`);
    }

    // Force JWT token update regardless of user ID extraction
    console.log(`  🔄 Forcing JWT token update in verify-token payload`);
    forceUpdateJWTToken();

    // Generate fresh credentials for auth endpoints
    console.log(`  🔄 Generating fresh credentials for auth endpoints`);
    generateFreshAuthCredentials();

    return true;
  } catch (error) {
    console.log('  ❌ Authentication error:', error.message);
    return false;
  }
}

// Update generated payloads with actual user ID and JWT token
function updatePayloadsWithUserId(userId) {
  console.log(`  🔍 Starting payload update for userId: ${userId}, authToken: ${authToken ? authToken.substring(0, 20) + '...' : 'null'}`);
  
  for (const entityName in generatedPayloads) {
    const endpoints = generatedPayloads[entityName];
    for (const endpoint of endpoints) {
      if (endpoint.payload) {
        if (endpoint.payload.user_id) endpoint.payload.user_id = userId;
        if (endpoint.payload.userId) endpoint.payload.userId = userId;
        
        // Update verify-token endpoint with real JWT token
        if (entityName === 'auth' && endpoint.path === '/verify-token') {
          console.log(`  🔍 Found auth verify-token endpoint, current token: ${endpoint.payload.token}`);
          if (endpoint.payload.token && authToken) {
            console.log(`  🔄 Updating verify-token with real JWT: ${authToken.substring(0, 20)}...`);
            endpoint.payload.token = authToken;
          }
        }
      }
      
      // Update URL parameters
      if (endpoint.url_params && endpoint.url_params.userId) {
        endpoint.url_params.userId = userId;
      }
    }
  }
  
  // Force JWT token update in payloads regardless of whether userId was found
  console.log(`  🔄 Forcing JWT token update in verify-token payload`);
  for (const entityName in generatedPayloads) {
    const endpoints = generatedPayloads[entityName];
    for (const endpoint of endpoints) {
      if (entityName === 'auth' && endpoint.path === '/verify-token' && endpoint.payload && endpoint.payload.token) {
        console.log(`  🔄 Updated verify-token payload with real JWT: ${authToken.substring(0, 20)}...`);
        endpoint.payload.token = authToken;
      }
    }
  }
}

// Force JWT token update - standalone function
function forceUpdateJWTToken() {
  if (!authToken) {
    console.log(`  ⚠️  No authToken available for force update`);
    return;
  }
  
  for (const entityName in generatedPayloads) {
    const endpoints = generatedPayloads[entityName];
    for (const endpoint of endpoints) {
      if (entityName === 'auth' && endpoint.path === '/verify-token' && endpoint.payload) {
        console.log(`  🔧 Force updating verify-token from '${endpoint.payload.token}' to '${authToken.substring(0, 20)}...'`);
        endpoint.payload.token = authToken;
      }
    }
  }
}

// Test Render health endpoint
async function testRenderHealth() {
  console.log('🏥 Testing Render health endpoint...');
  try {
    const healthResult = await makeRequest('GET', `${RENDER_API_URL}/health`, null, false);
    
    if (healthResult.ok) {
      console.log('  ✅ Render health check passed');
      console.log(`  📊 Health check response time: ${healthResult.responseTime}ms`);
      if (healthResult.data) {
        console.log('  📋 Health data:', JSON.stringify(healthResult.data, null, 2));
      }
      return true;
    } else {
      console.log(`  ❌ Health check failed: ${healthResult.status} ${healthResult.statusText}`);
      console.log(`  📊 Response time: ${healthResult.responseTime}ms`);
      return false;
    }
  } catch (error) {
    console.log('  ❌ Health check error:', error.message);
    return false;
  }
}

// Calculate performance metrics
function calculatePerformanceMetrics() {
  if (performanceMetrics.requests.length === 0) return;

  const responseTimes = performanceMetrics.requests.map(r => r.responseTime);
  performanceMetrics.averageResponseTime = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length;
  
  const slowestRequest = performanceMetrics.requests.reduce((prev, current) => 
    (prev.responseTime > current.responseTime) ? prev : current
  );
  
  const fastestRequest = performanceMetrics.requests.reduce((prev, current) => 
    (prev.responseTime < current.responseTime) ? prev : current
  );
  
  performanceMetrics.slowestEndpoint = {
    endpoint: `${slowestRequest.method} ${slowestRequest.url}`,
    responseTime: slowestRequest.responseTime,
    status: slowestRequest.status
  };
  
  performanceMetrics.fastestEndpoint = {
    endpoint: `${fastestRequest.method} ${fastestRequest.url}`,
    responseTime: fastestRequest.responseTime,
    status: fastestRequest.status
  };
}

// Main testing function
async function testRenderAPI() {
  console.log('🚀 Starting Render API Connectivity Test');
  console.log('🌐 RENDER API:', RENDER_API_URL);
  console.log('📁 PAYLOADS  :', PAYLOADS_PATH);
  console.log('🎯 TARGET    : Production Render Environment');

  // Test health endpoint first
  const healthOk = await testRenderHealth();
  if (!healthOk) {
    console.log('⚠️  Health check failed, but continuing with API tests...');
  }

  // Load payloads
  console.log('\n📦 Loading generated payloads...');
  generatedPayloads = loadGeneratedPayloads();
  console.log(`  ✅ Loaded payloads for ${Object.keys(generatedPayloads).length} entity groups`);

  // Authenticate
  const authSuccess = await authenticate();
  if (!authSuccess) {
    console.log('❌ Authentication failed. Cannot test protected endpoints.');
    process.exit(1);
  }

  const results = { 
    total: 0, 
    successful: 0, 
    failed: 0, 
    errors: [],
    skipped: 0
  };

  // Test each entity group
  for (const [entityName, endpoints] of Object.entries(generatedPayloads)) {
    console.log(`\n🔍 Testing ${entityName} endpoints (${endpoints.length} endpoints) on Render:`);

    for (const endpoint of endpoints) {
      results.total++;
      
      const url = buildEndpointUrl(entityName, endpoint);
      const method = endpoint.method;
      const handler = endpoint.handler || '';
      const requireAuth = endpoint.auth_required !== false;

      console.log(`  ${method.padEnd(6)} ${url}`);

      // Make request with production-appropriate timeout
      const result = await makeRequest(method, url, endpoint.payload, requireAuth);

      // Show response time for all requests
      if (result.responseTime) {
        console.log(`    ⏱️  Response time: ${result.responseTime}ms`);
      }

      // Evaluate result - ONLY 200/201 are success, everything else is failure
      if (result.error) {
        console.log(`    ❌ ERROR: ${result.error}`);
        results.failed++;
        results.errors.push({
          endpoint: `${method} ${url}`,
          error: result.error,
          handler,
          entityName,
          payload: endpoint.payload,
          responseTime: result.responseTime
        });
      } else if ([200, 201].includes(result.status)) {
        console.log(`    ✅ ${result.status} ${result.statusText}`);
        results.successful++;
      } else {
        // ALL other status codes are failures
        console.log(`    ❌ ${result.status} ${result.statusText}`);
        if (result.data) {
          const responseStr = JSON.stringify(result.data, null, 2);
          console.log(`    ⤷ Response: ${responseStr.substring(0, 200)}${responseStr.length > 200 ? '...' : ''}`);
        }
        results.failed++;
        results.errors.push({
          endpoint: `${method} ${url}`,
          status: result.status,
          statusText: result.statusText,
          handler,
          entityName,
          payload: endpoint.payload,
          response: result.data,
          responseTime: result.responseTime
        });
      }

      // Longer delay for production to be respectful
      await new Promise(resolve => setTimeout(resolve, 200));
    }
  }

  // Calculate performance metrics
  calculatePerformanceMetrics();

  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('📊 RENDER API CONNECTIVITY TEST RESULTS');
  console.log('='.repeat(70));
  console.log(`Target Environment: ${RENDER_API_URL}`);
  console.log(`Total Endpoints Tested: ${results.total}`);
  console.log(`✅ Successful: ${results.successful} (${((results.successful / results.total) * 100).toFixed(1)}%)`);
  console.log(`❌ Failed: ${results.failed} (${((results.failed / results.total) * 100).toFixed(1)}%)`);
  console.log(`⏭️  Skipped: ${results.skipped} (${((results.skipped / results.total) * 100).toFixed(1)}%)`);

  // Performance summary
  if (performanceMetrics.requests.length > 0) {
    console.log('\n📈 PERFORMANCE METRICS:');
    console.log(`Average Response Time: ${performanceMetrics.averageResponseTime.toFixed(0)}ms`);
    if (performanceMetrics.slowestEndpoint) {
      console.log(`Slowest Endpoint: ${performanceMetrics.slowestEndpoint.endpoint} (${performanceMetrics.slowestEndpoint.responseTime}ms)`);
    }
    if (performanceMetrics.fastestEndpoint) {
      console.log(`Fastest Endpoint: ${performanceMetrics.fastestEndpoint.endpoint} (${performanceMetrics.fastestEndpoint.responseTime}ms)`);
    }
    
    // Performance assessment
    const avgTime = performanceMetrics.averageResponseTime;
    if (avgTime < 500) {
      console.log('🚀 Excellent response times! Production environment is performing well.');
    } else if (avgTime < 1000) {
      console.log('👍 Good response times for production environment.');
    } else if (avgTime < 2000) {
      console.log('⚠️  Moderate response times. Consider optimization if possible.');
    } else {
      console.log('🐌 Slow response times detected. May need performance optimization.');
    }
  }

  // Error details
  if (results.errors.length > 0) {
    console.log('\n🔍 ERROR DETAILS:');
    results.errors.forEach((error, index) => {
      console.log(`\n${index + 1}. ${error.endpoint}`);
      console.log(`   Entity: ${error.entityName}`);
      if (error.handler) console.log(`   Handler: ${error.handler}`);
      if (error.error) console.log(`   Error: ${error.error}`);
      if (error.status) console.log(`   Status: ${error.status} ${error.statusText}`);
      if (error.responseTime) console.log(`   Response Time: ${error.responseTime}ms`);
      if (error.payload) {
        console.log(`   Payload: ${JSON.stringify(error.payload, null, 2)}`);
      }
      if (error.response) {
        const responseStr = JSON.stringify(error.response, null, 2);
        console.log(`   Response: ${responseStr.substring(0, 300)}${responseStr.length > 300 ? '...' : ''}`);
      }
    });
  }

  // Final assessment
  const successRate = ((results.successful / results.total) * 100).toFixed(1);
  console.log(`\n🎯 Overall Success Rate: ${successRate}%`);
  console.log(`🌐 Production Environment: ${RENDER_API_URL}`);
  
  if (parseFloat(successRate) >= 85) {
    console.log('🎊 Excellent! Render API is performing very well in production.');
    return true;
  } else if (parseFloat(successRate) >= 70) {
    console.log('👍 Good connectivity to Render API. Some endpoints may need attention.');
    return true;
  } else {
    console.log('⚠️  Connectivity issues detected with Render API. Review errors above.');
    return false;
  }
}

// Run the test
if (require.main === module) {
  testRenderAPI()
    .then((success) => process.exit(success ? 0 : 1))
    .catch((error) => {
      console.error('💥 Fatal error:', error);
      process.exit(1);
    });
}

module.exports = { testRenderAPI };