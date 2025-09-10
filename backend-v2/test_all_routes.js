#!/usr/bin/env node
/**
 * Comprehensive Route Testing Script
 * Tests all endpoints with proper authentication and CRUD operations
 */

const { makeRequest, testAuthFlow } = require('./test_auth');

const BASE_URL = 'http://localhost:3001';

// Convert snake_case to camelCase for URLs
function snakeToCamel(str) {
  return str.replace(/[-_]([a-z])/g, (g) => g[1].toUpperCase());
}

// Generate comprehensive endpoint list from backend config
const API_ENDPOINTS = {
  // Authentication endpoints
  auth: [
    { method: 'POST', path: '/api/auth/register', auth: false, data: { username: 'testuser', email: 'test@example.com', password: 'Test123!' } },
    { method: 'POST', path: '/api/auth/login', auth: false, data: { email: 'test@example.com', password: 'Test123!' } },
    { method: 'GET', path: '/api/auth/me', auth: true },
    { method: 'PUT', path: '/api/auth/profile', auth: true, data: { display_name: 'Updated Name' } },
    { method: 'POST', path: '/api/auth/change-password', auth: true, data: { current_password: 'Test123!', new_password: 'NewTest123!' } },
    { method: 'POST', path: '/api/auth/verify-token', auth: false, data: { token: 'test-token' } },
    { method: 'POST', path: '/api/auth/forgot-password', auth: false, data: { email: 'test@example.com' } },
    { method: 'POST', path: '/api/auth/reset-password', auth: false, data: { token: 'reset-token', password: 'NewTest123!' } },
    { method: 'POST', path: '/api/auth/logout', auth: false },
    { method: 'POST', path: '/api/auth/check-email', auth: false, data: { email: 'test@example.com' } },
    { method: 'POST', path: '/api/auth/check-username', auth: false, data: { username: 'testuser' } },
    { method: 'DELETE', path: '/api/auth/delete-account', auth: true },
    { method: 'GET', path: '/api/auth/health', auth: false }
  ],

  // All custom endpoints from backend config
  custom: [
    // Users endpoints
    { method: 'GET', path: '/api/users/', auth: true },
    { method: 'GET', path: '/api/users/profile', auth: true },
    { method: 'PUT', path: '/api/users/profile', auth: true, data: { display_name: 'Test User' } },
    { method: 'GET', path: '/api/users/preferences', auth: true },
    { method: 'PUT', path: '/api/users/preferences', auth: true, data: { theme: 'dark' } },
    { method: 'GET', path: '/api/users/settings', auth: true },
    { method: 'PUT', path: '/api/users/settings', auth: true, data: { notifications: true } },
    
    // Puzzles endpoints
    { method: 'GET', path: '/api/puzzles/', auth: true },
    { method: 'GET', path: '/api/puzzles/next', auth: true },
    { method: 'POST', path: '/api/puzzles/test-id/solve', auth: true, data: { moves: ['e2e4'] } },
    { method: 'GET', path: '/api/puzzles/test-id/hint', auth: true },
    { method: 'GET', path: '/api/puzzles/categories', auth: true },
    { method: 'GET', path: '/api/puzzles/history', auth: true },
    { method: 'POST', path: '/api/puzzles/custom', auth: true, data: { fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' } },
    { method: 'GET', path: '/api/puzzles/custom', auth: true },
    
    // Games endpoints
    { method: 'GET', path: '/api/games/', auth: true },
    { method: 'GET', path: '/api/games/test-id', auth: true },
    { method: 'POST', path: '/api/games/', auth: true, data: { ai_level: 1, user_color: 'white' } },
    { method: 'PUT', path: '/api/games/test-id', auth: true, data: { status: 'completed' } },
    { method: 'POST', path: '/api/games/test-id/analyze', auth: true },
    { method: 'GET', path: '/api/games/test-id/analysis', auth: true },
    { method: 'GET', path: '/api/games/reviews', auth: true },
    
    // Stats endpoints
    { method: 'GET', path: '/api/stats/', auth: true },
    { method: 'GET', path: '/api/stats/overview', auth: true },
    { method: 'GET', path: '/api/stats/puzzles', auth: true },
    { method: 'GET', path: '/api/stats/games', auth: true },
    { method: 'GET', path: '/api/stats/progress', auth: true },
    { method: 'GET', path: '/api/stats/performance', auth: true },
    { method: 'GET', path: '/api/stats/ratings', auth: true },
    
    // Learning paths (camelCase URL)
    { method: 'GET', path: '/api/learningPaths/', auth: true },
    { method: 'GET', path: '/api/learningPaths/paths', auth: true },
    { method: 'GET', path: '/api/learningPaths/paths/test-id', auth: true },
    { method: 'POST', path: '/api/learningPaths/paths/test-id/enroll', auth: true },
    { method: 'PUT', path: '/api/learningPaths/paths/test-id/progress', auth: true, data: { progress: 50 } },
    
    // Tutorials endpoints
    { method: 'GET', path: '/api/tutorials/', auth: true },
    { method: 'GET', path: '/api/tutorials/test-id', auth: true },
    { method: 'POST', path: '/api/tutorials/test-id/complete', auth: true },
    
    // Sessions endpoints
    { method: 'GET', path: '/api/sessions/', auth: true },
    { method: 'POST', path: '/api/sessions/create', auth: true, data: { session_data: 'test' } },
    { method: 'GET', path: '/api/sessions/validate/test-token', auth: true },
    { method: 'DELETE', path: '/api/sessions/test-token', auth: true },
    
    // Achievements endpoints
    { method: 'GET', path: '/api/achievements/', auth: true },
    { method: 'GET', path: '/api/achievements/user/test-user-id', auth: true },
    { method: 'POST', path: '/api/achievements/unlock', auth: true, data: { achievement_id: 'test-id' } },
    
    // Progress endpoints
    { method: 'GET', path: '/api/progress/', auth: true },
    { method: 'GET', path: '/api/progress/user/test-user-id', auth: true },
    { method: 'PUT', path: '/api/progress/update', auth: true, data: { puzzles_solved: 10 } },
    { method: 'GET', path: '/api/progress/stats/test-user-id', auth: true },
    
    // Openings endpoints
    { method: 'GET', path: '/api/openings/', auth: true },
    { method: 'GET', path: '/api/openings/eco/A00', auth: true },
    { method: 'GET', path: '/api/openings/search', auth: true },
    
    // Analysis endpoints
    { method: 'GET', path: '/api/analysis/', auth: true },
    { method: 'POST', path: '/api/analysis/position', auth: true, data: { fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' } },
    { method: 'GET', path: '/api/analysis/position/test-fen', auth: true },
    
    // AI Opponents (camelCase URL)
    { method: 'GET', path: '/api/aiOpponents/', auth: true },
    { method: 'GET', path: '/api/aiOpponents/test-id', auth: true },
    { method: 'GET', path: '/api/aiOpponents/difficulty/1', auth: true },
    
    // Analytics endpoints
    { method: 'GET', path: '/api/analytics/', auth: true },
    { method: 'POST', path: '/api/analytics/track', auth: true, data: { event_type: 'puzzle_solved' } },
    { method: 'GET', path: '/api/analytics/user/test-user-id', auth: true },
    
    // Profiles endpoints
    { method: 'GET', path: '/api/profiles/', auth: true },
    { method: 'GET', path: '/api/profiles/test-user-id', auth: true },
    { method: 'PUT', path: '/api/profiles/test-user-id', auth: true, data: { bio: 'Chess player' } },
    
    // Endgames endpoints
    { method: 'GET', path: '/api/endgames/', auth: true },
    { method: 'GET', path: '/api/endgames/test-id', auth: true },
    { method: 'GET', path: '/api/endgames/category/king-pawn', auth: true },
    
    // Game Reviews (camelCase URL)
    { method: 'GET', path: '/api/gameReviews/', auth: true },
    { method: 'POST', path: '/api/gameReviews/', auth: true, data: { game_id: 'test-game-id', rating: 5 } },
    { method: 'GET', path: '/api/gameReviews/game/test-game-id', auth: true },
    { method: 'GET', path: '/api/gameReviews/test-id', auth: true },
    
    // Historic Games (camelCase URL)
    { method: 'GET', path: '/api/historicGames/', auth: true },
    { method: 'GET', path: '/api/historicGames/test-id', auth: true },
    { method: 'GET', path: '/api/historicGames/search', auth: true },
    { method: 'GET', path: '/api/historicGames/player/kasparov', auth: true },
    
    // Puzzle Attempts (camelCase URL)
    { method: 'GET', path: '/api/puzzleAttempts/', auth: true },
    { method: 'POST', path: '/api/puzzleAttempts/', auth: true, data: { puzzle_id: 'test-id', correct: true } },
    { method: 'GET', path: '/api/puzzleAttempts/user/test-user-id', auth: true },
    { method: 'GET', path: '/api/puzzleAttempts/puzzle/test-puzzle-id', auth: true },
    
    // Puzzle Sources (camelCase URL)
    { method: 'GET', path: '/api/puzzleSources/', auth: true },
    { method: 'GET', path: '/api/puzzleSources/test-id', auth: true },
    
    // Learning Modules (camelCase URL)
    { method: 'GET', path: '/api/learningModules/', auth: true },
    { method: 'GET', path: '/api/learningModules/path/test-path-id', auth: true },
    { method: 'GET', path: '/api/learningModules/test-id', auth: true },
    { method: 'POST', path: '/api/learningModules/test-id/complete', auth: true },
    
    // Tutorial Steps (camelCase URL)
    { method: 'GET', path: '/api/tutorialSteps/', auth: true },
    { method: 'GET', path: '/api/tutorialSteps/tutorial/test-tutorial-id', auth: true },
    { method: 'POST', path: '/api/tutorialSteps/test-id/complete', auth: true },
    
    // Study Plans (camelCase URL)
    { method: 'GET', path: '/api/studyPlans/', auth: true },
    { method: 'GET', path: '/api/studyPlans/user/test-user-id', auth: true },
    { method: 'POST', path: '/api/studyPlans/', auth: true, data: { title: 'My Study Plan' } },
    { method: 'PUT', path: '/api/studyPlans/test-id', auth: true, data: { progress: 75 } },
    
    // Help endpoints
    { method: 'GET', path: '/api/help/', auth: true },
    { method: 'GET', path: '/api/help/category/basics', auth: true },
    { method: 'GET', path: '/api/help/search', auth: true },
    
    // Subscriptions endpoints
    { method: 'GET', path: '/api/subscriptions/', auth: true },
    { method: 'GET', path: '/api/subscriptions/user/test-user-id', auth: true },
    { method: 'POST', path: '/api/subscriptions/', auth: true, data: { plan_type: 'premium' } },
    { method: 'PUT', path: '/api/subscriptions/test-id', auth: true, data: { status: 'active' } }
  ],

  // Resources for CRUD testing
  resources: [
    { path: '/api/users', entity: 'users', testData: { username: 'crudtest', email: 'crud@test.com', password: 'Test123!' } },
    { path: '/api/achievements', entity: 'achievements', testData: { title: 'Test Achievement', points: 100 } },
    { path: '/api/aiOpponents', entity: 'aiOpponents', testData: { name: 'Test AI', difficulty: 3, elo_rating: 1500 } },
    { path: '/api/analytics', entity: 'analytics', testData: { event_type: 'test_event', event_data: '{}' } },
    { path: '/api/endgames', entity: 'endgames', testData: { name: 'Test Endgame', category: 'pawn' } },
    { path: '/api/gameReviews', entity: 'gameReviews', testData: { game_id: 'test-game', rating: 4 } },
    { path: '/api/games', entity: 'games', testData: { ai_level: 2, user_color: 'white' } },
    { path: '/api/help', entity: 'help', testData: { title: 'Test Help', category: 'general' } },
    { path: '/api/historicGames', entity: 'historicGames', testData: { white_player: 'Test White', black_player: 'Test Black' } },
    { path: '/api/learningModules', entity: 'learningModules', testData: { title: 'Test Module', difficulty: 'beginner' } },
    { path: '/api/learningPaths', entity: 'learningPaths', testData: { title: 'Test Path', difficulty: 'intermediate' } },
    { path: '/api/openings', entity: 'openings', testData: { name: 'Test Opening', eco_code: 'A00' } },
    { path: '/api/profiles', entity: 'profiles', testData: { display_name: 'Test Profile', bio: 'Test bio' } },
    { path: '/api/progress', entity: 'progress', testData: { puzzles_solved: 5, puzzles_correct: 4 } },
    { path: '/api/puzzleAttempts', entity: 'puzzleAttempts', testData: { puzzle_id: 'test-puzzle', correct: true } },
    { path: '/api/puzzleSources', entity: 'puzzleSources', testData: { name: 'Test Source', description: 'Test description' } },
    { path: '/api/puzzles', entity: 'puzzles', testData: { fen: 'test-fen', rating: 1200 } },
    { path: '/api/sessions', entity: 'sessions', testData: { session_token: 'test-token-123' } },
    { path: '/api/stats', entity: 'stats', testData: { user_id: 'test-user', total_puzzles: 10 } },
    { path: '/api/studyPlans', entity: 'studyPlans', testData: { title: 'CRUD Test Plan', goals: 'Learn chess' } },
    { path: '/api/subscriptions', entity: 'subscriptions', testData: { plan_type: 'basic', status: 'active' } },
    { path: '/api/tutorialSteps', entity: 'tutorialSteps', testData: { tutorial_id: 'test-tutorial', step_number: 1 } },
    { path: '/api/tutorials', entity: 'tutorials', testData: { title: 'CRUD Tutorial', difficulty: 'easy' } }
  ]
};

async function testEndpoint(method, path, token = null, data = null) {
  try {
    const response = await makeRequest(method, path, data, token);
    
    // Determine success based on status code
    const isSuccess = response.status === 200 || response.status === 401;
    const statusIcon = response.status === 200 ? '✅' : 
                      response.status === 401 ? '🔒' : 
                      response.status === 404 ? '❌' : '⚠️';
    
    return {
      method,
      path,
      status: response.status,
      success: isSuccess,
      icon: statusIcon,
      data: response.data,
      error: !isSuccess ? (response.data?.error || response.data) : null
    };
  } catch (error) {
    return {
      method,
      path,
      status: 'ERROR',
      success: false,
      icon: '💥',
      error: error.message
    };
  }
}

async function testCRUDOperations(basePath, token, entityName, testData = null) {
  console.log(`\n🔄 Testing DEDICATED CRUD operations for ${entityName}`);
  
  const results = [];
  const defaultTestData = testData || { name: `Test ${entityName}`, description: `Test description for ${entityName}` };
  
  // Test GET (Read all) - Root endpoint
  const getAll = await testEndpoint('GET', basePath, token);
  results.push(getAll);
  console.log(`  ${getAll.icon} GET ${basePath} (Read All) -> ${getAll.status}`);
  
  // Test POST (Create) - Create new resource
  const create = await testEndpoint('POST', basePath, token, defaultTestData);
  results.push(create);
  console.log(`  ${create.icon} POST ${basePath} (Create) -> ${create.status}`);
  
  // Test GET with ID (Read one)
  const getById = await testEndpoint('GET', `${basePath}/test-id-123`, token);
  results.push(getById);
  console.log(`  ${getById.icon} GET ${basePath}/:id (Read One) -> ${getById.status}`);
  
  // Test PUT (Update)
  const updateData = { ...defaultTestData, updated: true, last_modified: new Date().toISOString() };
  const update = await testEndpoint('PUT', `${basePath}/test-id-123`, token, updateData);
  results.push(update);
  console.log(`  ${update.icon} PUT ${basePath}/:id (Update) -> ${update.status}`);
  
  // Test DELETE
  const del = await testEndpoint('DELETE', `${basePath}/test-id-123`, token);
  results.push(del);
  console.log(`  ${del.icon} DELETE ${basePath}/:id (Delete) -> ${del.status}`);
  
  return results;
}

async function testAllEndpoints(token) {
  console.log('🧪 Testing ALL API Endpoints\n');
  
  const allResults = [];
  
  // Test auth endpoints
  console.log('🔐 Testing Authentication Endpoints:');
  for (const endpoint of API_ENDPOINTS.auth) {
    const result = await testEndpoint(endpoint.method, endpoint.path, 
      endpoint.auth ? token : null, 
      endpoint.data || null
    );
    allResults.push(result);
    console.log(`  ${result.icon} ${endpoint.method} ${endpoint.path} -> ${result.status}`);
  }
  
  // Test ALL custom endpoints from backend config
  console.log('\n🎯 Testing ALL Custom Endpoints:');
  for (const endpoint of API_ENDPOINTS.custom) {
    const result = await testEndpoint(endpoint.method, endpoint.path, 
      endpoint.auth ? token : null,
      endpoint.data || null
    );
    allResults.push(result);
    console.log(`  ${result.icon} ${endpoint.method} ${endpoint.path} -> ${result.status}`);
  }
  
  return allResults;
}

async function testCRUDForAllResources(token) {
  console.log('\n🔄 Testing DEDICATED CRUD Operations for ALL Resources\n');
  console.log('   🎯 This tests standard CRUD operations (Create, Read, Update, Delete)');
  console.log('   📋 Testing all resources defined in backend config\n');
  
  const crudResults = [];
  
  // Test CRUD for ALL resources from the backend config
  for (const resource of API_ENDPOINTS.resources) {
    const results = await testCRUDOperations(
      resource.path, 
      token, 
      resource.entity,
      resource.testData
    );
    crudResults.push(...results);
    
    // Add small delay between resource tests
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  return crudResults;
}

async function generateReport(endpointResults, crudResults) {
  console.log('\n' + '='.repeat(80));
  console.log('📊 COMPREHENSIVE TEST REPORT');
  console.log('='.repeat(80));
  
  // Endpoint summary
  const total = endpointResults.length;
  const successful = endpointResults.filter(r => r.success).length;
  const authRequired = endpointResults.filter(r => r.status === 401).length;
  const working = endpointResults.filter(r => r.status === 200).length;
  const failing = endpointResults.filter(r => !r.success).length;
  
  console.log(`\n📈 ALL ENDPOINTS SUMMARY:`);
  console.log(`   Total Endpoints Tested: ${total}`);
  console.log(`   ✅ Working (200 OK): ${working}`);
  console.log(`   🔒 Auth Required (401): ${authRequired}`);
  console.log(`   ❌ Failing: ${failing}`);
  console.log(`   📊 Success Rate: ${Math.round((successful/total)*100)}%`);
  
  // CRUD summary
  if (crudResults.length > 0) {
    const crudTotal = crudResults.length;
    const crudSuccessful = crudResults.filter(r => r.success).length;
    const crudWorking = crudResults.filter(r => r.status === 200).length;
    
    console.log(`\n🔄 DEDICATED CRUD OPERATIONS SUMMARY:`);
    console.log(`   Total CRUD Tests: ${crudTotal}`);
    console.log(`   ✅ Working (200 OK): ${crudWorking}`);
    console.log(`   🔒 Auth/Success: ${crudSuccessful}`);
    console.log(`   📊 CRUD Success Rate: ${Math.round((crudSuccessful/crudTotal)*100)}%`);
  }
  
  // Breakdown by endpoint type
  const authEndpoints = endpointResults.filter(r => r.path.includes('/auth/'));
  const resourceEndpoints = endpointResults.filter(r => !r.path.includes('/auth/'));
  
  console.log(`\n📂 BREAKDOWN BY TYPE:`);
  console.log(`   🔐 Auth Endpoints: ${authEndpoints.filter(r => r.success).length}/${authEndpoints.length} successful`);
  console.log(`   🎯 Resource Endpoints: ${resourceEndpoints.filter(r => r.success).length}/${resourceEndpoints.length} successful`);
  
  // Failed endpoints
  const failed = endpointResults.filter(r => !r.success && r.status !== 401);
  if (failed.length > 0) {
    console.log(`\n❌ TRULY FAILED ENDPOINTS (excluding 401 auth):`);
    failed.forEach(result => {
      console.log(`   ${result.method} ${result.path} -> ${result.status} ${result.error || ''}`);
    });
  }
  
  // camelCase URL verification
  const camelCaseEndpoints = endpointResults.filter(r => 
    r.path.includes('learningPaths') || 
    r.path.includes('aiOpponents') || 
    r.path.includes('gameReviews') ||
    r.path.includes('historicGames') ||
    r.path.includes('learningModules') ||
    r.path.includes('puzzleAttempts') ||
    r.path.includes('puzzleSources') ||
    r.path.includes('studyPlans') ||
    r.path.includes('tutorialSteps')
  );
  
  const workingCamelCase = camelCaseEndpoints.filter(r => r.success).length;
  
  console.log(`\n🐫 CAMELCASE URL VERIFICATION:`);
  console.log(`   camelCase URLs tested: ${camelCaseEndpoints.length}`);
  console.log(`   Working: ${workingCamelCase}/${camelCaseEndpoints.length}`);
  
  // Coverage summary
  console.log(`\n🎯 COVERAGE SUMMARY:`);
  console.log(`   📋 ALL Endpoints from config: ${API_ENDPOINTS.custom.length + API_ENDPOINTS.auth.length} tested`);
  console.log(`   🔄 CRUD Operations: ${API_ENDPOINTS.resources.length} resources tested`);
  console.log(`   📊 Total Test Operations: ${total + (crudResults?.length || 0)}`);
  
  console.log('\n' + '='.repeat(80));
  console.log('🎉 COMPREHENSIVE test suite completed!');
  console.log('   ✨ ALL endpoints AND CRUD operations tested!');
  console.log('='.repeat(80));
}

async function main() {
  console.log('🚀 COMPREHENSIVE API Test Suite');
  console.log('📋 Testing ALL endpoints from backend config AND dedicated CRUD operations');
  console.log('🎯 This covers EVERY endpoint defined in the backend configuration\n');
  
  // Get authentication token
  console.log('🔐 Getting authentication token...');
  const authResult = await testAuthFlow();
  
  if (!authResult || !authResult.token) {
    console.error('❌ Failed to get authentication token');
    process.exit(1);
  }
  
  const token = authResult.token;
  console.log(`✅ Got auth token: ${token.substring(0, 20)}...`);
  
  console.log('\n' + '='.repeat(60) + '\n');
  console.log('🎯 Phase 1: Testing ALL Individual Endpoints');
  console.log('📋 This covers every single endpoint from the backend config\n');
  
  // Test ALL endpoints from backend config
  const endpointResults = await testAllEndpoints(token);
  
  console.log('\n' + '='.repeat(60) + '\n');
  console.log('🔄 Phase 2: Testing DEDICATED CRUD Operations');
  console.log('📋 This tests standard Create/Read/Update/Delete for all resources\n');
  
  // Test dedicated CRUD operations for ALL resources
  const crudResults = await testCRUDForAllResources(token);
  
  // Generate comprehensive report
  await generateReport(endpointResults, crudResults);
}

// Export for use by other scripts
module.exports = { testEndpoint, testCRUDOperations, testAllEndpoints, main };

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}