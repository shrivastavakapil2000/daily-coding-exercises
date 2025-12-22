import json
import pytest
from lambda_function import lambda_handler


class TestLambdaFunction:
    """Unit tests for the Hello World Lambda function"""
    
    def test_lambda_handler_returns_200(self):
        """Test that the function returns a 200 status code"""
        event = {}
        context = {}
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
    
    def test_lambda_handler_returns_hello_world_message(self):
        """Test that the function returns the correct Hello World message"""
        event = {}
        context = {}
        
        response = lambda_handler(event, context)
        body = json.loads(response['body'])
        
        assert body['message'] == 'Hello World'
    
    def test_lambda_handler_returns_valid_json(self):
        """Test that the function returns valid JSON in the body"""
        event = {}
        context = {}
        
        response = lambda_handler(event, context)
        
        # This should not raise an exception
        body = json.loads(response['body'])
        assert isinstance(body, dict)
    
    def test_lambda_handler_with_api_gateway_event(self):
        """Test the function with a typical API Gateway event"""
        event = {
            "httpMethod": "GET",
            "path": "/hello",
            "headers": {
                "Accept": "application/json"
            },
            "queryStringParameters": None,
            "body": None
        }
        context = {
            "requestId": "test-request-id",
            "functionName": "hello-world-function"
        }
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['message'] == 'Hello World'
    
    def test_lambda_handler_response_structure(self):
        """Test that the response has the correct structure"""
        event = {}
        context = {}
        
        response = lambda_handler(event, context)
        
        # Check response structure
        assert 'statusCode' in response
        assert 'body' in response
        assert isinstance(response['statusCode'], int)
        assert isinstance(response['body'], str)
        
        # Check body structure
        body = json.loads(response['body'])
        assert 'message' in body