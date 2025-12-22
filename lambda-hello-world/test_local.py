#!/usr/bin/env python3
"""
Simple local test script to validate the Lambda function
Run this script to quickly test the function locally
"""

import json
from lambda_function import lambda_handler


def test_function():
    """Test the Lambda function locally"""
    print("🧪 Testing Lambda function locally...")
    
    # Test with empty event
    event = {}
    context = {}
    
    try:
        response = lambda_handler(event, context)
        
        print(f"✅ Status Code: {response['statusCode']}")
        
        body = json.loads(response['body'])
        print(f"✅ Response Body: {json.dumps(body, indent=2)}")
        
        # Validate response
        assert response['statusCode'] == 200, f"Expected 200, got {response['statusCode']}"
        assert body['message'] == 'Hello World', f"Expected 'Hello World', got {body['message']}"
        
        print("🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_with_api_gateway_event():
    """Test with a simulated API Gateway event"""
    print("\n🧪 Testing with API Gateway event...")
    
    event = {
        "httpMethod": "GET",
        "path": "/hello",
        "headers": {
            "Accept": "application/json",
            "User-Agent": "test-client"
        },
        "queryStringParameters": None,
        "body": None,
        "isBase64Encoded": False
    }
    
    context = {
        "requestId": "test-12345",
        "functionName": "hello-world-function",
        "functionVersion": "$LATEST"
    }
    
    try:
        response = lambda_handler(event, context)
        
        print(f"✅ Status Code: {response['statusCode']}")
        body = json.loads(response['body'])
        print(f"✅ Response Body: {json.dumps(body, indent=2)}")
        
        assert response['statusCode'] == 200
        assert body['message'] == 'Hello World'
        
        print("🎉 API Gateway event test passed!")
        return True
        
    except Exception as e:
        print(f"❌ API Gateway test failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Lambda Function Local Testing")
    print("=" * 50)
    
    success1 = test_function()
    success2 = test_with_api_gateway_event()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 All local tests passed! Your function is ready to deploy.")
    else:
        print("❌ Some tests failed. Please check your function.")
    print("=" * 50)