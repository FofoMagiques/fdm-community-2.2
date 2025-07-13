#!/usr/bin/env python3
"""
FDM Community Backend API Test Suite
Tests all backend endpoints using the public URL configuration
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class FDMBackendTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status} - {name}"
        if details:
            result += f" | {details}"
        
        print(result)
        self.test_results.append({
            "name": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def run_test(self, name: str, method: str, endpoint: str, expected_status: int, 
                 data: Optional[Dict] = None, headers: Optional[Dict] = None) -> tuple[bool, Dict]:
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        
        # Default headers
        default_headers = {'Content-Type': 'application/json'}
        if self.token:
            default_headers['Authorization'] = f'Bearer {self.token}'
        if headers:
            default_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=10)
            else:
                self.log_test(name, False, f"Unsupported method: {method}")
                return False, {}

            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}

            details = f"Status: {response.status_code}"
            if not success:
                details += f" (expected {expected_status})"
                if response.text:
                    details += f" | Response: {response.text[:200]}"

            self.log_test(name, success, details)
            return success, response_data

        except requests.exceptions.RequestException as e:
            self.log_test(name, False, f"Request failed: {str(e)}")
            return False, {}
        except Exception as e:
            self.log_test(name, False, f"Unexpected error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        success, response = self.run_test(
            "Root Endpoint",
            "GET",
            "",
            200
        )
        
        if success and response.get("message") == "FDM Community API":
            self.log_test("Root Message Content", True, "Correct API message")
        elif success:
            self.log_test("Root Message Content", False, f"Unexpected message: {response}")
        
        return success

    def test_discord_auth_endpoint(self):
        """Test Discord OAuth initiation endpoint"""
        success, response = self.run_test(
            "Discord Auth Endpoint",
            "GET",
            "auth/discord",
            200
        )
        
        if success and "url" in response and "discord.com" in response["url"]:
            self.log_test("Discord Auth URL", True, "Valid Discord OAuth URL returned")
        elif success:
            self.log_test("Discord Auth URL", False, f"Invalid response: {response}")
        
        return success

    def test_stats_endpoint(self):
        """Test server statistics endpoint"""
        success, response = self.run_test(
            "Server Stats Endpoint",
            "GET",
            "stats",
            200
        )
        
        if success:
            expected_fields = ["member_count", "online_count", "boost_count", "channel_count", "role_count"]
            missing_fields = [field for field in expected_fields if field not in response]
            
            if not missing_fields:
                self.log_test("Stats Fields", True, f"All required fields present: {expected_fields}")
            else:
                self.log_test("Stats Fields", False, f"Missing fields: {missing_fields}")
        
        return success

    def test_protected_endpoints_without_auth(self):
        """Test that protected endpoints return 401 without authentication"""
        protected_endpoints = [
            ("auth/me", "GET"),
            ("users", "GET"),
            ("admin/dashboard", "GET")
        ]
        
        all_passed = True
        for endpoint, method in protected_endpoints:
            success, _ = self.run_test(
                f"Protected {endpoint} (No Auth)",
                method,
                endpoint,
                401
            )
            if not success:
                all_passed = False
        
        return all_passed

    def test_nonexistent_endpoints(self):
        """Test that non-existent endpoints return 404"""
        nonexistent_endpoints = [
            "nonexistent",
            "auth/invalid",
            "users/invalid/action"
        ]
        
        all_passed = True
        for endpoint in nonexistent_endpoints:
            success, _ = self.run_test(
                f"Non-existent {endpoint}",
                "GET",
                endpoint,
                404
            )
            if not success:
                all_passed = False
        
        return all_passed

    def test_cors_headers(self):
        """Test CORS headers are present"""
        try:
            response = requests.options(f"{self.api_url}/", timeout=10)
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers'
            ]
            
            present_headers = [header for header in cors_headers if header in response.headers]
            
            if len(present_headers) >= 1:  # At least some CORS headers should be present
                self.log_test("CORS Headers", True, f"CORS headers present: {present_headers}")
                return True
            else:
                self.log_test("CORS Headers", False, "No CORS headers found")
                return False
                
        except Exception as e:
            self.log_test("CORS Headers", False, f"Failed to test CORS: {str(e)}")
            return False

    def test_api_health(self):
        """Test overall API health and connectivity"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code in [200, 404]:  # Either works or gives 404 (which means server is up)
                self.log_test("API Connectivity", True, f"Server responding (status: {response.status_code})")
                return True
            else:
                self.log_test("API Connectivity", False, f"Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Connectivity", False, f"Cannot connect to server: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting FDM Community Backend API Tests")
        print(f"📍 Testing API at: {self.api_url}")
        print("=" * 60)
        
        # Test API connectivity first
        if not self.test_api_health():
            print("\n❌ Cannot connect to API server. Stopping tests.")
            return False
        
        # Run all tests
        test_methods = [
            self.test_root_endpoint,
            self.test_discord_auth_endpoint,
            self.test_stats_endpoint,
            self.test_protected_endpoints_without_auth,
            self.test_nonexistent_endpoints,
            self.test_cors_headers
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(f"Test {test_method.__name__}", False, f"Test crashed: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 All tests passed! Backend API is working correctly.")
            return True
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} test(s) failed. Check the details above.")
            return False

def main():
    """Main test execution"""
    tester = FDMBackendTester()
    success = tester.run_all_tests()
    
    # Save test results to file
    try:
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_tests": tester.tests_run,
                "passed_tests": tester.tests_passed,
                "success_rate": tester.tests_passed/tester.tests_run if tester.tests_run > 0 else 0,
                "results": tester.test_results
            }, f, indent=2)
        print(f"\n📄 Test results saved to: /app/backend_test_results.json")
    except Exception as e:
        print(f"\n⚠️  Could not save test results: {e}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())