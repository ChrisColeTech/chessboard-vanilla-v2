#!/usr/bin/env python3
"""
Focused Endpoint Tests for Debugging

This test suite focuses exclusively on the 8 failing endpoints to troubleshoot
the specific causes of JSON formatting and foreign key constraint failures.
"""

import requests
import json
import time
import sys
import os
from typing import Dict, Any, List, Tuple

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mini-payload-generator'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'payload-generator'))

from mini_payload_generator import MiniPayloadGenerator


class FocusedEndpointTester:
    def __init__(self, base_url: str = "http://localhost:3001"):
        """Initialize the focused endpoint tester."""
        self.base_url = base_url
        self.payload_generator = MiniPayloadGenerator()
        self.test_results = []
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_id = None
        self.created_content_id = None
        self.created_puzzle_id = None
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def wait_for_server(self, timeout: int = 30) -> bool:
        """Wait for the server to be ready."""
        print(f"🔄 Waiting for server at {self.base_url}...")
        
        for i in range(timeout):
            try:
                response = self.session.get(f"{self.base_url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✅ Server is ready!")
                    return True
            except Exception as e:
                if i == 0:
                    print(f"⏳ Server not ready, waiting... ({e})")
                time.sleep(1)
        
        print(f"❌ Server not ready after {timeout} seconds")
        return False
    
    def authenticate(self) -> bool:
        """Authenticate and get an access token."""
        print("🔐 Setting up authentication...")
        
        try:
            # Generate unique test user credentials
            timestamp = int(time.time())
            test_user = {
                "username": f"focusedtest_{timestamp}",
                "email": f"focusedtest_{timestamp}@example.com",
                "password": "focusedtest123"
            }
            
            # Register test user
            print(f"📝 Registering test user: {test_user['email']}")
            register_response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=test_user,
                timeout=10
            )
            
            if register_response.status_code not in [200, 201]:
                print(f"❌ Registration failed: {register_response.status_code} - {register_response.text}")
                return False
            
            print("✅ User registered successfully")
            
            # Login to get token
            print("🔑 Logging in to get access token...")
            login_response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={"email": test_user["email"], "password": test_user["password"]},
                timeout=10
            )
            
            if login_response.status_code != 200:
                print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
                return False
            
            login_data = login_response.json()
            print(f"📋 Login response: {json.dumps(login_data, indent=2)[:200]}...")
            
            # Extract token from response
            self.auth_token = (
                login_data.get("token") or 
                (login_data.get("data", {}).get("token")) or
                (login_data.get("access", {}).get("token")) or
                (login_data.get("auth", {}).get("token"))
            )
            
            if not self.auth_token:
                print(f"❌ No token found in login response: {login_data}")
                return False
            
            print(f"✅ Authentication successful! Token: {self.auth_token[:20]}...")
            
            # Update session headers with token
            self.session.headers.update({
                'Authorization': f'Bearer {self.auth_token}'
            })
            
            # Get user info to extract user ID
            me_response = self.session.get(f"{self.base_url}/api/auth/me", timeout=10)
            if me_response.status_code == 200:
                user_data = me_response.json()
                # Handle nested data structure
                if isinstance(user_data.get("data"), dict):
                    user_info = user_data["data"]
                    if isinstance(user_info.get("user"), dict):
                        self.test_user_id = user_info["user"].get("id")
                    else:
                        self.test_user_id = user_info.get("id")
                else:
                    self.test_user_id = user_data.get("id")
                print(f"👤 User ID: {self.test_user_id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def make_request(self, method: str, endpoint: str, payload: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Tuple[int, str, str]:
        """Make a request and return status code, response text, and error details."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=payload, timeout=10)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=payload, timeout=10)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=10)
            else:
                return 0, "", f"Unsupported method: {method}"
            
            return response.status_code, response.text, ""
            
        except requests.exceptions.Timeout:
            return 0, "", "Request timeout"
        except requests.exceptions.ConnectionError:
            return 0, "", "Connection error"
        except Exception as e:
            return 0, "", f"Request error: {str(e)}"
    
    def test_content_post(self) -> Dict[str, Any]:
        """Test POST /api/content/ endpoint."""
        print("\n🔍 Testing POST /api/content/")
        
        payload = self.payload_generator.generate_content_payload()
        print(f"📦 Payload preview: {json.dumps(payload, indent=2)[:200]}...")
        
        status_code, response_text, error = self.make_request("POST", "/api/content/", payload)
        
        result = {
            "endpoint": "POST /api/content/",
            "status_code": status_code,
            "success": status_code in [200, 201],
            "payload": payload,
            "response": response_text[:500] if response_text else "",
            "error": error
        }
        
        # Extract created content ID for PUT test
        if result["success"] and response_text:
            try:
                response_data = json.loads(response_text)
                if response_data.get("success") and response_data.get("data", {}).get("id"):
                    self.created_content_id = response_data["data"]["id"]
                    print(f"📋 Created content ID: {self.created_content_id}")
            except:
                pass
        
        if not result["success"]:
            print(f"❌ Failed: {status_code} - {response_text[:200]}")
        else:
            print(f"✅ Success: {status_code}")
        
        return result
    
    def test_content_put(self) -> Dict[str, Any]:
        """Test PUT /api/content/:id endpoint."""
        print("\n🔍 Testing PUT /api/content/:id")
        
        # Use created content ID if available, otherwise skip
        if not self.created_content_id:
            print("⚠️  Skipping PUT test - no content ID from POST test")
            return {
                "endpoint": "PUT /api/content/:id",
                "status_code": 0,
                "success": False,
                "error": "No content ID available from POST test"
            }
        
        payload = self.payload_generator.generate_content_payload()
        # Modify payload slightly for update
        payload["title"] = "Updated Test Content for Debugging"
        
        print(f"📦 Payload preview: {json.dumps(payload, indent=2)[:200]}...")
        print(f"📦 Content ID: {self.created_content_id}")
        
        status_code, response_text, error = self.make_request("PUT", f"/api/content/{self.created_content_id}", payload)
        
        result = {
            "endpoint": f"PUT /api/content/{self.created_content_id}",
            "status_code": status_code,
            "success": status_code in [200, 201],
            "payload": payload,
            "response": response_text[:500] if response_text else "",
            "error": error
        }
        
        if not result["success"]:
            print(f"❌ Failed: {status_code} - {response_text[:200]}")
        else:
            print(f"✅ Success: {status_code}")
        
        return result
    
    def test_puzzle_post(self) -> Dict[str, Any]:
        """Test POST /api/puzzles/ endpoint."""
        print("\n🔍 Testing POST /api/puzzles/")
        
        payload = self.payload_generator.generate_puzzle_payload()
        print(f"📦 Payload preview: {json.dumps(payload, indent=2)[:200]}...")
        
        status_code, response_text, error = self.make_request("POST", "/api/puzzles/", payload)
        
        result = {
            "endpoint": "POST /api/puzzles/",
            "status_code": status_code,
            "success": status_code in [200, 201],
            "payload": payload,
            "response": response_text[:500] if response_text else "",
            "error": error
        }
        
        # Extract created puzzle ID for PUT test
        if result["success"] and response_text:
            try:
                response_data = json.loads(response_text)
                if response_data.get("success") and response_data.get("data", {}).get("id"):
                    self.created_puzzle_id = response_data["data"]["id"]
                    print(f"📋 Created puzzle ID: {self.created_puzzle_id}")
            except:
                pass
        
        if not result["success"]:
            print(f"❌ Failed: {status_code} - {response_text[:200]}")
        else:
            print(f"✅ Success: {status_code}")
        
        return result
    
    def test_puzzle_put(self) -> Dict[str, Any]:
        """Test PUT /api/puzzles/:id endpoint."""
        print("\n🔍 Testing PUT /api/puzzles/:id")
        
        # Use created puzzle ID if available, otherwise skip
        if not self.created_puzzle_id:
            print("⚠️  Skipping PUT test - no puzzle ID from POST test")
            return {
                "endpoint": "PUT /api/puzzles/:id",
                "status_code": 0,
                "success": False,
                "error": "No puzzle ID available from POST test"
            }
        
        payload = self.payload_generator.generate_puzzle_payload()
        # Modify payload slightly for update
        payload["title"] = "Updated Debug Puzzle: Fork Tactic"
        
        print(f"📦 Payload preview: {json.dumps(payload, indent=2)[:200]}...")
        print(f"📦 Puzzle ID: {self.created_puzzle_id}")
        
        status_code, response_text, error = self.make_request("PUT", f"/api/puzzles/{self.created_puzzle_id}", payload)
        
        result = {
            "endpoint": f"PUT /api/puzzles/{self.created_puzzle_id}",
            "status_code": status_code,
            "success": status_code in [200, 201],
            "payload": payload,
            "response": response_text[:500] if response_text else "",
            "error": error
        }
        
        if not result["success"]:
            print(f"❌ Failed: {status_code} - {response_text[:200]}")
        else:
            print(f"✅ Success: {status_code}")
        
        return result
    
    def test_puzzle_get_with_params(self) -> Dict[str, Any]:
        """Test GET /api/puzzles/ endpoint with parameters that might cause JSON parse errors."""
        print("\n🔍 Testing GET /api/puzzles/ with params")
        
        # Test with parameters that might cause JSON parsing issues
        params = {
            "themes": json.dumps(["tactics", "fork"]),  # JSON encoded param
            "difficulty": "intermediate",
            "limit": 10
        }
        
        print(f"📦 Params: {params}")
        
        status_code, response_text, error = self.make_request("GET", "/api/puzzles/", params=params)
        
        result = {
            "endpoint": "GET /api/puzzles/ (with params)",
            "status_code": status_code,
            "success": status_code == 200,
            "params": params,
            "response": response_text[:500] if response_text else "",
            "error": error
        }
        
        if not result["success"]:
            print(f"❌ Failed: {status_code} - {response_text[:200]}")
        else:
            print(f"✅ Success: {status_code}")
        
        return result
    
    def test_user_achievement_post(self) -> Dict[str, Any]:
        """Test POST /api/user-achievements/ endpoint."""
        print("\n🔍 Testing POST /api/user-achievements/")
        
        payload = self.payload_generator.generate_user_achievement_payload()
        print(f"📦 Payload preview: {json.dumps(payload, indent=2)[:200]}...")
        
        status_code, response_text, error = self.make_request("POST", "/api/user-achievements/", payload)
        
        result = {
            "endpoint": "POST /api/user-achievements/",
            "status_code": status_code,
            "success": status_code in [200, 201],
            "payload": payload,
            "response": response_text[:500] if response_text else "",
            "error": error
        }
        
        if not result["success"]:
            print(f"❌ Failed: {status_code} - {response_text[:200]}")
        else:
            print(f"✅ Success: {status_code}")
        
        return result
    
    def test_user_delete(self) -> Dict[str, Any]:
        """Test DELETE /api/users/ endpoint."""
        print("\n🔍 Testing DELETE /api/users/")
        
        user_id = self.payload_generator.get_user_id_for_deletion()
        endpoint = f"/api/users/{user_id}"
        
        print(f"📦 Deleting user ID: {user_id}")
        
        status_code, response_text, error = self.make_request("DELETE", endpoint)
        
        result = {
            "endpoint": f"DELETE /api/users/{user_id}",
            "status_code": status_code,
            "success": status_code in [200, 204],
            "user_id": user_id,
            "response": response_text[:500] if response_text else "",
            "error": error
        }
        
        if not result["success"]:
            print(f"❌ Failed: {status_code} - {response_text[:200]}")
        else:
            print(f"✅ Success: {status_code}")
        
        return result
    
    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run all focused tests for the failing endpoints."""
        print("🚀 FOCUSED ENDPOINT TESTING")
        print("=" * 50)
        print("Testing the 8 endpoints that are currently failing...")
        
        if not self.wait_for_server():
            print("❌ Cannot run tests - server is not responding")
            return []
        
        if not self.authenticate():
            print("❌ Cannot run tests - authentication failed")
            return []
        
        # Run all tests
        tests = [
            self.test_content_post,
            self.test_content_put,
            self.test_puzzle_post,
            self.test_puzzle_put,
            self.test_puzzle_get_with_params,
            self.test_user_achievement_post,
            self.test_user_delete
        ]
        
        results = []
        for test_func in tests:
            try:
                result = test_func()
                results.append(result)
                self.test_results.append(result)
            except Exception as e:
                print(f"❌ Test {test_func.__name__} failed with error: {e}")
                results.append({
                    "endpoint": test_func.__name__,
                    "status_code": 0,
                    "success": False,
                    "error": str(e)
                })
        
        self.print_summary(results)
        self.save_results(results)
        
        return results
    
    def print_summary(self, results: List[Dict[str, Any]]):
        """Print test summary."""
        print("\n" + "=" * 50)
        print("🔍 FOCUSED TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.get("success", False))
        
        print(f"Total tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
        
        print("\n📋 Detailed Results:")
        for result in results:
            status = "✅" if result.get("success", False) else "❌"
            endpoint = result.get("endpoint", "Unknown")
            status_code = result.get("status_code", 0)
            error = result.get("error", "")
            
            print(f"{status} {endpoint} - {status_code}")
            if error and not result.get("success", False):
                print(f"    Error: {error}")
    
    def save_results(self, results: List[Dict[str, Any]]):
        """Save test results to file."""
        output_path = os.path.join(os.path.dirname(__file__), "focused_test_results.json")
        
        output_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": len(results),
            "successful_tests": sum(1 for r in results if r.get("success", False)),
            "results": results
        }
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {output_path}")


if __name__ == "__main__":
    tester = FocusedEndpointTester()
    tester.run_all_tests()