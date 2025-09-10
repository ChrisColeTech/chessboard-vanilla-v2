#!/usr/bin/env node
/**
 * Authentication Test Script
 * Gets auth tokens and tests authentication endpoints
 */

const http = require('http');
const crypto = require('crypto');

const BASE_URL = 'http://localhost:3001';

// Generate random test user data
const generateTestUser = () => ({
  username: `testuser_${crypto.randomBytes(4).toString('hex')}`,
  email: `test_${crypto.randomBytes(4).toString('hex')}@example.com`,
  password: 'TestPassword123!'
});

async function makeRequest(method, path, data = null, token = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const jsonBody = body ? JSON.parse(body) : {};
          resolve({
            status: res.statusCode,
            data: jsonBody,
            headers: res.headers
          });
        } catch (e) {
          resolve({
            status: res.statusCode,
            data: body,
            headers: res.headers
          });
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

async function testAuthFlow() {
  console.log('🔐 Testing Authentication Flow\n');
  
  const testUser = generateTestUser();
  let authToken = null;

  try {
    // 1. Test user registration
    console.log('1. Testing user registration...');
    const registerResponse = await makeRequest('POST', '/api/auth/register', testUser);
    
    if (registerResponse.status === 200 && registerResponse.data.success) {
      console.log('✅ Registration successful');
      authToken = registerResponse.data.data.token;
      console.log(`📝 Auth Token: ${authToken.substring(0, 20)}...`);
    } else {
      console.log('❌ Registration failed:', registerResponse.data);
      return null;
    }

    // 2. Test login
    console.log('\n2. Testing login...');
    const loginResponse = await makeRequest('POST', '/api/auth/login', {
      email: testUser.email,
      password: testUser.password
    });

    if (loginResponse.status === 200 && loginResponse.data.success) {
      console.log('✅ Login successful');
      authToken = loginResponse.data.data.token; // Update token
    } else {
      console.log('❌ Login failed:', loginResponse.data);
    }

    // 3. Test token verification
    console.log('\n3. Testing token verification...');
    const verifyResponse = await makeRequest('POST', '/api/auth/verify-token', {
      token: authToken
    });

    if (verifyResponse.status === 200 && verifyResponse.data.success) {
      console.log('✅ Token verification successful');
    } else {
      console.log('❌ Token verification failed:', verifyResponse.data);
    }

    // 4. Test protected route
    console.log('\n4. Testing protected route (/api/auth/me)...');
    const meResponse = await makeRequest('GET', '/api/auth/me', null, authToken);

    if (meResponse.status === 200 && meResponse.data.success) {
      console.log('✅ Protected route access successful');
      console.log(`👤 User: ${meResponse.data.data.user.username} (${meResponse.data.data.user.email})`);
    } else {
      console.log('❌ Protected route access failed:', meResponse.data);
    }

    return {
      token: authToken,
      user: registerResponse.data.data.user
    };

  } catch (error) {
    console.error('💥 Auth test failed:', error.message);
    return null;
  }
}

async function testAuthEndpoints() {
  console.log('🧪 Testing All Auth Endpoints\n');

  const authEndpoints = [
    { method: 'GET', path: '/api/auth/health', auth: false, description: 'Health check' },
    { method: 'POST', path: '/api/auth/check-email', auth: false, data: { email: 'test@example.com' }, description: 'Check email availability' },
    { method: 'POST', path: '/api/auth/check-username', auth: false, data: { username: 'testuser' }, description: 'Check username availability' },
    { method: 'POST', path: '/api/auth/forgot-password', auth: false, data: { email: 'test@example.com' }, description: 'Forgot password' },
  ];

  for (const endpoint of authEndpoints) {
    try {
      console.log(`Testing: ${endpoint.method} ${endpoint.path} - ${endpoint.description}`);
      const response = await makeRequest(endpoint.method, endpoint.path, endpoint.data);
      
      const status = response.status === 200 ? '✅' : response.status === 401 ? '🔒' : '❌';
      console.log(`${status} ${response.status} - ${endpoint.description}`);
      
      if (response.status !== 200 && response.status !== 401) {
        console.log(`   Error: ${JSON.stringify(response.data)}`);
      }
    } catch (error) {
      console.log(`❌ Error testing ${endpoint.path}: ${error.message}`);
    }
  }
}

async function main() {
  console.log('🚀 Authentication Test Suite\n');
  
  // Test full auth flow
  const authResult = await testAuthFlow();
  
  console.log('\n' + '='.repeat(60) + '\n');
  
  // Test individual auth endpoints
  await testAuthEndpoints();
  
  if (authResult) {
    console.log('\n' + '='.repeat(60));
    console.log('🎉 Authentication tests completed!');
    console.log(`📋 Test Results Summary:`);
    console.log(`   🔑 Auth Token: Available`);
    console.log(`   👤 Test User: ${authResult.user.username}`);
    console.log(`   📧 Email: ${authResult.user.email}`);
    
    // Export token for use in other scripts
    process.env.TEST_AUTH_TOKEN = authResult.token;
    process.env.TEST_USER_ID = authResult.user.id;
    
    return authResult;
  } else {
    console.log('\n❌ Authentication tests failed - no token available');
    process.exit(1);
  }
}

// Export for use by other scripts
module.exports = { makeRequest, testAuthFlow, main };

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}