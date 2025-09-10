#!/usr/bin/env node
/**
 * Comprehensive API Connectivity Test Script (fixed)
 * - Authenticates, captures user id, and sends complete payloads
 * - Logs outgoing request bodies for POST/PUT/PATCH
 * - Defensive parsing of token/user shapes
 */

const fs = require('fs');
const path = require('path');

// ---- Optional fetch polyfill for Node < 18 ----
if (typeof fetch === 'undefined') {
  global.fetch = (...args) =>
    import('node-fetch').then(({ default: fetch }) => fetch(...args));
}

// --- Config (env overrides supported) ---
const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:5173';
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:3001';
const CONFIG_PATH =
  process.env.BACKEND_CONFIG_PATH ||
  path.join(__dirname, 'backend-tools', 'backend_config.json');

// Globals
let authToken = null;
let testUserId = null;

// Load backend configuration
let backendConfig;
try {
  const configData = fs.readFileSync(CONFIG_PATH, 'utf8');
  backendConfig = JSON.parse(configData);
} catch (error) {
  console.error('❌ Failed to load backend config:', error.message);
  process.exit(1);
}

// ---------- Helpers ----------
function snakeToCamelCase(str) {
  const components = String(str).split('_');
  return (
    components[0] +
    components
      .slice(1)
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join('')
  );
}

function normalizeEntityName(name) {
  if (!name) return '';
  const n = String(name).toLowerCase();
  // map common aliases to canonical keys used in generateTestData
  if (n.includes('session')) return 'user_sessions';
  if (n.includes('study') && n.includes('plan')) return 'user_study_plans';
  if (n.includes('game')) return 'games';
  if (n.includes('puzzle') && n.includes('attempt')) return 'puzzle_attempts';
  if (n.includes('subscription')) return 'subscriptions';
  if (n.includes('tutorial') && n.includes('step')) return 'tutorial_steps';
  if (n === 'auth' || n.includes('user')) return 'users';
  return n;
}

// ---------- Auth + user discovery ----------
async function authenticate() {
  console.log('🔐 Setting up authentication...');

  const testUser = {
    username: 'testuser3',
    email: 'test3@example.com',
    password: 'password123',
  };

  try {
    // Try register (ok if it already exists)
    await testEndpoint(
      'POST',
      `${BACKEND_URL}/api/auth/register`,
      testUser,
      false,
      true
    );

    // Try login
    const loginResult = await testEndpoint(
      'POST',
      `${BACKEND_URL}/api/auth/login`,
      { email: testUser.email, password: testUser.password },
      false,
      true
    );

    const payload = loginResult.data || {};
    const token =
      (payload.data && payload.data.token) ||
      payload.token ||
      (payload.access && payload.access.token) ||
      null;

    if (!token) {
      console.log('  ⚠️  No token returned by /api/auth/login response:', payload);
      return false;
    }

    authToken = token;
    console.log('  ✅ Authentication successful! Token acquired.');

    // Discover user id via /api/auth/me
    const me = await testEndpoint('GET', `${BACKEND_URL}/api/auth/me`, null, true, true);
    const meData = me.data || {};
    testUserId =
      (meData.data && meData.data.user && meData.data.user.id) ||
      (meData.user && meData.user.id) ||
      meData.id ||
      null;

    if (testUserId) {
      console.log(`  ℹ️  testUserId = ${testUserId}`);
    } else {
      console.log('  ⚠️  Could not determine user id from /api/auth/me. Some endpoints may still fail.');
    }

    return true;
  } catch (error) {
    console.log('  ⚠️  Authentication error:', error.message || error);
    return false;
  }
}

// ---------- HTTP ----------
async function testEndpoint(method, url, data = null, requireAuth = true, suppressLog = false) {
  try {
    const options = {
      method: method.toUpperCase(),
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
    };

    if (authToken && requireAuth) {
      options.headers['Authorization'] = `Bearer ${authToken}`;
    }

    if (data && ['POST', 'PUT', 'PATCH'].includes(options.method)) {
      options.body = JSON.stringify(data);
    }

    if (!suppressLog && options.body) {
      try {
        console.log('    ⤷ Request body:', JSON.stringify(JSON.parse(options.body), null, 2));
      } catch {
        console.log('    ⤷ Request body (raw):', options.body);
      }
    }

    const response = await fetch(url, options);
    const result = {
      status: response.status,
      ok: response.ok,
      statusText: response.statusText,
      url,
    };

    try {
      const text = await response.text();
      if (text) result.data = JSON.parse(text);
    } catch {
      // Non-JSON response
    }

    return result;
  } catch (error) {
    return { error: error.message, url, status: 'ERROR' };
  }
}

