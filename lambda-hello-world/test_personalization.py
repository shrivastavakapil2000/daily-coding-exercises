#!/usr/bin/env python3
"""
Test script for personalized Lambda function
"""

import json
from unittest.mock import MagicMock
from lambda_function import lambda_handler, sanitize_name_input

def test_personalization():
    """Test the enhanced Lambda function with personalization"""
    print("🧪 Testing Enhanced Lambda Function with Personalization")
    print("=" * 60)
    
    context = MagicMock()
    context.aws_request_id = 'test-123'
    
    # Test 1: Query parameter
    print("\n1. Testing with query parameter:")
    event1 = {
        'queryStringParameters': {'name': 'John'},
        'body': None
    }
    result1 = lambda_handler(event1, context)
    print(f"   Status: {result1['statusCode']}")
    body1 = json.loads(result1['body'])
    print(f"   Personalized: {body1.get('personalized')}")
    print(f"   Quote: {body1['quote'][:80]}...")
    
    # Test 2: POST body
    print("\n2. Testing with POST body:")
    event2 = {
        'queryStringParameters': None,
        'body': json.dumps({'name': 'Sarah'})
    }
    result2 = lambda_handler(event2, context)
    print(f"   Status: {result2['statusCode']}")
    body2 = json.loads(result2['body'])
    print(f"   Personalized: {body2.get('personalized')}")
    print(f"   Quote: {body2['quote'][:80]}...")
    
    # Test 3: Backward compatibility (no name)
    print("\n3. Testing backward compatibility (no name):")
    event3 = {
        'queryStringParameters': None,
        'body': None
    }
    result3 = lambda_handler(event3, context)
    print(f"   Status: {result3['statusCode']}")
    body3 = json.loads(result3['body'])
    print(f"   Personalized: {body3.get('personalized')}")
    print(f"   Quote: {body3['quote'][:80]}...")
    
    # Test 4: Input sanitization
    print("\n4. Testing input sanitization:")
    test_inputs = [
        'John Doe',
        'Sarah123!@#',
        '   Alice   ',
        'Bob<script>alert(1)</script>',
        '',
        '   ',
        'A' * 100,  # Long name
        'Mary-Jane O\'Connor'
    ]
    
    for test_input in test_inputs:
        sanitized = sanitize_name_input(test_input)
        print(f"   Input: {repr(test_input)} -> Sanitized: {repr(sanitized)}")
    
    # Test 5: CORS headers
    print("\n5. Testing CORS headers:")
    headers = result1['headers']
    cors_headers = [
        'Access-Control-Allow-Origin',
        'Access-Control-Allow-Methods',
        'Access-Control-Allow-Headers'
    ]
    for header in cors_headers:
        if header in headers:
            print(f"   ✅ {header}: {headers[header]}")
        else:
            print(f"   ❌ Missing: {header}")
    
    print("\n" + "=" * 60)
    print("🎉 Personalization testing complete!")

if __name__ == "__main__":
    test_personalization()