#!/usr/bin/env node
/**
 * Render API Production Test Script
 * 
 * Tests the deployed Render backend at https://chessboard-vanilla-v2.onrender.com
 * Based on local test-api-connectivity-v3.js but optimized for production testing
 * 
 * Features:
 * - Tests core API endpoints on Render deployment
 * - Enhanced error reporting and debugging
 * - Authentication handling for production API
 * - Health checks and basic connectivity validation
 */

const fs = require('fs');
const path = require('path');

// Optional fetch polyfill for Node < 18
if (typeof fetch === 'undefined') {
  global.fetch = (...args) =>
    import('node-fetch').then(({ default: fetch }) => fetch(...args));
}

// Configuration - Render Production
const BACKEND_URL = 'https://chessboard-vanilla-v2.onrender.com';

// Global state
let authToken = null;
let testUserId = null;

// Enhanced HTTP request handler
async function makeRequest(method, url, data = null, requireAuth = true) {
  try {
    const options = {
      method: method.toUpperCase(),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
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
      console.log('    ⤷ Request body:', JSON.stringify(JSON.parse(options.body), null, 2));
    }

    const response = await fetch(url, options);
    const result = {
      status: response.status,
      ok: response.ok,
      statusText: response.statusText,
      url,
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
    return { 
      error: error.message, 
      url, 
      status: 'NETWORK_ERROR',
      code: error.code || 'UNKNOWN'
    };
  }
}

// Authentication for production API
async function authenticate() {
  console.log('🔐 Setting up authentication for Render API...');

  // Generate a unique test user to avoid conflicts
  const timestamp = Date.now();
  const testUser = {
    username: `render_test_${timestamp}`,
    email: `render_test_${timestamp}@example.com`,
    password: 'TestPassword123!',
  };

  try {
    // Register the test user
    console.log('  📝 Registering test user on Render...');
    const registerResult = await makeRequest(
      'POST',
      `${BACKEND_URL}/api/auth/register`,
      testUser,
      false
    );

    if (registerResult.error) {
      console.log('  ❌ Registration failed:', registerResult.error);
      return false;
    }

    if (registerResult.status !== 200 && registerResult.status !== 201) {
      console.log('  ❌ Registration failed:', registerResult.status, registerResult.statusText);
      if (registerResult.data) {
        console.log('    Response:', JSON.stringify(registerResult.data, null, 2));
      }
      return false;
    }

    console.log('  ✅ User registered successfully on Render');

    // Login with the same user
    console.log('  🔑 Logging in to Render API...');
    const loginResult = await makeRequest(
      'POST',
      `${BACKEND_URL}/api/auth/login`,
      { email: testUser.email, password: testUser.password },
      false
    );

    if (loginResult.error) {
      console.log('  ❌ Login failed with error:', loginResult.error);
      return false;
    }

    if (loginResult.status !== 200 && loginResult.status !== 201) {
      console.log('  ❌ Login failed:', loginResult.status, loginResult.statusText);
      if (loginResult.data) {
        console.log('    Response:', JSON.stringify(loginResult.data, null, 2));
      }
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
    console.log('  ✅ Authentication successful! Token acquired from Render API.');

    // Get user information
    console.log('  👤 Fetching user information...');
    const meResult = await makeRequest('GET', `${BACKEND_URL}/api/auth/me`, null, true);
    
    if (meResult.ok && meResult.data) {
      const userData = meResult.data;
      testUserId = userData.id || 
                  (userData.data && userData.data.id) ||
                  (userData.user && userData.user.id) ||
                  userData.user_id;

      if (testUserId) {
        console.log(`  ℹ️  Test user ID: ${testUserId}`);
      }
    }

    return true;
  } catch (error) {
    console.log('  ❌ Authentication error:', error.message);
    return false;
  }
}

// All API endpoints to test (based on app.ts route registration)
const allEndpoints = [
  // Health and basic endpoints
  { method: 'GET', path: '/health', auth: false, description: 'Health check' },
  
  // Auth endpoints - /api/auth
  { method: 'GET', path: '/api/auth/me', auth: true, description: 'Get current user' },
  
  // Users - /api/users
  { method: 'GET', path: '/api/users', auth: true, description: 'List users' },
  
  // Puzzles - /api/puzzles
  { method: 'GET', path: '/api/puzzles', auth: true, description: 'List puzzles' },
  {
    method: 'POST',
    path: '/api/puzzles',
    auth: true,
    description: 'Create puzzle',
    payload: {
      fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
      solution: 'e2e4',
      rating: 1200,
      theme: 'opening'
    }
  },
  
  // Games - /api/games
  { method: 'GET', path: '/api/games', auth: true, description: 'List games' },
  {
    method: 'POST',
    path: '/api/games',
    auth: true,
    description: 'Create game',
    payload: {
      opponent: 'AI',
      difficulty: 'beginner',
      timeControl: '10+0'
    }
  },
  
  // Stats - /api/stats
  { method: 'GET', path: '/api/stats', auth: true, description: 'Get stats' },
  
  // Learning Paths - /api/learning
  { method: 'GET', path: '/api/learning', auth: true, description: 'List learning paths' },
  
  // Tutorials - /api/tutorials
  { method: 'GET', path: '/api/tutorials', auth: true, description: 'List tutorials' },
  
  // Sessions - /api/sessions
  { method: 'GET', path: '/api/sessions', auth: true, description: 'List sessions' },
  
  // Achievements - /api/achievements
  { method: 'GET', path: '/api/achievements', auth: true, description: 'List achievements' },
  
  // Progress - /api/progress
  { method: 'GET', path: '/api/progress', auth: true, description: 'Get progress' },
  
  // Openings - /api/openings
  { method: 'GET', path: '/api/openings', auth: true, description: 'List openings' },
  
  // Analysis - /api/analysis
  { method: 'GET', path: '/api/analysis', auth: true, description: 'List analysis' },
  
  // AI Opponents - /api/aiOpponents
  { method: 'GET', path: '/api/aiOpponents', auth: true, description: 'List AI opponents' },
  
  // Analytics - /api/analytics
  { method: 'GET', path: '/api/analytics', auth: true, description: 'Get analytics' },
  
  // Profiles - /api/profiles
  { method: 'GET', path: '/api/profiles', auth: true, description: 'List profiles' },
  
  // Endgames - /api/endgames
  { method: 'GET', path: '/api/endgames', auth: true, description: 'List endgames' },
  
  // Game Reviews - /api/gameReviews
  { method: 'GET', path: '/api/gameReviews', auth: true, description: 'List game reviews' },
  
  // Historic Games - /api/historicGames
  { method: 'GET', path: '/api/historicGames', auth: true, description: 'List historic games' },
  
  // Puzzle Attempts - /api/puzzleAttempts
  { method: 'GET', path: '/api/puzzleAttempts', auth: true, description: 'List puzzle attempts' },
  
  // Puzzle Sources - /api/puzzleSources
  { method: 'GET', path: '/api/puzzleSources', auth: true, description: 'List puzzle sources' },
  
  // Learning Modules - /api/learningModules
  { method: 'GET', path: '/api/learningModules', auth: true, description: 'List learning modules' },
  
  // Tutorial Steps - /api/tutorialSteps
  { method: 'GET', path: '/api/tutorialSteps', auth: true, description: 'List tutorial steps' },
  
  // Study Plans - /api/studyPlans
  { method: 'GET', path: '/api/studyPlans', auth: true, description: 'List study plans' },
  
  // Help - /api/help
  { method: 'GET', path: '/api/help', auth: true, description: 'Get help' },
  
  // Subscriptions - /api/subscriptions
  { method: 'GET', path: '/api/subscriptions', auth: true, description: 'List subscriptions' }
];

// Main testing function
async function testRenderAPI() {
  console.log('🚀 Starting Render API Production Test');
  console.log('🌐 BACKEND:', BACKEND_URL);
  console.log('='.repeat(60));

  // Test basic connectivity first
  console.log('\n🔍 Testing basic connectivity...');
  const healthResult = await makeRequest('GET', `${BACKEND_URL}/health`, null, false);
  
  if (healthResult.error) {
    console.log('❌ Cannot connect to Render API:', healthResult.error);
    process.exit(1);
  }

  if (healthResult.ok && healthResult.data) {
    console.log('✅ Render API is responding!');
    console.log('  Health data:', JSON.stringify(healthResult.data, null, 2));
  } else {
    console.log('⚠️  Render API responding but with issues:', healthResult.status);
  }

  // Authenticate
  const authSuccess = await authenticate();
  if (!authSuccess) {
    console.log('❌ Authentication failed. Testing only public endpoints.');
  }

  const results = { 
    total: 0, 
    successful: 0, 
    failed: 0, 
    errors: []
  };

  // Test each endpoint
  console.log('\n🧪 Testing ALL API endpoints...');
  
  for (const endpoint of allEndpoints) {
    results.total++;
    
    const url = `${BACKEND_URL}${endpoint.path}`;
    const method = endpoint.method;
    const requireAuth = endpoint.auth !== false;

    // Skip auth-required endpoints if auth failed
    if (requireAuth && !authToken) {
      console.log(`  SKIP   ${method.padEnd(4)} ${endpoint.path} - No auth token`);
      continue;
    }

    console.log(`  ${method.padEnd(6)} ${endpoint.path} - ${endpoint.description}`);

    // Make request
    const result = await makeRequest(method, url, endpoint.payload, requireAuth);

    // Evaluate result
    if (result.error) {
      console.log(`    ❌ ERROR: ${result.error}`);
      results.failed++;
      results.errors.push({
        endpoint: `${method} ${endpoint.path}`,
        error: result.error,
        description: endpoint.description
      });
    } else if ([200, 201].includes(result.status)) {
      console.log(`    ✅ ${result.status} ${result.statusText}`);
      if (result.data) {
        // Show a sample of the response data
        const dataStr = JSON.stringify(result.data, null, 2);
        if (dataStr.length > 200) {
          console.log(`    ⤷ Response: ${dataStr.substring(0, 200)}...`);
        } else {
          console.log(`    ⤷ Response: ${dataStr}`);
        }
      }
      results.successful++;
    } else {
      console.log(`    ❌ ${result.status} ${result.statusText}`);
      if (result.data) {
        const responseStr = JSON.stringify(result.data, null, 2);
        console.log(`    ⤷ Response: ${responseStr.substring(0, 200)}${responseStr.length > 200 ? '...' : ''}`);
      }
      results.failed++;
      results.errors.push({
        endpoint: `${method} ${endpoint.path}`,
        status: result.status,
        statusText: result.statusText,
        description: endpoint.description,
        response: result.data
      });
    }

    // Small delay to avoid overwhelming the server
    await new Promise(resolve => setTimeout(resolve, 200));
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 RENDER API PRODUCTION TEST RESULTS');
  console.log('='.repeat(60));
  console.log(`Total Endpoints Tested: ${results.total}`);
  console.log(`✅ Successful: ${results.successful} (${((results.successful / results.total) * 100).toFixed(1)}%)`);
  console.log(`❌ Failed: ${results.failed} (${((results.failed / results.total) * 100).toFixed(1)}%)`);

  // Error details
  if (results.errors.length > 0) {
    console.log('\n🔍 ERROR DETAILS:');
    results.errors.forEach((error, index) => {
      console.log(`\n${index + 1}. ${error.endpoint} - ${error.description}`);
      if (error.error) console.log(`   Error: ${error.error}`);
      if (error.status) console.log(`   Status: ${error.status} ${error.statusText}`);
      if (error.response) {
        const responseStr = JSON.stringify(error.response, null, 2);
        console.log(`   Response: ${responseStr.substring(0, 300)}${responseStr.length > 300 ? '...' : ''}`);
      }
    });
  }

  // Final assessment
  const successRate = ((results.successful / results.total) * 100).toFixed(1);
  console.log(`\n🎯 Overall Success Rate: ${successRate}%`);
  console.log(`🌐 Render API URL: ${BACKEND_URL}`);
  
  if (parseFloat(successRate) >= 80) {
    console.log('🎊 Excellent! Render API is working well.');
    return true;
  } else if (parseFloat(successRate) >= 60) {
    console.log('👍 Good! Render API is mostly functional.');
    return true;
  } else {
    console.log('⚠️  Issues detected with Render API. Review errors above.');
    return false;
  }
}

// Run the test
if (require.main === module) {
  testRenderAPI()
    .then((success) => {
      console.log(`\n🏁 Test completed. Exit code: ${success ? 0 : 1}`);
      process.exit(success ? 0 : 1);
    })
    .catch((error) => {
      console.error('💥 Fatal error:', error);
      process.exit(1);
    });
}

module.exports = { testRenderAPI };