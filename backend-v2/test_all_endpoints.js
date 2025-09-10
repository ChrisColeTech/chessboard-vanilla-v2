const http = require('http');

const BASE_URL = 'http://localhost:3001';
const endpoints = [
  // Auth endpoints - working correctly
  '/api/auth/health',
  
  // Users endpoints - require auth
  '/api/users/profile', 
  '/api/users/preferences',
  '/api/users/settings',
  
  // Games endpoints - require auth  
  '/api/games',
  '/api/games/reviews',
  
  // Puzzles endpoints - require auth
  '/api/puzzles/next',
  '/api/puzzles/categories', 
  '/api/puzzles/history',
  '/api/puzzles/custom',
  
  // Stats endpoints - require auth
  '/api/stats/overview',
  '/api/stats/puzzles',
  '/api/stats/games', 
  '/api/stats/progress',
  '/api/stats/performance',
  '/api/stats/ratings',
  
  // Tutorials endpoints - require auth
  '/api/tutorials/123',
  
  // Learning endpoints - require auth
  '/api/learning/paths',
  
  // Other new endpoints - require auth (using generic patterns for testing)
  '/api/sessions/validate/test-token',
  '/api/achievements/123',
  '/api/progress/123',
  '/api/openings/123', 
  '/api/analysis/123',
  '/api/ai-opponents/123',
  '/api/analytics/123',
  '/api/profiles/123',
  '/api/endgames/123',
  '/api/game-reviews/123',
  '/api/historic-games/123',
  '/api/puzzle-attempts/123',
  '/api/puzzle-sources/123',
  '/api/learning-modules/123',
  '/api/tutorial-steps/123',
  '/api/study-plans/123',
  '/api/help/123',
  '/api/subscriptions/123'
];

async function testEndpoint(endpoint) {
  return new Promise((resolve) => {
    const req = http.get(`${BASE_URL}${endpoint}`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const status = res.statusCode;
        let response;
        try { response = JSON.parse(data); } catch { response = data; }
        resolve({ endpoint, status, response });
      });
    });
    
    req.on('error', (err) => {
      resolve({ endpoint, status: 'ERROR', response: err.message });
    });
    
    req.setTimeout(2000, () => {
      req.destroy();
      resolve({ endpoint, status: 'TIMEOUT', response: 'Request timeout' });
    });
  });
}

async function testAllEndpoints() {
  console.log('🧪 Testing all 25 endpoints...\n');
  
  const results = [];
  for (const endpoint of endpoints) {
    const result = await testEndpoint(endpoint);
    results.push(result);
    
    // 200 OK and 401 Auth Required are both successful (routes exist)
    const isSuccess = result.status === 200 || result.status === 401;
    const statusColor = result.status === 200 ? '✅' : result.status === 401 ? '🔒' : '❌';
    
    console.log(`${statusColor} ${endpoint} -> ${result.status} ${result.response?.error || ''}`);
  }
  
  console.log('\n📊 Summary:');
  const passed = results.filter(r => r.status === 200 || r.status === 401).length;
  const failed = results.filter(r => r.status !== 200 && r.status !== 401).length;
  console.log(`✅ ${passed}/${endpoints.length} endpoints working (200 OK or 401 Auth Required)`);
  console.log(`❌ ${failed}/${endpoints.length} endpoints failed (404 or other errors)`);
  
  if (failed > 0) {
    console.log('\n❌ Failed endpoints:');
    results.filter(r => r.status !== 200 && r.status !== 401).forEach(r => {
      console.log(`   ${r.endpoint} -> ${r.status} ${r.response?.error || ''}`);
    });
  }
}

testAllEndpoints().catch(console.error);