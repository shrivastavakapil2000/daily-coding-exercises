#!/usr/bin/env python3
"""
Simple local test script to validate the Daily Quote Lambda function
Run this script to quickly test the function locally
"""

import json
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler


def test_function():
    """Test the Lambda function locally with mocked Bedrock"""
    print("🧪 Testing Daily Quote Lambda function locally...")
    
    # Mock boto3.client to return a mock bedrock client
    with patch('boto3.client') as mock_boto_client:
        mock_bedrock = MagicMock()
        mock_boto_client.return_value = mock_bedrock
        
        mock_response = {
            'body': MagicMock()
        }
        test_quote = "Today is your day to shine and make a difference! Embrace every challenge as an opportunity to grow stronger."
        mock_response['body'].read.return_value = json.dumps({
            'results': [{'outputText': test_quote}]
        }).encode()
        mock_bedrock.invoke_model.return_value = mock_response
        
        # Test with empty event
        event = {}
        context = MagicMock()
        context.aws_request_id = 'local-test-123'
        
        try:
            response = lambda_handler(event, context)
            
            print(f"✅ Status Code: {response['statusCode']}")
            
            body = json.loads(response['body'])
            print(f"✅ Response Body: {json.dumps(body, indent=2)}")
            
            # Validate response
            assert response['statusCode'] == 200, f"Expected 200, got {response['statusCode']}"
            assert 'quote' in body, "Response should contain 'quote' field"
            assert len(body['quote']) > 0, "Quote should not be empty"
            assert body['model'] == 'amazon.titan-text-express-v1', "Should use Titan Text Express model"
            
            print("🎉 Basic test passed!")
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            return False


def test_with_api_gateway_event():
    """Test with a simulated API Gateway event"""
    print("\n🧪 Testing with API Gateway event...")
    
    with patch('boto3.client') as mock_boto_client:
        mock_bedrock = MagicMock()
        mock_boto_client.return_value = mock_bedrock
        
        mock_response = {
            'body': MagicMock()
        }
        test_quote = "Success is not just about reaching your destination! It's about enjoying the journey and growing along the way."
        mock_response['body'].read.return_value = json.dumps({
            'results': [{'outputText': test_quote}]
        }).encode()
        mock_bedrock.invoke_model.return_value = mock_response
        
        event = {
            "httpMethod": "GET",
            "path": "/quote",
            "headers": {
                "Accept": "application/json",
                "User-Agent": "test-client"
            },
            "queryStringParameters": None,
            "body": None,
            "isBase64Encoded": False
        }
        
        context = MagicMock()
        context.aws_request_id = 'api-test-456'
        
        try:
            response = lambda_handler(event, context)
            
            print(f"✅ Status Code: {response['statusCode']}")
            body = json.loads(response['body'])
            print(f"✅ Response Body: {json.dumps(body, indent=2)}")
            
            assert response['statusCode'] == 200
            assert 'quote' in body
            assert len(body['quote']) > 0
            assert 'timestamp' in body
            assert 'model' in body
            
            print("🎉 API Gateway event test passed!")
            return True
            
        except Exception as e:
            print(f"❌ API Gateway test failed: {str(e)}")
            return False


def test_fallback_behavior():
    """Test fallback behavior when Bedrock fails"""
    print("\n🧪 Testing fallback behavior...")
    
    with patch('boto3.client') as mock_boto_client:
        mock_bedrock = MagicMock()
        mock_boto_client.return_value = mock_bedrock
        
        # Mock Bedrock to raise an exception
        mock_bedrock.invoke_model.side_effect = Exception("Bedrock service unavailable")
        
        event = {}
        context = MagicMock()
        context.aws_request_id = 'fallback-test-789'
        
        try:
            response = lambda_handler(event, context)
            
            print(f"✅ Status Code: {response['statusCode']}")
            body = json.loads(response['body'])
            print(f"✅ Fallback Quote: {body['quote']}")
            
            assert response['statusCode'] == 200
            assert 'quote' in body
            assert len(body['quote']) > 0
            # Should contain fallback quote
            assert "Every new day" in body['quote'] or "Success is not final" in body['quote']
            
            print("🎉 Fallback test passed!")
            return True
            
        except Exception as e:
            print(f"❌ Fallback test failed: {str(e)}")
            return False


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Daily Quote Lambda Function Local Testing")
    print("=" * 60)
    
    success1 = test_function()
    success2 = test_with_api_gateway_event()
    success3 = test_fallback_behavior()
    
    print("\n" + "=" * 60)
    if success1 and success2 and success3:
        print("🎉 All local tests passed! Your quote function is ready to deploy.")
        print("💡 The function will call Amazon Bedrock Titan Text Express for quotes.")
        print("🔄 Fallback quotes are available if Bedrock is unavailable.")
    else:
        print("❌ Some tests failed. Please check your function.")
    print("=" * 60)