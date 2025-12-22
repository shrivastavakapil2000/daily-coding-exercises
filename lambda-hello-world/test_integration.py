import json
import boto3
import pytest
import requests
from moto import mock_lambda, mock_apigateway
import zipfile
import os


@mock_lambda
@mock_apigateway
class TestLambdaIntegration:
    """Integration tests for the Lambda function"""
    
    def setup_method(self):
        """Set up test environment"""
        self.lambda_client = boto3.client('lambda', region_name='us-east-1')
        self.api_client = boto3.client('apigateway', region_name='us-east-1')
        
    def create_lambda_zip(self):
        """Create a zip file with the Lambda function code"""
        zip_path = '/tmp/lambda_function.zip'
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.write('lambda_function.py')
        
        with open(zip_path, 'rb') as zip_file:
            return zip_file.read()
    
    def test_lambda_function_deployment(self):
        """Test that the Lambda function can be deployed and invoked"""
        # Create the Lambda function
        function_name = 'hello-world-test'
        
        # Read the actual lambda function code
        with open('lambda_function.py', 'r') as f:
            lambda_code = f.read()
        
        # Create a simple zip with the code
        zip_content = self.create_lambda_zip()
        
        response = self.lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.9',
            Role='arn:aws:iam::123456789012:role/lambda-role',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content},
            Description='Test Hello World Lambda function'
        )
        
        assert response['FunctionName'] == function_name
        assert response['Runtime'] == 'python3.9'
    
    def test_lambda_function_invocation(self):
        """Test invoking the Lambda function directly"""
        function_name = 'hello-world-test'
        
        # Create the function first
        zip_content = self.create_lambda_zip()
        self.lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.9',
            Role='arn:aws:iam::123456789012:role/lambda-role',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content}
        )
        
        # Invoke the function
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps({})
        )
        
        # Parse the response
        payload = json.loads(response['Payload'].read())
        
        assert payload['statusCode'] == 200
        body = json.loads(payload['body'])
        assert body['message'] == 'Hello World'


class TestAPIEndpoint:
    """Test the actual API endpoint if deployed"""
    
    @pytest.mark.integration
    def test_api_endpoint_response(self):
        """Test the deployed API endpoint (requires actual deployment)"""
        # This test requires the API_ENDPOINT environment variable
        api_endpoint = os.environ.get('API_ENDPOINT')
        
        if not api_endpoint:
            pytest.skip("API_ENDPOINT environment variable not set")
        
        response = requests.get(f"{api_endpoint}/hello")
        
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == 'Hello World'
    
    @pytest.mark.integration
    def test_api_endpoint_headers(self):
        """Test that the API returns proper headers"""
        api_endpoint = os.environ.get('API_ENDPOINT')
        
        if not api_endpoint:
            pytest.skip("API_ENDPOINT environment variable not set")
        
        response = requests.get(f"{api_endpoint}/hello")
        
        assert response.status_code == 200
        assert 'application/json' in response.headers.get('content-type', '')