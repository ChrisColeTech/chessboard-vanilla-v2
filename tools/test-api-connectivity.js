#!/usr/bin/env node
/**
 * Comprehensive API Connectivity Test Script
 * Tests all endpoints from frontend (port 5173) to backend (port 3001)
 * Based on backend_config.json routes
 */

const fs = require('fs');
const path = require('path');

// Configuration
const FRONTEND_URL = 'http://localhost:5173';
const BACKEND_URL = 'http://localhost:3001';
const CONFIG_PATH = path.join(__dirname, 'backend-tools', 'backend_config.json');

// Global auth token
let authToken = null;

// Load backend configuration
let backendConfig;
try {
    const configData = fs.readFileSync(CONFIG_PATH, 'utf8');
    backendConfig = JSON.parse(configData);
} catch (error) {
    console.error('❌ Failed to load backend config:', error.message);
    process.exit(1);
}

/**
 * Convert snake_case to camelCase (matching our frontend generator)
 */
function snakeToCamelCase(str) {
    const components = str.split('_');
    return components[0] + components.slice(1).map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join('');
}

/**
 * Authenticate and get a token
 */
async function authenticate() {
    console.log('🔐 Setting up authentication...');
    
    const testUser = {
        username: 'testuser3',
        email: 'test3@example.com',
        password: 'password123'
    };
    
    try {
        // Try to register a test user (no auth required)
        const registerResult = await testEndpoint('POST', `${BACKEND_URL}/api/auth/register`, testUser, false);
        
        if (registerResult.ok || registerResult.status === 400) { // 400 might mean user exists
            // Try to login (no auth required)
            const loginResult = await testEndpoint('POST', `${BACKEND_URL}/api/auth/login`, {
                email: testUser.email,
                password: testUser.password
            }, false);
            
            if (loginResult.ok && loginResult.data && loginResult.data.data && loginResult.data.data.token) {
                authToken = loginResult.data.data.token;
                console.log('  ✅ Authentication successful!');
                return true;
            } else if (registerResult.status === 400) {
                // User might exist, try with a more generic user
                const genericLoginResult = await testEndpoint('POST', `${BACKEND_URL}/api/auth/login`, {
                    email: 'admin@admin.com',
                    password: 'admin'
                }, false);
                
                if (genericLoginResult.ok && genericLoginResult.data && genericLoginResult.data.data && genericLoginResult.data.data.token) {
                    authToken = genericLoginResult.data.data.token;
                    console.log('  ✅ Authentication successful with default credentials!');
                    return true;
                }
            }
        }
        
        console.log('  ⚠️  Authentication failed, continuing without token (some endpoints may fail)');
        return false;
    } catch (error) {
        console.log('  ⚠️  Authentication error:', error.message);
        return false;
    }
}

/**
 * Test a single endpoint
 */
async function testEndpoint(method, url, data = null, requireAuth = true) {
    try {
        const options = {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };

        // Add auth token if available and required
        if (authToken && requireAuth) {
            options.headers['Authorization'] = `Bearer ${authToken}`;
        }

        if (data && ['POST', 'PUT', 'PATCH'].includes(method.toUpperCase())) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        const result = {
            status: response.status,
            ok: response.ok,
            statusText: response.statusText,
            url: url
        };

        // Try to parse JSON response
        try {
            const text = await response.text();
            if (text) {
                result.data = JSON.parse(text);
            }
        } catch (e) {
            // Non-JSON response, that's okay
        }

        return result;
    } catch (error) {
        return {
            error: error.message,
            url: url,
            status: 'ERROR'
        };
    }
}

/**
 * Generate test data for different entity types
 */
