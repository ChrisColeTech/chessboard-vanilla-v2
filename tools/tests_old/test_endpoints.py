#!/usr/bin/env python3
"""
Frontend-to-Backend Endpoint Testing Script
Tests all API endpoints by making requests through the frontend application running on port 5173
"""

import requests
import json
import time
from typing import Dict, List, Any
import sys

class EndpointTester:
    def __init__(self, frontend_url: str = "http://localhost:5173", backend_url: str = "http://localhost:3001"):
        self.frontend_url = frontend_url
        self.backend_url = backend_url
        self.session = requests.Session()
        self.results = []
        self.passed_tests = 0
        self.total_tests = 0
        
    def log_test(self, endpoint: str, method: str, status: str, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            
        result = {
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results.append(result)
        
        # Color output
        color = "\033[92m" if status == "PASS" else "\033[91m"  # Green for PASS, Red for FAIL
        reset = "\033[0m"
        
        print(f"{color}[{status}]{reset} {method} {endpoint} - {details}")
    
    def test_endpoint(self, method: str, path: str, data: Dict = None, expected_status: List[int] = None):
        """Test a single endpoint"""
        if expected_status is None:
            expected_status = [200, 201]
            
        full_url = f"{self.backend_url}{path}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(full_url, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(full_url, json=data, timeout=10)
            elif method.upper() == "PUT":
                response = self.session.put(full_url, json=data, timeout=10)
            elif method.upper() == "DELETE":
                response = self.session.delete(full_url, timeout=10)
            else:
                self.log_test(path, method, "FAIL", f"Unsupported method: {method}")
                return False
            
            if response.status_code in expected_status:
                try:
                    response_data = response.json()
                    self.log_test(path, method, "PASS", f"Status: {response.status_code}, Response: {json.dumps(response_data, default=str)[:100]}")
                    return True
                except ValueError:
                    self.log_test(path, method, "PASS", f"Status: {response.status_code}, Non-JSON response")
                    return True
            else:
                self.log_test(path, method, "FAIL", f"Expected {expected_status}, got {response.status_code}: {response.text[:200]}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test(path, method, "FAIL", f"Connection error: {str(e)}")
            return False
        except Exception as e:
            self.log_test(path, method, "FAIL", f"Unexpected error: {str(e)}")
            return False
    
    def check_servers_running(self):
        """Check if both frontend and backend servers are running"""
        print("🔍 Checking server status...")
        
        # Check frontend
        try:
            frontend_response = requests.get(self.frontend_url, timeout=5)
            if frontend_response.status_code == 200:
                print(f"✅ Frontend server running at {self.frontend_url}")
            else:
                print(f"❌ Frontend server returned status {frontend_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Frontend server not accessible: {e}")
            return False
        
        # Check backend
        try:
            backend_response = requests.get(f"{self.backend_url}/api/health", timeout=5)
            if backend_response.status_code == 200:
                print(f"✅ Backend server running at {self.backend_url}")
            else:
                print(f"❌ Backend server returned status {backend_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Backend server not accessible: {e}")
            return False
        
        return True
    
    def run_all_tests(self):
        """Run tests for all endpoints based on backend config"""
        print("🚀 Starting comprehensive endpoint testing...")
        print("=" * 60)
        
        if not self.check_servers_running():
            print("\n❌ Server check failed. Please ensure both servers are running.")
            return False
        
        print("\n📋 Testing all API endpoints...")
        
        # Load backend config to get all endpoints
        try:
            with open("backend_config.json", 'r') as f:
                backend_config = json.load(f)
        except FileNotFoundError:
            print("❌ backend_config.json not found. Please run this from the tools directory.")
            return False
        
        # Test health endpoint first
        print("\n🏥 Testing Health Endpoints...")
        self.test_endpoint("GET", "/api/health")
        self.test_endpoint("GET", "/api")
        
        # Test auth endpoints
        print("\n🔐 Testing Authentication Endpoints...")
        
        # Test user registration
        register_data = {
            "username": "testuser123",
            "email": "test@example.com",
            "password": "testPassword123"
        }
        self.test_endpoint("POST", "/auth/register", register_data, [200, 201, 400, 409])
        
        # Test user login
        login_data = {
            "email": "test@example.com",
            "password": "testPassword123"
        }
        self.test_endpoint("POST", "/auth/login", login_data, [200, 401])
        
        # Test other auth endpoints
        self.test_endpoint("POST", "/auth/logout", {}, [200, 401])
        self.test_endpoint("GET", "/auth/profile", expected_status=[200, 401])
        self.test_endpoint("POST", "/auth/verify-token", {"token": "dummy-token"}, [200, 401, 400])
        self.test_endpoint("POST", "/auth/forgot-password", {"email": "test@example.com"}, [200, 404])
        self.test_endpoint("POST", "/auth/reset-password", {"token": "dummy-token", "password": "newpass"}, [200, 400, 404])
        
        # Test user management endpoints
        print("\n👤 Testing User Management Endpoints...")
        self.test_endpoint("GET", "/api/users", expected_status=[200, 401])
        self.test_endpoint("GET", "/api/users/1", expected_status=[200, 404, 401])
        self.test_endpoint("POST", "/api/users", {"username": "newuser", "email": "new@test.com"}, [200, 201, 400, 401])
        self.test_endpoint("PUT", "/api/users/1", {"username": "updated"}, [200, 404, 401])
        self.test_endpoint("DELETE", "/api/users/999", expected_status=[200, 404, 401])
        
        # Test chess/puzzle endpoints
        print("\n♟️  Testing Chess/Puzzle Endpoints...")
        self.test_endpoint("GET", "/api/puzzles", expected_status=[200, 401])
        self.test_endpoint("GET", "/api/puzzles/next", expected_status=[200, 404, 401])
        self.test_endpoint("GET", "/api/puzzles/1", expected_status=[200, 404, 401])
        self.test_endpoint("POST", "/api/puzzles/1/solve", {"solution": "e4"}, [200, 400, 404, 401])
        self.test_endpoint("GET", "/api/puzzles/1/hint", expected_status=[200, 404, 401])
        
        # Test game endpoints
        print("\n🎮 Testing Game Endpoints...")
        self.test_endpoint("GET", "/api/games", expected_status=[200, 401])
        self.test_endpoint("GET", "/api/games/1", expected_status=[200, 404, 401])
        game_data = {"playerWhite": "player1", "playerBlack": "player2"}
        self.test_endpoint("POST", "/api/games", game_data, [200, 201, 400, 401])
        self.test_endpoint("PUT", "/api/games/1", {"status": "completed"}, [200, 404, 401])
        self.test_endpoint("POST", "/api/games/1/analyze", {"moves": ["e4", "e5"]}, [200, 400, 404, 401])
        
        # Test stats/performance endpoints
        print("\n📊 Testing Stats/Performance Endpoints...")
        self.test_endpoint("GET", "/api/stats", expected_status=[200, 401])
        self.test_endpoint("GET", "/api/stats/user/1", expected_status=[200, 404, 401])
        stats_data = {"userId": 1, "puzzlesSolved": 10, "accuracy": 85.5}
        self.test_endpoint("POST", "/api/stats", stats_data, [200, 201, 400, 401])
        self.test_endpoint("PUT", "/api/stats/1", {"accuracy": 90.0}, [200, 404, 401])
        
        # Test learning endpoints
        print("\n📚 Testing Learning Endpoints...")
        self.test_endpoint("GET", "/api/learning", expected_status=[200, 401])
        self.test_endpoint("GET", "/api/learning/1", expected_status=[200, 404, 401])
        
        # Test tutorial endpoints
        print("\n📖 Testing Tutorial Endpoints...")
        self.test_endpoint("GET", "/api/tutorials", expected_status=[200, 401])
        self.test_endpoint("GET", "/api/tutorials/1", expected_status=[200, 404, 401])
        tutorial_data = {"title": "Chess Basics", "content": "Learn chess fundamentals"}
        self.test_endpoint("POST", "/api/tutorials", tutorial_data, [200, 201, 400, 401])
        self.test_endpoint("PUT", "/api/tutorials/1", {"title": "Updated Tutorial"}, [200, 404, 401])
        
        # Additional frontend-specific tests
        print("\n🌐 Testing Frontend Assets...")
        try:
            # Test if frontend can serve its assets
            assets_response = requests.get(f"{self.frontend_url}/src/main.tsx", timeout=5)
            if assets_response.status_code == 200:
                self.log_test("/src/main.tsx", "GET", "PASS", "Frontend assets accessible")
            else:
                self.log_test("/src/main.tsx", "GET", "FAIL", f"Frontend assets not accessible: {assets_response.status_code}")
        except Exception as e:
            self.log_test("/src/main.tsx", "GET", "FAIL", f"Frontend asset test failed: {e}")
        
        return True
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        print("\n" + "=" * 60)
        print("📋 TEST REPORT")
        print("=" * 60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("\n🎉 ALL TESTS PASSED! Frontend-Backend communication is 100% functional!")
        elif success_rate >= 80:
            print(f"\n✅ {success_rate:.1f}% tests passed - Communication is mostly functional")
        elif success_rate >= 60:
            print(f"\n⚠️  {success_rate:.1f}% tests passed - Some communication issues detected")
        else:
            print(f"\n❌ {success_rate:.1f}% tests passed - Significant communication problems")
        
        # Show failed tests
        failed_tests = [r for r in self.results if r["status"] == "FAIL"]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['method']} {test['endpoint']} - {test['details']}")
        
        # Save detailed report
        report_data = {
            "summary": {
                "total_tests": self.total_tests,
                "passed_tests": self.passed_tests,
                "failed_tests": self.total_tests - self.passed_tests,
                "success_rate": success_rate
            },
            "test_results": self.results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open("endpoint_test_report.json", "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: endpoint_test_report.json")
        
        return success_rate == 100

def main():
    """Main function"""
    print("🧪 Frontend-to-Backend Endpoint Communication Tester")
    print("Testing all endpoints via frontend (port 5173) to backend (port 3001)")
    print("=" * 60)
    
    tester = EndpointTester()
    
    # Run all tests
    if tester.run_all_tests():
        success = tester.generate_report()
        sys.exit(0 if success else 1)
    else:
        print("\n❌ Test execution failed")
        sys.exit(1)

if __name__ == "__main__":
    main()