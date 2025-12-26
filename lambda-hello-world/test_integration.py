import json
import pytest
import requests
import os


class TestAPIEndpoint:
    """Test the actual API endpoint if deployed"""
    
    @pytest.mark.integration
    def test_api_endpoint_response(self):
        """Test the deployed API endpoint"""
        # Use the known deployed endpoint
        api_endpoint = "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/"
        
        response = requests.get(api_endpoint)
        
        assert response.status_code == 200
        data = response.json()
        assert 'quote' in data
        assert 'timestamp' in data
        assert 'model' in data
        assert data['model'] == 'amazon.titan-text-express-v1'
        assert len(data['quote']) > 0
    
    @pytest.mark.integration
    def test_api_endpoint_headers(self):
        """Test that the API returns proper headers"""
        api_endpoint = "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/"
        
        response = requests.get(api_endpoint)
        
        assert response.status_code == 200
        assert 'application/json' in response.headers.get('content-type', '')
    
    @pytest.mark.integration
    def test_api_endpoint_multiple_calls(self):
        """Test multiple calls to ensure consistency"""
        api_endpoint = "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/"
        
        responses = []
        for i in range(3):
            response = requests.get(api_endpoint)
            assert response.status_code == 200
            data = response.json()
            responses.append(data)
            
        # All responses should have the required structure
        for data in responses:
            assert 'quote' in data
            assert 'timestamp' in data
            assert 'model' in data
            assert data['model'] == 'amazon.titan-text-express-v1'
            
        # Timestamps should be different (unique request IDs)
        timestamps = [r['timestamp'] for r in responses]
        assert len(set(timestamps)) == len(timestamps), "All timestamps should be unique"


class TestLambdaFunction:
    """Test Lambda function behavior without mocking AWS services"""
    
    def test_lambda_function_import(self):
        """Test that we can import the lambda function"""
        from lambda_function import lambda_handler, get_energizing_quote
        assert callable(lambda_handler)
        assert callable(get_energizing_quote)
    
    def test_lambda_function_structure(self):
        """Test the lambda function code structure"""
        import lambda_function
        import inspect
        
        # Check that required functions exist
        assert hasattr(lambda_function, 'lambda_handler')
        assert hasattr(lambda_function, 'get_energizing_quote')
        
        # Check function signatures
        handler_sig = inspect.signature(lambda_function.lambda_handler)
        assert len(handler_sig.parameters) == 2  # event, context
        
        quote_sig = inspect.signature(lambda_function.get_energizing_quote)
        assert len(quote_sig.parameters) == 1  # name parameter (optional)