function generateTestData(entityName) {
    const baseData = {
        id: 'test-id-' + Date.now(),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    };

    switch (entityName.toLowerCase()) {
        case 'user':
            return { ...baseData, username: 'testuser', email: 'test@example.com' };
        case 'puzzle':
            return { ...baseData, fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', solution: 'e2e4' };
        case 'game':
            return { ...baseData, pgn: '1. e4 e5', result: '1-0' };
        case 'achievement':
            return { ...baseData, title: 'Test Achievement', description: 'Test description' };
        case 'tutorial':
            return { ...baseData, title: 'Test Tutorial', content: 'Test content' };
        default:
            return { ...baseData, name: `Test ${entityName}`, description: 'Test description' };
    }
}

/**
 * Build full URL for an endpoint
 */
function buildEndpointUrl(endpointName, endpointConfig, apiEndpoint) {
    const entities = endpointConfig.entities || endpointName;
    const camelCaseEntities = snakeToCamelCase(entities);
    
    let basePath;
    if (endpointName === 'auth') {
        basePath = '/api/auth';  // Fixed: auth routes are under /api/auth not /auth
    } else {
        basePath = `/api/${camelCaseEntities}`;
    }
    
    let fullPath = basePath + apiEndpoint.path;
    
    // Replace path parameters with test values
    fullPath = fullPath.replace(/:id/g, 'test-id-123');
    fullPath = fullPath.replace(/:userId/g, 'test-user-123');
    fullPath = fullPath.replace(/:puzzleId/g, 'test-puzzle-123');
    fullPath = fullPath.replace(/:gameId/g, 'test-game-123');
    fullPath = fullPath.replace(/:fen/g, 'rnbqkbnr-pppppppp-8-8-8-8-PPPPPPPP-RNBQKBNR');
    fullPath = fullPath.replace(/:level/g, 'beginner');
    fullPath = fullPath.replace(/:category/g, 'endgame');
    fullPath = fullPath.replace(/:player/g, 'kasparov');
    fullPath = fullPath.replace(/:pathId/g, 'test-path-123');
    fullPath = fullPath.replace(/:tutorialId/g, 'test-tutorial-123');
    
    return BACKEND_URL + fullPath;
}

/**
 * Test all endpoints for connectivity
 */
async function testAllEndpoints() {
    console.log('🚀 Starting API Connectivity Test');
    console.log('📊 Testing all endpoints from backend config...\n');

    // Try to authenticate first - REQUIRED for protected endpoints
    const authSuccess = await authenticate();
    if (!authSuccess) {
        console.log('❌ Authentication failed. Cannot test protected endpoints without valid token.');
        console.log('💡 Please ensure database is running and auth endpoints are working.');
        process.exit(1);
    }

    const results = {
        total: 0,
        successful: 0,
        failed: 0,
        errors: []
    };

    // Test each endpoint
    for (const [endpointName, endpointConfig] of Object.entries(backendConfig.endpoints)) {
        console.log(`\n🔍 Testing ${endpointName} endpoints:`);
        
        const endpoints = endpointConfig.endpoints || [];
        
        for (const apiEndpoint of endpoints) {
            results.total++;
            
            const url = buildEndpointUrl(endpointName, endpointConfig, apiEndpoint);
            const method = apiEndpoint.method;
            const handler = apiEndpoint.handler;
            
            // Generate test data for POST/PUT requests
            let testData = null;
            if (['POST', 'PUT', 'PATCH'].includes(method.toUpperCase()) && 
                !apiEndpoint.path.includes('complete') && 
                !apiEndpoint.path.includes('unlock') &&
                !apiEndpoint.path.includes('enroll')) {
                testData = generateTestData(endpointConfig.entity);
            }
            
            console.log(`  ${method.padEnd(6)} ${url}`);
            
            // Check if auth is required for this endpoint
            const requireAuth = apiEndpoint.auth_required !== false; // Default to true unless explicitly false
            
            const result = await testEndpoint(method, url, testData, requireAuth);
            
            if (result.error) {
                console.log(`    ❌ ERROR: ${result.error}`);
                results.failed++;
                results.errors.push({
                    endpoint: `${method} ${url}`,
                    error: result.error,
                    handler: handler
                });
            } else if ([200, 201].includes(result.status)) {
                // Only 200/201 indicate actual success
                console.log(`    ✅ ${result.status} ${result.statusText}`);
                results.successful++;
            } else {
                console.log(`    ⚠️  ${result.status} ${result.statusText}`);
                results.failed++;
                results.errors.push({
                    endpoint: `${method} ${url}`,
                    status: result.status,
                    statusText: result.statusText,
                    handler: handler
                });
            }
            
            // Small delay to avoid overwhelming the server
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }

    // Print summary
    console.log('\n' + '='.repeat(60));
    console.log('📊 API CONNECTIVITY TEST RESULTS');
    console.log('='.repeat(60));
    console.log(`Total Endpoints Tested: ${results.total}`);
    console.log(`✅ Successful: ${results.successful} (${(results.successful/results.total*100).toFixed(1)}%)`);
    console.log(`❌ Failed: ${results.failed} (${(results.failed/results.total*100).toFixed(1)}%)`);
    
    if (results.errors.length > 0) {
        console.log('\n🔍 ERROR DETAILS:');
        results.errors.forEach((error, index) => {
            console.log(`${index + 1}. ${error.endpoint}`);
            if (error.error) {
                console.log(`   Error: ${error.error}`);
            }
            if (error.status) {
                console.log(`   Status: ${error.status} ${error.statusText}`);
            }
            console.log(`   Handler: ${error.handler}`);
        });
    }
    
    // Test basic frontend access
    console.log('\n🌐 Testing Frontend Access:');
    try {
        const frontendResult = await testEndpoint('GET', FRONTEND_URL);
        if (frontendResult.ok) {
            console.log(`  ✅ Frontend accessible at ${FRONTEND_URL}`);
        } else {
            console.log(`  ❌ Frontend not accessible: ${frontendResult.status} ${frontendResult.statusText}`);
        }
    } catch (error) {
        console.log(`  ❌ Frontend error: ${error.message}`);
    }
    
    const successRate = (results.successful / results.total * 100).toFixed(1);
    console.log(`\n🎯 Overall Success Rate: ${successRate}%`);
    
    if (successRate === '100.0') {
        console.log('🎉 PERFECT! 100% API connectivity achieved!');
        return true;
    } else if (successRate >= '90.0') {
        console.log('🎊 EXCELLENT! Over 90% connectivity achieved!');
        return true;
    } else {
        console.log('⚠️  Issues detected. Please review the errors above.');
        return false;
    }
}

// Run the test
if (require.main === module) {
    testAllEndpoints()
        .then(success => {
            process.exit(success ? 0 : 1);
        })
        .catch(error => {
            console.error('Fatal error:', error);
            process.exit(1);
        });
}

module.exports = { testAllEndpoints };