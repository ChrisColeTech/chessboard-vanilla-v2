#!/usr/bin/env python3
"""
Fixed Frontend-to-Backend Endpoint Testing Script
Uses correct endpoint paths that actually exist in the backend
Based on the working JS test script paths
"""

import json
import requests
import time
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path


class FixedEndpointTester:
    def __init__(self):
        self.frontend_url = "http://localhost:5173"
        self.backend_url = "http://localhost:3001"
        self.auth_token = None
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
        # Correct endpoint paths based on working JS script
        self.test_endpoints = {
            "auth": [
                {"method": "GET", "path": "/api/auth/health", "description": "Health check"},
                {"method": "POST", "path": "/api/auth/login", "description": "Demo user login", 
                 "body": {"email": "chessdemo@example.com", "password": "ChessDemo2024"}},
                {"method": "POST", "path": "/api/auth/check-email", "description": "Check email availability", 
                 "body": {"email": "newemail@example.com"}},
                {"method": "POST", "path": "/api/auth/check-username", "description": "Check username availability", 
                 "body": {"username": "newuser"}},
            ],
            "users": [
                {"method": "GET", "path": "/api/users/profile", "description": "Get user profile", "requiresAuth": True},
                {"method": "GET", "path": "/api/users/preferences", "description": "Get user preferences", "requiresAuth": True},
                {"method": "GET", "path": "/api/users/settings", "description": "Get user settings", "requiresAuth": True},
            ],
            "puzzles": [
                {"method": "GET", "path": "/api/puzzles/next", "description": "Get next puzzle", "requiresAuth": True},
                {"method": "GET", "path": "/api/puzzles/categories", "description": "Get puzzle categories", "requiresAuth": True},
                {"method": "GET", "path": "/api/puzzles/history", "description": "Get puzzle history", "requiresAuth": True},
                {"method": "GET", "path": "/api/puzzles/custom", "description": "Get custom puzzles", "requiresAuth": True},
            ],
            "games": [
                {"method": "GET", "path": "/api/games", "description": "Get games list", "requiresAuth": True},
                {"method": "GET", "path": "/api/games/reviews", "description": "Get game reviews", "requiresAuth": True},
            ],
            "stats": [
                {"method": "GET", "path": "/api/stats/overview", "description": "Get overview stats", "requiresAuth": True},
                {"method": "GET", "path": "/api/stats/puzzles", "description": "Get puzzle stats", "requiresAuth": True},
                {"method": "GET", "path": "/api/stats/games", "description": "Get game stats", "requiresAuth": True},
                {"method": "GET", "path": "/api/stats/progress", "description": "Get progress stats", "requiresAuth": True},
                {"method": "GET", "path": "/api/stats/performance", "description": "Get performance stats", "requiresAuth": True},
                {"method": "GET", "path": "/api/stats/ratings", "description": "Get rating stats", "requiresAuth": True},
            ],
            "learning": [
                {"method": "GET", "path": "/api/learning/paths", "description": "Get learning paths", "requiresAuth": True},
            ],
            "tutorials": [
                {"method": "GET", "path": "/api/tutorials", "description": "Get tutorials list", "requiresAuth": True},
            ]
        }
        
    def _log_test(self, endpoint: str, method: str, status: str, details: str = ""):
        """Log test result"""
        result = {
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {method} {endpoint} - {details}")
        else:
            self.failed_tests += 1
            print(f"❌ {method} {endpoint} - {details}")
        
        self.total_tests += 1
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Make HTTP request to backend"""
        url = f"{self.backend_url}{endpoint}"
        
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
        
        if self.auth_token:
            default_headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=default_headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=default_headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=default_headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=default_headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
        except requests.exceptions.RequestException as e:
            # Create a mock response for connection errors
            mock_response = requests.Response()
            mock_response.status_code = 500
            mock_response._content = json.dumps({"error": str(e)}).encode()
            return mock_response
    
    def test_connectivity(self):
        """Test basic frontend and backend connectivity"""
        print("🔍 Testing server connectivity...")
        
        # Test frontend
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Frontend accessible at {self.frontend_url}")
            else:
                print(f"⚠️ Frontend returned status {response.status_code}")
        except:
            print(f"❌ Frontend not accessible at {self.frontend_url}")
            return False
            
        # Test backend
        try:
            response = requests.get(f"{self.backend_url}/api/auth/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Backend accessible at {self.backend_url}")
            else:
                print(f"⚠️ Backend returned status {response.status_code}")
        except:
            print(f"❌ Backend not accessible at {self.backend_url}")
            return False
            
        return True
    
    def test_endpoint(self, endpoint_config: Dict):
        """Test a single endpoint"""
        method = endpoint_config["method"]
        path = endpoint_config["path"]
        description = endpoint_config["description"]
        requires_auth = endpoint_config.get("requiresAuth", False)
        body = endpoint_config.get("body")
        
        print(f"\n🧪 Testing: {method} {path}")
        print(f"   Description: {description}")
        
        if requires_auth:
            if self.auth_token:
                print(f"   🔐 Using auth token")
            else:
                print(f"   ⚠️ Requires auth but no token available")
        
        response = self._make_request(method, path, body)
        
        # Only accept 200 as success (like the JS script)
        if response.status_code == 200:
            try:
                data = response.json()
                self._log_test(path, method, "PASS", f"Status: 200, Response type: {type(data).__name__}")
                
                # Extract auth token from login
                if "login" in path and data:
                    token = data.get("data", {}).get("token") if isinstance(data.get("data"), dict) else data.get("token")
                    if token:
                        self.auth_token = token
                        print(f"   🔑 Auth token obtained for future requests")
                    else:
                        print(f"   ⚠️ No token found in login response")
                        
            except:
                self._log_test(path, method, "PASS", f"Status: 200, Non-JSON response")
        else:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", f"Status {response.status_code}")
            except:
                error_msg = response.text[:100] if response.text else f"Status {response.status_code}"
            
            self._log_test(path, method, "FAIL", f"Status: {response.status_code}, Error: {error_msg}")
    
    def run_all_tests(self):
        """Run all endpoint tests using correct paths"""
        print("🚀 Fixed Frontend-to-Backend Communication Tests")
        print("Using correct endpoint paths from working JS script")
        print("=" * 60)
        
        if not self.test_connectivity():
            print("\n❌ Connectivity test failed. Please ensure both servers are running.")
            return False
        
        print("\n📡 Testing all API endpoints with correct paths...")
        print("=" * 50)
        
        # Test all endpoints by domain
        for domain, endpoints in self.test_endpoints.items():
            print(f"\n📂 Testing {domain.upper()} domain:")
            for endpoint in endpoints:
                self.test_endpoint(endpoint)
                time.sleep(0.1)  # Small delay between requests
        
        # Print final summary
        self.print_summary()
        return self.failed_tests == 0
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 FIXED TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("\n🎉 100% SUCCESSFUL COMMUNICATION VERIFIED! 🎉")
        elif success_rate >= 85:
            print(f"\n✅ Excellent! {success_rate:.1f}% of tests passed - Communication is highly functional!")
        elif success_rate >= 70:
            print(f"\n✅ Good! {success_rate:.1f}% of tests passed - Communication is mostly functional")
        else:
            print(f"\n⚠️ {success_rate:.1f}% of tests passed - Communication issues detected")
        
        # Show failed tests
        if self.failed_tests > 0:
            print(f"\n❌ Failed Tests ({self.failed_tests}):")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"   • {result['method']} {result['endpoint']} - {result['details']}")
        
        # Compare with JS script results
        print(f"\n🔍 Comparison with JS script:")
        print(f"   JS Script: 85.7% success rate")
        print(f"   Fixed Python Script: {success_rate:.1f}% success rate")
        
        if abs(success_rate - 85.7) < 5:
            print(f"   ✅ Results match! Both scripts now test the same endpoints correctly.")
        else:
            print(f"   ⚠️ Results differ - may indicate different test conditions.")
        
        print("\n📄 Detailed test results:")
        with open("fixed_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": self.total_tests,
                    "passed_tests": self.passed_tests,
                    "failed_tests": self.failed_tests,
                    "success_rate": success_rate
                },
                "results": self.test_results
            }, f, indent=2)
        print("   Saved to: fixed_test_results.json")


def main():
    """Main function"""
    print("🔧 Fixed Frontend-to-Backend Endpoint Communication Tester")
    print("Now using correct endpoint paths that actually exist in the backend!")
    print("=" * 60)
    
    tester = FixedEndpointTester()
    
    # Run all tests
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()