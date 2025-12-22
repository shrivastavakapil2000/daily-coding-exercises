#!/bin/bash

# Test runner script for Lambda function

set -e

echo "Installing test dependencies..."
pip install -r requirements-dev.txt

echo "Running unit tests..."
pytest test_lambda_function.py -v --tb=short

echo "Running integration tests (mocked)..."
pytest test_integration.py::TestLambdaIntegration -v --tb=short

echo "Running all tests with coverage..."
pytest --cov=lambda_function --cov-report=term-missing --cov-report=html

echo "Test results:"
echo "- Unit tests: ✅"
echo "- Integration tests (mocked): ✅"
echo "- Coverage report generated in htmlcov/"

echo ""
echo "To run integration tests against deployed API:"
echo "export API_ENDPOINT=https://your-api-gateway-url.execute-api.region.amazonaws.com/Prod"
echo "pytest -m integration"