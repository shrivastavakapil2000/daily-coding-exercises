import json
import pytest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler, get_energizing_quote


class TestLambdaFunction:
    """Unit tests for the Daily Quote Lambda function"""
    
    @patch('boto3.client')
    def test_lambda_handler_returns_200(self, mock_boto_client):
        """Test that the function returns a 200 status code"""
        # Mock Bedrock client
        mock_bedrock = MagicMock()
        mock_boto_client.return_value = mock_bedrock
        
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'results': [{'outputText': 'Today is your day to shine! Make every moment count.'}]
        }).encode()
        mock_bedrock.invoke_model.return_value = mock_response
        
        event = {}
        context = MagicMock()
        context.aws_request_id = 'test-123'
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
    
    @patch('boto3.client')
    def test_lambda_handler_returns_quote(self, mock_boto_client):
        """Test that the function returns a quote"""
        # Mock Bedrock client
        mock_bedrock = MagicMock()
        mock_boto_client.return_value = mock_bedrock
        
        mock_response = {
            'body': MagicMock()
        }
        test_quote = 'Today is your day to shine! Make every moment count.'
        mock_response['body'].read.return_value = json.dumps({
            'results': [{'outputText': test_quote}]
        }).encode()
        mock_bedrock.invoke_model.return_value = mock_response
        
        event = {}
        context = MagicMock()
        context.aws_request_id = 'test-123'
        
        response = lambda_handler(event, context)
        body = json.loads(response['body'])
        
        assert 'quote' in body
        assert len(body['quote']) > 0
        assert body['model'] == 'amazon.titan-text-express-v1'
    
    @patch('boto3.client')
    def test_lambda_handler_returns_valid_json(self, mock_boto_client):
        """Test that the function returns valid JSON in the body"""
        # Mock Bedrock client
        mock_bedrock = MagicMock()
        mock_boto_client.return_value = mock_bedrock
        
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'results': [{'outputText': 'Success starts with believing in yourself! Take action today.'}]
        }).encode()
        mock_bedrock.invoke_model.return_value = mock_response
        
        event = {}
        context = MagicMock()
        context.aws_request_id = 'test-123'
        
        response = lambda_handler(event, context)
        
        # This should not raise an exception
        body = json.loads(response['body'])
        assert isinstance(body, dict)
        assert 'quote' in body
        assert 'timestamp' in body
        assert 'model' in body
    
    @patch('boto3.client')
    def test_lambda_handler_with_api_gateway_event(self, mock_boto_client):
        """Test the function with a typical API Gateway event"""
        # Mock Bedrock client
        mock_bedrock = MagicMock()
        mock_boto_client.return_value = mock_bedrock
        
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'results': [{'outputText': 'Dream big and work hard! Your potential is limitless.'}]
        }).encode()
        mock_bedrock.invoke_model.return_value = mock_response
        
        event = {
            "httpMethod": "GET",
            "path": "/quote",
            "headers": {
                "Accept": "application/json"
            },
            "queryStringParameters": None,
            "body": None
        }
        context = MagicMock()
        context.aws_request_id = 'test-request-id'
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'quote' in body
        assert len(body['quote']) > 0
    
    @patch('boto3.client')
    def test_bedrock_error_fallback(self, mock_boto_client):
        """Test that function returns fallback quote when Bedrock fails"""
        # Mock Bedrock client to raise an exception
        mock_bedrock = MagicMock()
        mock_boto_client.return_value = mock_bedrock
        mock_bedrock.invoke_model.side_effect = Exception("Bedrock unavailable")
        
        event = {}
        context = MagicMock()
        context.aws_request_id = 'test-123'
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'quote' in body
        # Should return a fallback quote
        assert len(body['quote']) > 0
        assert "Every new day" in body['quote'] or "Success is not final" in body['quote']
    
    @patch('lambda_function.bedrock_client')
    def test_get_energizing_quote_direct(self, mock_bedrock):
        """Test the get_energizing_quote function directly"""
        # Mock Bedrock response
        mock_response = {
            'body': MagicMock()
        }
        test_quote = 'Believe in yourself and all that you are! Know that there is something inside you that is greater than any obstacle.'
        mock_response['body'].read.return_value = json.dumps({
            'results': [{'outputText': test_quote}]
        }).encode()
        mock_bedrock.invoke_model.return_value = mock_response
        
        quote = get_energizing_quote()
        
        assert quote == test_quote
        mock_bedrock.invoke_model.assert_called_once()
    
    def test_lambda_handler_response_structure(self):
        """Test that the response has the correct structure"""
        event = {}
        context = MagicMock()
        context.aws_request_id = 'test-123'
        
        response = lambda_handler(event, context)
        
        # Check response structure
        assert 'statusCode' in response
        assert 'body' in response
        assert 'headers' in response
        assert isinstance(response['statusCode'], int)
        assert isinstance(response['body'], str)
        
        # Check body structure
        body = json.loads(response['body'])
        assert 'quote' in body
        assert 'timestamp' in body
        assert 'model' in body