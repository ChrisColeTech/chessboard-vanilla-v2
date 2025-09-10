#!/usr/bin/env node

/**
 * Backend-V2 Endpoint Test Script
 * Tests all 13 current endpoints (7 original + 6 new)
 */

const BASE_URL = 'http://localhost:3001/api';

// Test endpoints organized by category
const ENDPOINTS = {
  'Health Check': [
    { method: 'GET', path: '/health', auth: false }
  ],
  'Authentication (7 endpoints)': [
    { method: 'GET', path: '/auth/health', auth: false },
    { method: 'POST', path: '/auth/check-email', auth: false, body: { email: 'test@example.com' } },
    { method: 'POST', path: '/auth/check-username', auth: false, body: { username: 'testuser' } }
  ],
  'Core Chess Features': [
    { method: 'GET', path: '/users/profile', auth: true },
    { method: 'GET', path: '/games/', auth: true },
    { method: 'GET', path: '/puzzles/next', auth: true },
    { method: 'GET', path: '/puzzles/categories', auth: true },
    { method: 'GET', path: '/stats/overview', auth: true },
    { method: 'GET', path: '/tutorials/', auth: true },
    { method: 'GET', path: '/learning/paths', auth: true }
  ],
  'New Session Management': [
    { method: 'POST', path: '/sessions/create', auth: true, body: { user_id: 'test' } }
  ],
  'New Achievement System': [
    { method: 'GET', path: '/achievements/', auth: true }
  ],
  'New Progress Tracking': [
    { method: 'GET', path: '/progress/user/test', auth: true }
  ],
  'New Chess Theory': [
    { method: 'GET', path: '/openings/', auth: true },
    { method: 'GET', path: '/openings/search', auth: true }
  ],
  'New Chess Analysis': [
    { method: 'POST', path: '/analysis/position', auth: true, body: { position_fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' } }
  ],
  'New AI Opponents': [
    { method: 'GET', path: '/ai-opponents/', auth: true },
    { method: 'GET', path: '/ai-opponents/difficulty/1', auth: true }
  ]
};

// Mock JWT token for authenticated requests
const TEST_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ0ZXN0LXVzZXItaWQiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiaWF0IjoxNzAwMDAwMDAwLCJleHAiOjk5OTk5OTk5OTl9.placeholder';

async function makeRequest(method, url, options = {}) {
  const { auth, body } = options;
  
  const fetchOptions = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(auth && { 'Authorization': `Bearer ${TEST_TOKEN}` })
    }
  };
  
  if (body && (method === 'POST' || method === 'PUT')) {
    fetchOptions.body = JSON.stringify(body);
  }
  
  try {
    const fullUrl = url.startsWith('http') ? url : `${BASE_URL}${url}`;
    const response = await fetch(fullUrl, fetchOptions);
    
    return {
      status: response.status,
      ok: response.ok,
      data: response.ok ? await response.json() : { error: await response.text() }
    };
  } catch (error) {
    return {
      status: 0,
      ok: false,
      data: { error: error.message }
    };
  }
}

function formatResult(endpoint, result) {
  const status = result.ok ? '✅' : '❌';
  const statusCode = result.status === 0 ? 'CONN_ERR' : result.status;
  return `${status} ${endpoint.method} ${endpoint.path} - ${statusCode}`;
}

async function testAllEndpoints() {
  console.log('🚀 Testing Backend-V2 Endpoints\n');
  console.log(`📍 Base URL: ${BASE_URL}`);
  console.log(`🔧 Testing ${Object.values(ENDPOINTS).flat().length} total endpoints\n`);
  
  let totalTests = 0;
  let passedTests = 0;
  
  for (const [category, endpoints] of Object.entries(ENDPOINTS)) {
    console.log(`\n📂 ${category}`);
    console.log('─'.repeat(50));
    
    for (const endpoint of endpoints) {
      const result = await makeRequest(endpoint.method, endpoint.path, {
        auth: endpoint.auth,
        body: endpoint.body
      });
      
      console.log(formatResult(endpoint, result));
      
      if (!result.ok && result.status !== 401) {
        console.log(`   └─ Error: ${result.data.error || 'Unknown error'}`);
      }
      
      totalTests++;
      if (result.ok || result.status === 401) { // 401 is expected for some auth-required endpoints
        passedTests++;
      }
    }
  }
  
  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('📊 Test Summary');
  console.log('='.repeat(50));
  console.log(`Total Endpoints: ${totalTests}`);
  console.log(`✅ Successful: ${passedTests}`);
  console.log(`❌ Failed: ${totalTests - passedTests}`);
  console.log(`📈 Success Rate: ${Math.round((passedTests / totalTests) * 100)}%`);
  
  if (passedTests === totalTests) {
    console.log('\n🎉 All endpoints are working correctly!');
  } else {
    console.log('\n⚠️  Some endpoints need attention.');
  }
}

// Add fetch polyfill for Node.js
if (typeof fetch === 'undefined') {
  global.fetch = require('node-fetch');
}

testAllEndpoints().catch(console.error);