// ---------- Test data generation ----------
function generateTestData(entityNameRaw, apiEndpoint = {}) {
  const entityName = normalizeEntityName(entityNameRaw);
  const now = new Date().toISOString();

  const baseData = {
    id: 'test-id-' + Date.now(),
    createdAt: now,
    updatedAt: now,
  };

  const attachUser = (obj) => {
    if (testUserId) {
      obj.user_id = testUserId; // snake_case
      obj.userId = testUserId;  // camelCase
    }
    return obj;
  };

  switch (entityName) {
    case 'games':
      return attachUser({
        ...baseData,
        ai_level: 1,
        user_color: 'white',
        current_fen:
          'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        pgn: '',
        result: null,
      });

    case 'user_sessions': {
      const refreshToken = 'rt-' + Math.random().toString(36).slice(2);
      const expiresAt = new Date(Date.now() + 1000 * 60 * 60 * 24).toISOString();
      return attachUser({
        ...baseData,
        refresh_token: refreshToken, // snake
        refreshToken,                // camel
        expires_at: expiresAt,
        expiresAt,
      });
    }

    case 'subscriptions':
      return {
        ...baseData,
        tier: 'basic',
        name: 'Test Subscription',
        price: 0.0,
        currency: 'USD',
        is_active: true,
      };

    case 'user_study_plans':
      return attachUser({
        ...baseData,
        name: 'Default Study Plan',
        description: 'Created by connectivity test',
        target_rating: 1500,
        estimated_weeks: 4,
      });

    case 'puzzle_attempts':
      return attachUser({
        ...baseData,
        puzzle_id: 'test-puzzle-123',
        moves: 'e2e4 e7e5',
        correct: true,
        time_taken: 30,
        rating_change: 5,
      });

    case 'tutorials':
      return { ...baseData, title: 'Test Tutorial', content: 'Test content' };

    case 'achievements':
      return { ...baseData, name: 'Test Achievement', description: 'Test desc', points: 10 };

    case 'users':
      return { ...baseData, username: 'testuser', email: 'test@example.com' };

    default:
      // Fallback: include a name + description, and attach user if we have it
      return attachUser({ ...baseData, name: `Test ${entityNameRaw}`, description: 'Test item' });
  }
}

// ---------- URL building ----------
function buildEndpointUrl(endpointName, endpointConfig, apiEndpoint) {
  const entities = endpointConfig.entities || endpointConfig.entity || endpointName;
  const camelCaseEntities = snakeToCamelCase(entities);

  let basePath;
  if (String(endpointName).toLowerCase() === 'auth') {
    basePath = '/api/auth';
  } else {
    basePath = `/api/${camelCaseEntities}`;
  }

  let fullPath = basePath + apiEndpoint.path;

  // Path parameter substitutions
  fullPath = fullPath
    .replace(/:id/g, 'test-id-123')
    .replace(/:userId/g, testUserId || 'test-user-123')
    .replace(/:puzzleId/g, 'test-puzzle-123')
    .replace(/:gameId/g, 'test-game-123')
    .replace(/:fen/g, 'rnbqkbnr-pppppppp-8-8-8-8-PPPPPPPP-RNBQKBNR')
    .replace(/:level/g, 'beginner')
    .replace(/:category/g, 'endgame')
    .replace(/:player/g, 'kasparov')
    .replace(/:pathId/g, 'test-path-123')
    .replace(/:tutorialId/g, 'test-tutorial-123');

  return BACKEND_URL + fullPath;
}

