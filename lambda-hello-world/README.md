# Hello World AWS Lambda Function

A simple AWS Lambda function that returns "Hello World" with CI/CD pipeline.

## Project Structure

```
lambda-hello-world/
├── lambda_function.py          # Main Lambda function
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── template.yaml              # SAM template for infrastructure
├── deploy.sh                  # Local deployment script
├── test_lambda_function.py    # Unit tests
├── test_integration.py        # Integration tests
├── test_local.py              # Quick local test script
├── run_tests.sh               # Test runner script
├── pytest.ini                # Pytest configuration
├── .github/workflows/         # GitHub Actions CI/CD
│   └── deploy.yml
├── .gitignore
└── README.md
```

## Prerequisites

1. **AWS CLI** - Install and configure with your credentials
2. **SAM CLI** - AWS Serverless Application Model CLI
3. **Python 3.9+**

## Local Development

### Install SAM CLI
```bash
pip install aws-sam-cli
```

### Configure AWS Credentials
```bash
aws configure
```

### Deploy Locally
```bash
cd lambda-hello-world
./deploy.sh
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow that automatically deploys on push to main branch.

### Setup GitHub Secrets

Add these secrets to your GitHub repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Manual Deployment Trigger

You can also trigger deployment manually from the GitHub Actions tab.

## Testing

### Quick Local Test
```bash
cd lambda-hello-world
python test_local.py
```

### Run Full Test Suite
```bash
cd lambda-hello-world
./run_tests.sh
```

### Run Specific Tests
```bash
# Unit tests only
pytest test_lambda_function.py -v

# Integration tests (mocked)
pytest test_integration.py::TestLambdaIntegration -v

# Tests with coverage
pytest --cov=lambda_function --cov-report=term-missing
```

### Test Against Deployed API
After deployment, test the live API:
```bash
# Set your API endpoint
export API_ENDPOINT=https://your-api-gateway-url.execute-api.region.amazonaws.com/Prod

# Run integration tests
pytest -m integration
```

## Testing

Once deployed, you'll get an API Gateway URL. Test it with:

```bash
curl https://your-api-gateway-url/Prod/hello/
```

Expected response:
```json
{
  "message": "Hello World"
}
```

## AWS Resources Created

- Lambda Function
- API Gateway REST API
- IAM Role for Lambda execution
- CloudFormation Stack