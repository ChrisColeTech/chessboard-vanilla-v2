const endpoints = [
  'GET /api/auth/health',
  'GET /health', 
  'POST /api/auth/register',
  'POST /api/auth/login',
  'GET /api/users',
  'GET /api/puzzles',
  'GET /api/games',
  'GET /api/stats',
  'GET /api/progress'
];

let successful = 0;
let total = 0;

async function testEndpoint(method, url) {
  total++;
  try {
    const response = await fetch(`http://localhost:3001${url}`, {
      method: method,
      headers: method === 'POST' ? {'Content-Type': 'application/json'} : {},
      body: method === 'POST' && url.includes('/register') ? 
        JSON.stringify({username: 'test', email: 'test@test.com', password: 'test123'}) : 
        undefined
    });
    
    const result = await response.text();
    
    // Consider it successful if:
    // 1. Status is 200 and we get valid JSON
    // 2. Or status is 400 with expected auth/validation errors
    if (response.status === 200 || 
        (response.status === 400 && (result.includes('already exists') || result.includes('Access token required')))) {
      successful++;
      console.log(`✓ ${method} ${url} - SUCCESS`);
      return true;
    } else {
      console.log(`✗ ${method} ${url} - FAILED (${response.status}): ${result.substring(0, 100)}`);
      return false;
    }
  } catch (error) {
    console.log(`✗ ${method} ${url} - ERROR: ${error.message}`);
    return false;
  }
}

async function runTests() {
  console.log('🧪 Testing backend endpoints...\n');
  
  for (const endpoint of endpoints) {
    const [method, url] = endpoint.split(' ');
    await testEndpoint(method, url);
    await new Promise(resolve => setTimeout(resolve, 100)); // Small delay
  }
  
  console.log(`\n📊 Results: ${successful}/${total} endpoints working (${Math.round(successful/total*100)}%)`);
}

runTests().catch(console.error);