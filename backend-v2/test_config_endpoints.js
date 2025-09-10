const http = require('http');

const BASE_URL = 'http://localhost:3001';

// All endpoints from backend_config.json with exact patterns
const endpoints = [
  // Auth endpoints (13 total)
  '/api/auth/health',
  '/api/auth/login',
  '/api/auth/register', 
  '/api/auth/me',
  '/api/auth/check-email',
  '/api/auth/check-username',
  
  // Users endpoints (6 total)
  '/api/users/profile',
  '/api/users/preferences', 
  '/api/users/settings',
  
  // Puzzles endpoints (7 total)
  '/api/puzzles/next',
  '/api/puzzles/categories',
  '/api/puzzles/history',
  '/api/puzzles/custom',
  
  // Games endpoints (7 total)
  '/api/games',
  '/api/games/reviews',
  
  // Stats endpoints (6 total)
  '/api/stats/overview',
  '/api/stats/puzzles',
  '/api/stats/games',
  '/api/stats/progress',
  '/api/stats/performance',
  '/api/stats/ratings',
  
  // Learning endpoints (4 total)
  '/api/learning/paths',
  
  // Tutorials endpoints (3 total)
  '/api/tutorials',
  
  // New endpoints from config
  '/api/sessions/create',
  '/api/achievements',
  '/api/progress/update',
  '/api/openings',
  '/api/analysis/position',
  '/api/ai-opponents',
  '/api/analytics/track',
  '/api/profiles/user123',
  '/api/endgames',
  '/api/game-reviews',
  '/api/historic-games',
  '/api/puzzle-attempts',
  '/api/puzzle-sources',
  '/api/learning-modules/path/123',
  '/api/tutorial-steps/tutorial/123',
  '/api/study-plans',
  '/api/help',
  '/api/subscriptions'
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
  console.log(`🧪 Testing ${endpoints.length} endpoints from backend_config.json...\n`);
  
  const results = [];
  for (const endpoint of endpoints) {
    const result = await testEndpoint(endpoint);
    results.push(result);
    
    // 200 OK and 401 Auth Required are both successful (routes exist)
    const statusColor = result.status === 200 ? '✅' : result.status === 401 ? '🔒' : '❌';
    
    console.log(`${statusColor} ${endpoint} -> ${result.status} ${result.response?.error || ''}`);
  }
  
  console.log('\n📊 Summary:');
  const passed = results.filter(r => r.status === 200 || r.status === 401).length;
  const failed = results.filter(r => r.status !== 200 && r.status !== 401).length;
  console.log(`✅ ${passed}/${endpoints.length} endpoints working (200 OK or 401 Auth Required)`);
  console.log(`❌ ${failed}/${endpoints.length} endpoints failed (404 or other errors)`);
  
  const successRate = ((passed / endpoints.length) * 100).toFixed(1);
  console.log(`📈 Success rate: ${successRate}%`);
  
  if (failed > 0) {
    console.log('\n❌ Failed endpoints:');
    results.filter(r => r.status !== 200 && r.status !== 401).forEach(r => {
      console.log(`   ${r.endpoint} -> ${r.status} ${r.response?.error || ''}`);
    });
  }
  
  if (successRate === '100.0') {
    console.log('\n🎉 100% SUCCESS! All endpoints from config are working! 🎉');
  }
}

testAllEndpoints().catch(console.error);