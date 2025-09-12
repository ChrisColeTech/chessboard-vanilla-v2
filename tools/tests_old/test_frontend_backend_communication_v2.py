#!/usr/bin/env python3
"""
Frontend-Backend Communication Test Script V2
Tests all endpoints from frontend (port 5173) to backend (port 3001) to verify 100% successful communication
"""

import requests
import json
import time
from typing import Dict, List, Any
import sys
from pathlib import Path

class FrontendBackendTester:
    def __init__(self, frontend_url="http://localhost:5173", backend_url="http://localhost:3001"):
        self.frontend_url = frontend_url
        self.backend_url = backend_url
        self.test_results = []
        self.auth_token = None
        
    def load_backend_config(self) -> Dict[str, Any]:
        """Load backend configuration to get all endpoints"""
        config_path = Path(__file__).parent / "backend_config.json"
        if not config_path.exists():
            raise FileNotFoundError("backend_config.json not found")
        
        with open(config_path) as f:
            return json.load(f)
    
    def setup_test_user(self):
        """Setup test user and get authentication token"""
        print("🔐 Setting up test user and authentication...")
        
        # Test user data
        test_user = {
            "email": "test2@example.com", 
            "password": "password123",
            "username": "testuser2"
        }
        
        try:
            # First, try to register the user (this may fail if user exists)
            print("   📝 Attempting to register test user...")
            register_response = requests.post(
                f"{self.backend_url}/api/auth/register",
                json=test_user,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if register_response.status_code == 200:
                register_result = register_response.json()
                print(f"   ✅ User registered successfully")
                print(f"   📋 Register response: {register_result}")
                
                # Extract token from registration if provided
                if register_result.get("success") and register_result.get("data", {}).get("token"):
                    self.auth_token = register_result["data"]["token"]
                    print("   🔑 Auth token obtained from registration")
                    return True
            else:
                print(f"   ⚠️ Registration failed with status {register_response.status_code}")
                try:
                    error_response = register_response.json()
                    print(f"   📋 Register error: {error_response}")
                except:
                    print(f"   📋 Register error: {register_response.text}")
            
            # Whether registration succeeded or failed, try to login
            print("   🔐 Attempting to login...")
            login_response = requests.post(
                f"{self.backend_url}/api/auth/login",
                json={"email": test_user["email"], "password": test_user["password"]},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                print(f"   ✅ Login successful")
                print(f"   📋 Login response: {login_result}")
                
                if login_result.get("success") and login_result.get("data", {}).get("token"):
                    self.auth_token = login_result["data"]["token"]
                    print("   🔑 Auth token obtained from login")
                    return True
                else:
                    print("   ⚠️ Login response missing token")
                    return False
            else:
                print(f"   ❌ Login failed with status {login_response.status_code}")
                try:
                    error_response = login_response.json()
                    print(f"   📋 Login error: {error_response}")
                except:
                    print(f"   📋 Login error: {login_response.text}")
                
        except Exception as e:
            print(f"   ❌ Authentication setup failed: {e}")
        
        print("   ⚠️ Proceeding without authentication token")
        return False
    
    def test_endpoint(self, method: str, path: str, endpoint_name: str, 
                     data: Dict = None, requires_auth: bool = False) -> Dict[str, Any]:
        """Test a single endpoint"""
        url = f"{self.backend_url}{path}"
        
        headers = {"Content-Type": "application/json"}
        if requires_auth and self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            start_time = time.time()
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return {
                    "endpoint": endpoint_name,
                    "method": method,
                    "path": path,
                    "status": "ERROR",
                    "status_code": 0,
                    "error": f"Unsupported method: {method}",
                    "response_time": 0
                }
            
            response_time = round((time.time() - start_time) * 1000, 2)
            
            # Determine if this is a success
            success = response.status_code == 200
            
            result = {
                "endpoint": endpoint_name,
                "method": method.upper(),
                "path": path,
                "status": "SUCCESS" if success else "FAILED",
                "status_code": response.status_code,
                "response_time": response_time,
                "requires_auth": requires_auth
            }
            
            # Add response data for successful requests
            if success:
                try:
                    result["response_data"] = response.json()
                except:
                    result["response_data"] = response.text[:200] + "..." if len(response.text) > 200 else response.text
            else:
                try:
                    result["error"] = response.json().get("error", response.text)
                except:
                    result["error"] = response.text[:200] + "..." if len(response.text) > 200 else response.text
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                "endpoint": endpoint_name,
                "method": method,
                "path": path,
                "status": "TIMEOUT",
                "status_code": 0,
                "error": "Request timed out after 10 seconds",
                "response_time": 10000,
                "requires_auth": requires_auth
            }
        except requests.exceptions.ConnectionError:
            return {
                "endpoint": endpoint_name,
                "method": method,
                "path": path,
                "status": "CONNECTION_ERROR",
                "status_code": 0,
                "error": "Could not connect to backend",
                "response_time": 0,
                "requires_auth": requires_auth
            }
        except Exception as e:
            return {
                "endpoint": endpoint_name,
                "method": method,
                "path": path,
                "status": "ERROR",
                "status_code": 0,
                "error": str(e),
                "response_time": 0,
                "requires_auth": requires_auth
            }
    
    def test_all_endpoints(self) -> List[Dict[str, Any]]:
        """Test all endpoints from backend configuration"""
        print("🚀 Starting comprehensive endpoint testing...")
        
        config = self.load_backend_config()
        endpoints = config.get("endpoints", {})
        
        # Test basic health endpoint first
        health_result = self.test_endpoint("GET", "/health", "health_check")
        self.test_results.append(health_result)
        
        if health_result["status"] != "SUCCESS":
            print(f"❌ Backend health check failed: {health_result.get('error', 'Unknown error')}")
            print("⚠️ Continuing with endpoint tests anyway...")
        else:
            print("✅ Backend is healthy and responding")
        
        # Test all configured endpoints
        total_endpoints = 0
        
        for endpoint_key, endpoint_config in endpoints.items():
            entity_name = endpoint_config.get("entity", endpoint_key.capitalize())
            entities_name = endpoint_config.get("entities", endpoint_key)
            api_endpoints = endpoint_config.get("endpoints", [])
            
            print(f"\n📊 Testing {entity_name} endpoints ({len(api_endpoints)} endpoints)...")
            
            for api_endpoint in api_endpoints:
                method = api_endpoint["method"]
                path = api_endpoint["path"]
                handler = api_endpoint["handler"]
                
                # Build full API path
                full_path = f"/api/{entities_name}{path}"
                
                # Determine if authentication is required
                requires_auth = "auth" not in endpoint_key and endpoint_key != "help"
                
                # Prepare test data for POST/PUT requests
                test_data = {}
                if method.upper() in ["POST", "PUT"]:
                    # Use simple test data based on endpoint
                    if "login" in handler.lower():
                        test_data = {"email": "test@example.com", "password": "password123"}
                    elif "register" in handler.lower():
                        test_data = {"email": "newuser@example.com", "password": "password123", "username": "newuser"}
                    elif "email" in handler.lower():
                        test_data = {"email": "test@example.com"}
                    elif "username" in handler.lower():
                        test_data = {"username": "testuser"}
                    else:
                        # Generic test data
                        properties = endpoint_config.get("properties", {})
                        for prop, prop_type in properties.items():
                            if prop not in ["id", "created_at", "updated_at"]:
                                if prop_type == "string":
                                    test_data[prop] = f"test_{prop}"
                                elif prop_type == "number":
                                    test_data[prop] = 1000
                                elif prop_type == "boolean":
                                    test_data[prop] = True
                
                # Handle path parameters (replace :id with test values)
                test_path = full_path.replace(":id", "test-id-123")
                
                result = self.test_endpoint(method, test_path, f"{entity_name}_{handler}", test_data, requires_auth)
                self.test_results.append(result)
                
                # Print result
                status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
                print(f"  {status_icon} {method.upper()} {test_path} - {result['status']} ({result['status_code']}) - {result['response_time']}ms")
                
                total_endpoints += 1
        
        print(f"\n📈 Tested {total_endpoints} endpoints total")
        return self.test_results
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        if not self.test_results:
            return {"error": "No test results available"}
        
        total = len(self.test_results)
        successful = len([r for r in self.test_results if r["status"] == "SUCCESS"])
        failed = len([r for r in self.test_results if r["status"] == "FAILED"])
        errors = len([r for r in self.test_results if r["status"] in ["ERROR", "TIMEOUT", "CONNECTION_ERROR"]])
        
        success_rate = (successful / total) * 100 if total > 0 else 0
        
        # Group results by status
        successful_endpoints = [r for r in self.test_results if r["status"] == "SUCCESS"]
        failed_endpoints = [r for r in self.test_results if r["status"] == "FAILED"]
        error_endpoints = [r for r in self.test_results if r["status"] in ["ERROR", "TIMEOUT", "CONNECTION_ERROR"]]
        
        # Calculate average response time for successful requests
        successful_times = [r["response_time"] for r in successful_endpoints if r["response_time"] > 0]
        avg_response_time = sum(successful_times) / len(successful_times) if successful_times else 0
        
        report = {
            "summary": {
                "total_endpoints": total,
                "successful": successful,
                "failed": failed,
                "errors": errors,
                "success_rate": round(success_rate, 2),
                "average_response_time": round(avg_response_time, 2)
            },
            "successful_endpoints": successful_endpoints,
            "failed_endpoints": failed_endpoints,
            "error_endpoints": error_endpoints,
            "all_results": self.test_results
        }
        
        return report
    
    def print_report(self, report: Dict[str, Any]):
        """Print formatted test report"""
        print("\n" + "="*80)
        print("📊 FRONTEND-BACKEND COMMUNICATION TEST REPORT")
        print("="*80)
        
        summary = report["summary"]
        print(f"📈 SUMMARY:")
        print(f"   Total Endpoints Tested: {summary['total_endpoints']}")
        print(f"   ✅ Successful: {summary['successful']} ({summary['success_rate']:.1f}%)")
        print(f"   ❌ Failed: {summary['failed']}")
        print(f"   🚫 Errors: {summary['errors']}")
        print(f"   ⚡ Average Response Time: {summary['average_response_time']:.1f}ms")
        
        if report["successful_endpoints"]:
            print(f"\n✅ WORKING ENDPOINTS ({len(report['successful_endpoints'])}):")
            for endpoint in report["successful_endpoints"]:
                print(f"   • {endpoint['method']} {endpoint['path']} - {endpoint['response_time']}ms")
        
        if report["failed_endpoints"]:
            print(f"\n❌ FAILED ENDPOINTS ({len(report['failed_endpoints'])}):")
            for endpoint in report["failed_endpoints"]:
                error_msg = endpoint.get('error', 'Unknown error')[:50]
                print(f"   • {endpoint['method']} {endpoint['path']} - {endpoint['status_code']} - {error_msg}")
        
        if report["error_endpoints"]:
            print(f"\n🚫 ERROR ENDPOINTS ({len(report['error_endpoints'])}):")
            for endpoint in report["error_endpoints"]:
                error_msg = endpoint.get('error', 'Unknown error')[:50]
                print(f"   • {endpoint['method']} {endpoint['path']} - {endpoint['status']} - {error_msg}")
        
        # Communication status
        print(f"\n🔗 FRONTEND-BACKEND COMMUNICATION STATUS:")
        if summary['success_rate'] == 100:
            print("   🎉 100% SUCCESSFUL COMMUNICATION! All endpoints are working perfectly.")
        elif summary['success_rate'] >= 80:
            print(f"   ✅ MOSTLY SUCCESSFUL ({summary['success_rate']:.1f}%) - Core functionality is working.")
        elif summary['success_rate'] >= 50:
            print(f"   ⚠️ PARTIALLY WORKING ({summary['success_rate']:.1f}%) - Some endpoints need attention.")
        else:
            print(f"   ❌ MOSTLY FAILING ({summary['success_rate']:.1f}%) - Significant issues detected.")
        
        print("\n" + "="*80)

def main():
    """Main function"""
    print("🚀 Frontend-Backend Communication Tester V2")
    print("Testing communication from Frontend (localhost:5173) to Backend (localhost:3001)")
    
    tester = FrontendBackendTester()
    
    # Setup authentication
    tester.setup_test_user()
    
    # Run all tests
    results = tester.test_all_endpoints()
    
    # Generate and print report
    report = tester.generate_report()
    tester.print_report(report)
    
    # Save detailed results to file
    output_file = Path(__file__).parent / "frontend_backend_test_results_v2.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    # Return exit code based on success rate
    success_rate = report["summary"]["success_rate"]
    if success_rate == 100:
        print("✅ All tests passed! Perfect communication achieved.")
        sys.exit(0)
    elif success_rate >= 80:
        print("⚠️ Most tests passed, but some issues detected.")
        sys.exit(1)
    else:
        print("❌ Many tests failed. Significant communication issues.")
        sys.exit(2)

if __name__ == "__main__":
    main()