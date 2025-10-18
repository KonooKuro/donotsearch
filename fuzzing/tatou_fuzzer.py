#!/usr/bin/env python3
"""
Clean Tatou API Fuzzer - No special characters
"""

import requests
import json
import itertools
import random
import string
from typing import Dict, List, Any

class TatouFuzzer:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.api_base = base_url + "/api"
        self.session = requests.Session()
        self.findings = []
        
    def generate_malformed_inputs(self):
        """Generate various malformed inputs for testing"""
        return [
            # String attacks
            "A" * 1000,  # Oversized string
            "../../../etc/passwd",  # Path traversal
            "<script>alert(1)</script>",  # XSS
            "'; DROP TABLE users; --",  # SQL injection
            
            # Number attacks
            -1, 0, 999999, 
            
            # Special values
            None, "", " ",
        ]
    
    def fuzz_create_user(self):
        """Fuzz the create-user endpoint"""
        print("Testing /api/create-user endpoint...")
        
        malformed_inputs = self.generate_malformed_inputs()
        
        # Test a few combinations
        test_cases = [
            {"login": "A" * 1000, "password": "test", "email": "test@test.com"},
            {"login": "../../../etc/passwd", "password": "test", "email": "test@test.com"},
            {"login": "test", "password": "A" * 1000, "email": "test@test.com"},
            {"login": "test", "password": "test", "email": "A" * 1000},
        ]
        
        for payload in test_cases:
            try:
                response = self.session.post(
                    self.api_base + "/create-user",
                    json=payload,
                    timeout=5
                )
                
                # Look for interesting responses
                if response.status_code in [500]:
                    self.findings.append({
                        "endpoint": "/api/create-user",
                        "payload": str(payload)[:100],
                        "status_code": response.status_code,
                        "response": response.text[:200],
                        "issue": "Server error with malformed input"
                    })
                    print(f"  Found issue: HTTP {response.status_code}")
                    
            except Exception as e:
                self.findings.append({
                    "endpoint": "/api/create-user", 
                    "payload": str(payload)[:100],
                    "error": str(e),
                    "issue": "Request caused exception"
                })
                print(f"  Exception: {e}")
    
    def fuzz_authentication(self):
        """Fuzz authentication mechanisms"""
        print("Testing authentication...")
        
        # Test with malformed tokens
        malformed_tokens = [
            "Bearer " + "A" * 1000,  # Oversized token
            "Bearer ../../../etc/passwd",  # Path traversal
            "InvalidTokenType xyz123",  # Wrong token type
            "",  # Empty header
            "Bearer",  # Missing token
        ]
        
        for token in malformed_tokens:
            headers = {"Authorization": token} if token else {}
            
            try:
                response = self.session.get(
                    self.api_base + "/list-documents",
                    headers=headers,
                    timeout=5
                )
                
                # Should get 401, anything else is interesting
                if response.status_code not in [401, 403, 404]:
                    self.findings.append({
                        "endpoint": "/api/list-documents",
                        "token": token[:50],
                        "status_code": response.status_code,
                        "issue": "Unexpected auth response"
                    })
                    print(f"  Auth issue: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  Auth exception: {e}")
    
    def run_campaign(self):
        """Run the full fuzzing campaign"""
        print("Starting Tatou API Fuzzing Campaign...")
        
        # Test if server is reachable
        try:
            response = self.session.get(self.api_base + "/healthz", timeout=5)
            print(f"Server reachable: HTTP {response.status_code}")
        except Exception as e:
            print(f"Server not reachable: {e}")
            return
        
        # Run fuzzing campaigns
        self.fuzz_create_user()
        self.fuzz_authentication()
        
        # Report findings
        print(f"\nFuzzing complete! Found {len(self.findings)} potential issues:")
        for i, finding in enumerate(self.findings, 1):
            print(f"{i}. {finding.get('issue', 'Unknown issue')}")
            print(f"   Endpoint: {finding.get('endpoint')}")
            if 'status_code' in finding:
                print(f"   Status: {finding['status_code']}")
    
    def generate_report(self, filename: str = "fuzzing_report.json"):
        """Generate a detailed report"""
        report = {
            "timestamp": "2025-10-19",
            "total_findings": len(self.findings),
            "findings": self.findings,
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to {filename}")

if __name__ == "__main__":
    fuzzer = TatouFuzzer("http://localhost:5000")
    fuzzer.run_campaign()
    fuzzer.generate_report()
