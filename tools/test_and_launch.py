#!/usr/bin/env python3
"""
Frontend/Backend Integration Test and Launch Script
Tests all API endpoints, then launches both frontend and backend for full integration testing
"""

import json
import requests
import subprocess
import time
import os
import signal
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import threading
import queue

class EndpointTester:
    def __init__(self, base_url: str = "http://localhost:3001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_id = None
        
    def log(self, message: str, level: str = "INFO"):
        """Centralized logging with color coding"""
        colors = {
            "INFO": "\033[94m",  # Blue
            "SUCCESS": "\033[92m",  # Green
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",  # Red
            "RESET": "\033[0m"
        }
        color = colors.get(level, colors["INFO"])
        print(f"{color}[{level}] {message}{colors['RESET']}")
    
    def wait_for_service(self, url: str, timeout: int = 30) -> bool:
        """Wait for a service to be available"""
        self.log(f"Waiting for service at {url}...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    self.log(f"Service at {url} is ready!", "SUCCESS")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(2)
        
        self.log(f"Service at {url} failed to start within {timeout} seconds", "ERROR")
        return False
    
    def test_endpoint(self, method: str, path: str, handler: str, 
                     auth_required: bool = False, test_data: Dict = None) -> Dict:
        """Test a single endpoint"""
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json"}
        
        if auth_required and self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, headers=headers, json=test_data or {})
            elif method.upper() == "PUT":
                response = self.session.put(url, headers=headers, json=test_data or {})
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                return {"success": False, "error": f"Unsupported method: {method}"}
            
            success = response.status_code < 400
            result = {
                "success": success,
                "status_code": response.status_code,
                "handler": handler,
                "method": method,
                "path": path
            }
            
            try:
                result["data"] = response.json()
            except:
                result["data"] = response.text
            
            if success:
                self.log(f"✓ {method} {path} ({handler}) - {response.status_code}", "SUCCESS")
            else:
                self.log(f"✗ {method} {path} ({handler}) - {response.status_code}", "ERROR")
                
            return result
            
        except Exception as e:
            self.log(f"✗ {method} {path} ({handler}) - Exception: {str(e)}", "ERROR")
            return {"success": False, "error": str(e), "handler": handler, "method": method, "path": path}
    
    def setup_test_user(self) -> bool:
        """Register and login a test user"""
        self.log("Setting up test user...")
        
        # Register test user
        register_data = {
            "username": "testuser123",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        
        register_result = self.test_endpoint("POST", "/auth/register", "register", 
                                           auth_required=False, test_data=register_data)
        
        if not register_result["success"] and register_result.get("status_code") != 409:
            self.log("Failed to register test user", "ERROR")
            return False
        
        # Login test user
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        
        login_result = self.test_endpoint("POST", "/auth/login", "login", 
                                        auth_required=False, test_data=login_data)
        
        if login_result["success"] and "data" in login_result:
            data = login_result["data"]
            if isinstance(data, dict) and "token" in data:
                self.auth_token = data["token"]
                self.test_user_id = data.get("user", {}).get("id")
                self.log("Test user authenticated successfully", "SUCCESS")
                return True
        
        self.log("Failed to authenticate test user", "ERROR")
        return False
    
    def get_test_data(self, endpoint_name: str, handler: str) -> Optional[Dict]:
        """Generate appropriate test data for endpoints"""
        test_data_map = {
            # Auth endpoints
            "register": {
                "username": "newuser123",
                "email": "newuser@example.com", 
                "password": "NewPassword123!"
            },
            "login": {
                "email": "test@example.com",
                "password": "TestPassword123!"
            },
            "updateProfile": {
                "username": "updateduser",
                "preferences": {"theme": "dark", "notifications": True}
            },
            "changePassword": {
                "currentPassword": "TestPassword123!",
                "newPassword": "NewTestPassword123!"
            },
            "verifyToken": {
                "token": self.auth_token
            },
            "forgotPassword": {
                "email": "test@example.com"
            },
            "resetPassword": {
                "token": "reset_token_123",
                "password": "ResetPassword123!"
            },
            "checkEmailAvailability": {
                "email": "check@example.com"
            },
            "checkUsernameAvailability": {
                "username": "checkuser"
            },
            
            # Users endpoints
            "updateUserProfile": {
                "username": "updateduser",
                "chess_elo": 1500
            },
            "updateUserPreferences": {
                "theme": "dark",
                "notifications": True,
                "sound": False
            },
            "updateUserSettings": {
                "language": "en",
                "timezone": "UTC"
            },
            
            # Puzzles endpoints
            "solvePuzzle": {
                "moves": ["e2e4", "e7e5"],
                "time_taken": 30
            },
            "createCustomPuzzle": {
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "solution_moves": "e2e4,e7e5",
                "themes": "tactics,pins",
                "description": "Basic opening puzzle"
            },
            
            # Games endpoints
            "createGame": {
                "ai_level": 3,
                "user_color": "white",
                "time_control": "10+5"
            },
            "updateGame": {
                "current_fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
                "pgn": "1. e4",
                "status": "active"
            },
            "analyzeGame": {
                "depth": 15,
                "engine": "stockfish"
            },
            
            # Learning endpoints
            "enrollInPath": {
                "enrollment_date": "2024-01-01"
            },
            "updateProgress": {
                "progress": 75,
                "completed_modules": ["intro", "basics"]
            },
            
            # Tutorial endpoints
            "completeTutorial": {
                "completion_time": 300,
                "score": 85
            }
        }
        
        return test_data_map.get(handler)
    
    def test_all_endpoints(self, config_path: str = "backend_config.json") -> Dict:
        """Test all endpoints from config"""
        self.log("Starting comprehensive endpoint testing...")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        # Setup test user first
        if not self.setup_test_user():
            self.log("Failed to setup test user, some tests may fail", "WARNING")
        
        # Test endpoints by domain
        for endpoint_name, endpoint_config in config["endpoints"].items():
            domain_results = {"domain": endpoint_name, "tests": []}
            
            for endpoint in endpoint_config.get("endpoints", []):
                method = endpoint["method"]
                path = endpoint["path"]
                handler = endpoint["handler"]
                auth_required = endpoint.get("auth_required", True)
                
                # Build full path
                if endpoint_name == "auth":
                    full_path = f"/auth{path}"
                else:
                    full_path = f"/api/{endpoint_config.get('entities', endpoint_name)}{path}"
                
                # Replace path parameters with test values
                if ":id" in full_path:
                    test_id = "test-id-123"
                    if endpoint_name == "puzzles" and handler in ["solvePuzzle", "getPuzzleHint"]:
                        test_id = "puzzle-1"
                    elif endpoint_name == "games":
                        test_id = "game-1"
                    elif endpoint_name == "learning" and "paths" in full_path:
                        test_id = "path-1"
                    elif endpoint_name == "tutorials":
                        test_id = "tutorial-1"
                    
                    full_path = full_path.replace(":id", test_id)
                
                # Get test data
                test_data = self.get_test_data(endpoint_name, handler)
                
                # Test the endpoint
                result = self.test_endpoint(method, full_path, handler, auth_required, test_data)
                
                domain_results["tests"].append(result)
                results["total_tests"] += 1
                
                if result["success"]:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
            
            results["details"].append(domain_results)
        
        # Print summary
        self.log(f"\n📊 Test Summary:", "INFO")
        self.log(f"Total Tests: {results['total_tests']}", "INFO")
        self.log(f"Passed: {results['passed']}", "SUCCESS")
        self.log(f"Failed: {results['failed']}", "ERROR" if results['failed'] > 0 else "SUCCESS")
        self.log(f"Success Rate: {(results['passed']/results['total_tests']*100):.1f}%", "INFO")
        
        return results

class ServiceManager:
    def __init__(self):
        self.processes = []
        self.logs_queue = queue.Queue()
        
    def log(self, message: str, level: str = "INFO"):
        """Centralized logging with color coding"""
        colors = {
            "INFO": "\033[94m",  # Blue
            "SUCCESS": "\033[92m",  # Green
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",  # Red
            "RESET": "\033[0m"
        }
        color = colors.get(level, colors["INFO"])
        print(f"{color}[{level}] {message}{colors['RESET']}")
    
    def stream_logs(self, process, service_name):
        """Stream logs from a process"""
        while True:
            try:
                line = process.stdout.readline()
                if line:
                    self.log(f"[{service_name}] {line.strip()}", "INFO")
                elif process.poll() is not None:
                    break
            except:
                break
    
    def start_backend(self) -> subprocess.Popen:
        """Start the backend service"""
        self.log("Starting backend service...")
        
        backend_dir = Path("../backend")
        if not backend_dir.exists():
            self.log("Backend directory not found", "ERROR")
            return None
        
        try:
            # Check if package.json exists
            package_json = backend_dir / "package.json"
            if not package_json.exists():
                self.log("Backend package.json not found", "ERROR")
                return None
            
            # Start backend
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Start log streaming in background
            log_thread = threading.Thread(
                target=self.stream_logs, 
                args=(process, "BACKEND"),
                daemon=True
            )
            log_thread.start()
            
            self.processes.append(process)
            return process
            
        except Exception as e:
            self.log(f"Failed to start backend: {str(e)}", "ERROR")
            return None
    
    def start_frontend(self) -> subprocess.Popen:
        """Start the frontend service"""
        self.log("Starting frontend service...")
        
        frontend_dir = Path("../frontend-v2")
        if not frontend_dir.exists():
            self.log("Frontend directory not found", "ERROR")
            return None
        
        try:
            # Check if package.json exists
            package_json = frontend_dir / "package.json"
            if not package_json.exists():
                self.log("Frontend package.json not found", "ERROR")
                return None
            
            # Start frontend
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Start log streaming in background
            log_thread = threading.Thread(
                target=self.stream_logs,
                args=(process, "FRONTEND"), 
                daemon=True
            )
            log_thread.start()
            
            self.processes.append(process)
            return process
            
        except Exception as e:
            self.log(f"Failed to start frontend: {str(e)}", "ERROR")
            return None
    
    def stop_all_services(self):
        """Stop all running services"""
        self.log("Stopping all services...")
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
            except:
                pass
        
        self.processes.clear()
        self.log("All services stopped", "SUCCESS")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.log("\nReceived interrupt signal. Stopping services...", "WARNING")
        self.stop_all_services()
        sys.exit(0)

def main():
    """Main function to orchestrate testing and launching"""
    print("""
🚀 Chess Platform Integration Test & Launch Script
==================================================
This script will:
1. Test all backend API endpoints
2. Launch backend service
3. Launch frontend service  
4. Provide integration testing results
    """)
    
    service_manager = ServiceManager()
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, service_manager.signal_handler)
    signal.signal(signal.SIGTERM, service_manager.signal_handler)
    
    try:
        # Step 1: Launch Backend
        backend_process = service_manager.start_backend()
        if not backend_process:
            service_manager.log("Failed to start backend. Exiting.", "ERROR")
            return
        
        # Wait for backend to be ready
        tester = EndpointTester()
        if not tester.wait_for_service("http://localhost:3001"):
            service_manager.log("Backend service not responding. Exiting.", "ERROR")
            service_manager.stop_all_services()
            return
        
        # Step 2: Test All Endpoints
        service_manager.log("🧪 Running comprehensive endpoint tests...", "INFO")
        test_results = tester.test_all_endpoints()
        
        # Step 3: Launch Frontend
        frontend_process = service_manager.start_frontend()
        if not frontend_process:
            service_manager.log("Failed to start frontend", "ERROR")
        else:
            # Wait for frontend to be ready
            if tester.wait_for_service("http://localhost:5173"):
                service_manager.log("🎉 Frontend service is ready!", "SUCCESS")
            else:
                service_manager.log("Frontend service may not be fully ready", "WARNING")
        
        # Step 4: Display Results and Instructions
        service_manager.log("""
🎯 Integration Test Complete!
=============================
✅ Backend: http://localhost:3001
✅ Frontend: http://localhost:5173

📋 Test Results Summary:
""", "SUCCESS")
        
        for domain_result in test_results["details"]:
            domain = domain_result["domain"]
            tests = domain_result["tests"]
            passed = sum(1 for t in tests if t["success"])
            total = len(tests)
            
            status = "SUCCESS" if passed == total else "WARNING"
            service_manager.log(f"  {domain}: {passed}/{total} tests passed", status)
        
        service_manager.log(f"""
🔧 What to test:
================
1. Visit http://localhost:5173 to see the frontend
2. Test authentication (register/login)
3. Test chess puzzle functionality
4. Test game creation and management
5. Check user profile and statistics
6. Verify learning paths and tutorials

Press Ctrl+C to stop all services when done.
""", "INFO")
        
        # Keep services running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process and backend_process.poll() is not None:
                service_manager.log("Backend process has stopped", "ERROR")
                break
            
            if frontend_process and frontend_process.poll() is not None:
                service_manager.log("Frontend process has stopped", "ERROR")
                break
                
    except KeyboardInterrupt:
        service_manager.log("Received interrupt signal", "WARNING")
    except Exception as e:
        service_manager.log(f"Unexpected error: {str(e)}", "ERROR")
    finally:
        service_manager.stop_all_services()

if __name__ == "__main__":
    main()