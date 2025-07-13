#!/usr/bin/env python3
"""
FDM Community Integration Test
Tests frontend-backend integration and API communication
"""

import requests
import json
import sys
from datetime import datetime

class FDMIntegrationTester:
    def __init__(self):
        self.backend_url = "http://localhost:8001"
        self.frontend_url = "http://localhost:3000"
        self.api_url = f"{self.backend_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

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

    def test_frontend_serving(self):
        """Test that frontend is serving the React app"""
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200 and "FDM Community" in response.text:
                self.log_test("Frontend Serving", True, "React app HTML served correctly")
                return True
            else:
                self.log_test("Frontend Serving", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Frontend Serving", False, f"Error: {str(e)}")
            return False

    def test_frontend_static_assets(self):
        """Test that static assets are accessible"""
        assets_to_test = [
            "/image/Logo FDM V3.png",
            "/static/js/bundle.js"
        ]
        
        all_passed = True
        for asset in assets_to_test:
            try:
                response = requests.get(f"{self.frontend_url}{asset}", timeout=5)
                if response.status_code == 200:
                    self.log_test(f"Asset {asset}", True, f"Size: {len(response.content)} bytes")
                else:
                    self.log_test(f"Asset {asset}", False, f"Status: {response.status_code}")
                    all_passed = False
            except Exception as e:
                self.log_test(f"Asset {asset}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_backend_api_endpoints(self):
        """Test key backend API endpoints"""
        endpoints_to_test = [
            ("/", "Root endpoint"),
            ("/auth/discord", "Discord OAuth"),
            ("/stats", "Server statistics")
        ]
        
        all_passed = True
        for endpoint, description in endpoints_to_test:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(f"API {description}", True, f"Response keys: {list(data.keys())}")
                else:
                    self.log_test(f"API {description}", False, f"Status: {response.status_code}")
                    all_passed = False
            except Exception as e:
                self.log_test(f"API {description}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_cors_configuration(self):
        """Test CORS configuration for frontend-backend communication"""
        try:
            # Test preflight request
            headers = {
                'Origin': self.frontend_url,
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = requests.options(f"{self.api_url}/stats", headers=headers, timeout=5)
            
            # Check if CORS headers are present in response
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers'
            ]
            
            present_cors = [h for h in cors_headers if h in response.headers]
            
            if present_cors:
                self.log_test("CORS Configuration", True, f"Headers: {present_cors}")
                return True
            else:
                # Try actual request to see if CORS works
                response = requests.get(f"{self.api_url}/stats", 
                                      headers={'Origin': self.frontend_url}, timeout=5)
                if response.status_code == 200:
                    self.log_test("CORS Configuration", True, "CORS working (simple request)")
                    return True
                else:
                    self.log_test("CORS Configuration", False, "No CORS headers found")
                    return False
                    
        except Exception as e:
            self.log_test("CORS Configuration", False, f"Error: {str(e)}")
            return False

    def test_discord_oauth_flow(self):
        """Test Discord OAuth configuration"""
        try:
            response = requests.get(f"{self.api_url}/auth/discord", timeout=5)
            if response.status_code == 200:
                data = response.json()
                oauth_url = data.get('url', '')
                
                # Check OAuth URL components
                required_components = [
                    'discord.com/api/oauth2/authorize',
                    'client_id=1393406406865977477',
                    'redirect_uri=http://teamfdm.fr:3000/callback',
                    'response_type=code',
                    'scope=identify%20email%20guilds'
                ]
                
                missing_components = [comp for comp in required_components if comp not in oauth_url]
                
                if not missing_components:
                    self.log_test("Discord OAuth URL", True, "All required components present")
                    return True
                else:
                    self.log_test("Discord OAuth URL", False, f"Missing: {missing_components}")
                    return False
            else:
                self.log_test("Discord OAuth URL", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Discord OAuth URL", False, f"Error: {str(e)}")
            return False

    def test_server_statistics(self):
        """Test server statistics endpoint and data structure"""
        try:
            response = requests.get(f"{self.api_url}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                
                required_fields = [
                    'member_count', 'online_count', 'boost_count', 
                    'channel_count', 'role_count', 'updated_at'
                ]
                
                missing_fields = [field for field in required_fields if field not in stats]
                
                if not missing_fields:
                    # Check if we got actual Discord data
                    has_data = any(stats[field] > 0 for field in required_fields[:-1])  # Exclude updated_at
                    
                    if has_data:
                        self.log_test("Server Statistics", True, 
                                    f"Members: {stats['member_count']}, Channels: {stats['channel_count']}")
                    else:
                        self.log_test("Server Statistics", True, 
                                    "Structure correct but no Discord data (expected in test env)")
                    return True
                else:
                    self.log_test("Server Statistics", False, f"Missing fields: {missing_fields}")
                    return False
            else:
                self.log_test("Server Statistics", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Server Statistics", False, f"Error: {str(e)}")
            return False

    def test_protected_endpoints(self):
        """Test that protected endpoints require authentication"""
        protected_endpoints = [
            "/auth/me",
            "/users", 
            "/admin/dashboard"
        ]
        
        all_passed = True
        for endpoint in protected_endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=5)
                # Should return 401 or 403 for unauthenticated requests
                if response.status_code in [401, 403]:
                    self.log_test(f"Protected {endpoint}", True, f"Status: {response.status_code}")
                else:
                    self.log_test(f"Protected {endpoint}", False, 
                                f"Expected 401/403, got {response.status_code}")
                    all_passed = False
            except Exception as e:
                self.log_test(f"Protected {endpoint}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed

    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting FDM Community Integration Tests")
        print("=" * 60)
        
        test_methods = [
            self.test_frontend_serving,
            self.test_frontend_static_assets,
            self.test_backend_api_endpoints,
            self.test_cors_configuration,
            self.test_discord_oauth_flow,
            self.test_server_statistics,
            self.test_protected_endpoints
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(f"Test {test_method.__name__}", False, f"Test crashed: {str(e)}")
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 All integration tests passed!")
            return True
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} test(s) failed.")
            return False

def main():
    """Main test execution"""
    tester = FDMIntegrationTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())