const axios = require('axios');

async function testAuth() {
  console.log('🧪 Starting auth debug test...');
  
  try {
    // 1. Register a user
    console.log('\n1. Registering user...');
    const registerResponse = await axios.post('http://localhost:3001/api/auth/register', {
      username: 'testuser_debug_' + Date.now(),
      email: 'testuser_debug_' + Date.now() + '@example.com',
      password: 'password123'
    });
    console.log('✅ Registration successful');
    
    // 2. Login to get token
    console.log('\n2. Logging in...');
    const loginResponse = await axios.post('http://localhost:3001/api/auth/login', {
      email: registerResponse.data.data.email,
      password: 'password123'
    });
    console.log('✅ Login successful');
    console.log('🎫 Token received:', loginResponse.data.data.token.substring(0, 50) + '...');
    
    const token = loginResponse.data.data.token;
    
    // 3. Test the auth/me endpoint with detailed logging
    console.log('\n3. Testing /auth/me endpoint...');
    try {
      const meResponse = await axios.get('http://localhost:3001/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      console.log('✅ /auth/me successful:', meResponse.data);
    } catch (error) {
      console.log('❌ /auth/me failed:', error.response?.data || error.message);
    }
    
  } catch (error) {
    console.log('❌ Test failed:', error.response?.data || error.message);
  }
}

testAuth();