// ---------- Main runner ----------
async function testAllEndpoints() {
  console.log('🚀 Starting API Connectivity Test');
  console.log('🌍 FRONTEND:', FRONTEND_URL);
  console.log('🔧 BACKEND :', BACKEND_URL);
  console.log('📄 CONFIG  :', CONFIG_PATH);

  // Authenticate first (required for protected endpoints)
  const authSuccess = await authenticate();
  if (!authSuccess) {
    console.log('❌ Authentication failed. Cannot test protected endpoints without valid token.');
    process.exit(1);
  }

  const results = { total: 0, successful: 0, failed: 0, errors: [] };

  for (const [endpointName, endpointConfig] of Object.entries(backendConfig.endpoints)) {
    console.log(`\n🔍 Testing ${endpointName} endpoints:`);

    const endpoints = endpointConfig.endpoints || [];
    const entityForData = endpointConfig.entity || endpointConfig.entities || endpointName;

    for (const apiEndpoint of endpoints) {
      results.total++;
      const url = buildEndpointUrl(endpointName, endpointConfig, apiEndpoint);
      const method = apiEndpoint.method;
      const handler = apiEndpoint.handler || '';

      // Decide if auth is required (default true unless explicitly false)
      const requireAuth = apiEndpoint.auth_required !== false;

      // Build request body for mutating verbs
      let testData = null;
      const isMutation = ['POST', 'PUT', 'PATCH'].includes(method.toUpperCase());

      if (isMutation) {
        const lowerPath = String(apiEndpoint.path).toLowerCase();

        // Special cases: endpoints that usually require a user id even if body is minimal
        const needsUserOnly =
          lowerPath.includes('/enroll') ||
          lowerPath.includes('/complete') ||
          lowerPath.includes('/unlock');

        if (needsUserOnly && testUserId) {
          testData = { user_id: testUserId, userId: testUserId };
        } else {
          testData = generateTestData(entityForData, apiEndpoint);
        }
      }

      console.log(`  ${method.padEnd(6)} ${url}`);
      const result = await testEndpoint(method, url, testData, requireAuth);

      if (result.error) {
        console.log(`    ❌ ERROR: ${result.error}`);
        results.failed++;
        results.errors.push({
          endpoint: `${method} ${url}`,
          error: result.error,
          handler,
        });
      } else if ([200, 201].includes(result.status)) {
        console.log(`    ✅ ${result.status} ${result.statusText}`);
        results.successful++;
      } else {
        console.log(`    ⚠️  ${result.status} ${result.statusText}`);
        if (result.data) {
          console.log('    ⤷ Response:', JSON.stringify(result.data, null, 2));
        }
        results.failed++;
        results.errors.push({
          endpoint: `${method} ${url}`,
          status: result.status,
          statusText: result.statusText,
          handler,
          body: isMutation ? testData : undefined,
          response: result.data,
        });
      }

      // small delay to avoid hammering the server
      await new Promise((r) => setTimeout(r, 100));
    }
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 API CONNECTIVITY TEST RESULTS');
  console.log('='.repeat(60));
  console.log(`Total Endpoints Tested: ${results.total}`);
  console.log(
    `✅ Successful: ${results.successful} (${(
      (results.successful / results.total) *
      100
    ).toFixed(1)}%)`
  );
  console.log(
    `❌ Failed: ${results.failed} (${(
      (results.failed / results.total) *
      100
    ).toFixed(1)}%)`
  );

  if (results.errors.length > 0) {
    console.log('\n🔍 ERROR DETAILS:');
    results.errors.forEach((e, i) => {
      console.log(`${i + 1}. ${e.endpoint}`);
      if (e.error) console.log(`   Error: ${e.error}`);
      if (e.status) console.log(`   Status: ${e.status} ${e.statusText}`);
      if (e.handler) console.log(`   Handler: ${e.handler}`);
      if (e.body) console.log(`   Sent Body: ${JSON.stringify(e.body)}`);
      if (e.response) console.log(`   Response: ${JSON.stringify(e.response)}`);
    });
  }

  // Frontend reachability
  console.log('\n🌐 Testing Frontend Access:');
  try {
    const frontendResult = await testEndpoint('GET', FRONTEND_URL, null, false);
    if (frontendResult.ok) {
      console.log(`  ✅ Frontend accessible at ${FRONTEND_URL}`);
    } else {
      console.log(
        `  ❌ Frontend not accessible: ${frontendResult.status} ${frontendResult.statusText}`
      );
    }
  } catch (error) {
    console.log(`  ❌ Frontend error: ${error.message}`);
  }

  const successRate = ((results.successful / results.total) * 100).toFixed(1);
  console.log(`\n🎯 Overall Success Rate: ${successRate}%`);
  if (parseFloat(successRate) >= 90) {
    console.log('🎊 Great! High connectivity achieved.');
    return true;
  } else {
    console.log('⚠️  Issues detected. Review the errors above.');
    return false;
  }
}

// Run
if (require.main === module) {
  testAllEndpoints()
    .then((ok) => process.exit(ok ? 0 : 1))
    .catch((err) => {
      console.error('Fatal error:', err);
      process.exit(1);
    });
}

module.exports = { testAllEndpoints };
