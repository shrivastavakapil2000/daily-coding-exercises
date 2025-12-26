# Personalized Daily Quote Generator

A complete serverless application that generates personalized energizing daily quotes using Amazon Bedrock AI, featuring a minimalistic web frontend and robust CI/CD pipeline.

## Features

- 🤖 **AI-Powered Quotes**: Uses Amazon Bedrock Titan Text Express (cost-effective model)
- 👤 **Personalization**: Generates personalized quotes based on user's name
- ⚡ **Energizing Content**: Creates motivational two-sentence quotes
- 🌐 **Web Frontend**: Clean, responsive web interface hosted on S3
- 🔄 **Fallback System**: Provides backup quotes if Bedrock is unavailable
- 🚀 **Serverless**: Fully serverless architecture with API Gateway and S3
- 🔧 **CI/CD Ready**: Automated testing and deployment pipeline
- ♿ **Accessible**: WCAG compliant with proper ARIA labels and keyboard navigation

## Project Structure

```
lambda-hello-world/
├── lambda_function.py          # Main Lambda function with personalization
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── template.yaml              # SAM template for infrastructure
├── deploy.sh                  # Local deployment script
├── frontend/                  # Web frontend files
│   ├── index.html            # Main HTML page
│   ├── style.css             # Responsive CSS styling
│   ├── script.js             # Frontend JavaScript logic
│   └── deploy-frontend.sh    # Frontend deployment script
├── test_lambda_function.py    # Unit tests
├── test_integration.py        # Integration tests
├── test_local.py              # Quick local test script
├── test_personalization.py   # Personalization feature tests
├── run_tests.sh               # Test runner script
├── pytest.ini                # Pytest configuration
├── .github/workflows/         # GitHub Actions CI/CD
│   └── deploy.yml
├── .gitignore
└── README.md
```

## Quick Start

### 🌐 Try the Live Application

**Web Interface:** http://daily-quote-frontend-1766764914.s3-website-us-east-1.amazonaws.com

Simply enter your name and get a personalized energizing quote powered by AI!

### 🔗 API Endpoint

**Backend API:** https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/

```bash
# Get a generic quote
curl "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/"

# Get a personalized quote
curl "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/?name=John"
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

### Deploy Backend
```bash
cd lambda-hello-world
./deploy.sh
```

### Deploy Frontend
```bash
cd lambda-hello-world/frontend
./deploy-frontend.sh
```

### Deploy Both (Complete System)
```bash
cd lambda-hello-world
# Deploy backend first
./deploy.sh

# Then deploy frontend
cd frontend
./deploy-frontend.sh
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

# Personalization tests
pytest test_personalization.py -v

# Tests with coverage
pytest --cov=lambda_function --cov-report=term-missing
```

### Test Against Deployed API
After deployment, test the live API:
```bash
# Test generic quote
curl "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/"

# Test personalized quote
curl "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/?name=Alice"
```

Expected response:
```json
{
  "quote": "Hey Alice, every new day is a chance to transform your dreams into reality! Embrace the possibilities and make today extraordinary.",
  "timestamp": "request-id-12345",
  "model": "amazon.titan-text-express-v1",
  "personalized": true
}
```

## AWS Resources Created

### Backend Resources
- Lambda Function with Bedrock permissions and personalization support
- API Gateway REST API with CORS enabled
- IAM Role for Lambda execution with Bedrock access
- CloudFormation Stack

### Frontend Resources
- S3 Bucket configured for static website hosting
- Bucket policy for public read access
- Website endpoint for frontend access

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   S3 Website    │    │   API Gateway    │    │  Lambda Function│
│   (Frontend)    │───▶│   (REST API)     │───▶│  (Backend Logic)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │ Amazon Bedrock  │
                                               │ (AI Quote Gen)  │
                                               └─────────────────┘
```

## Deployment Status

✅ **Successfully Deployed!**

### 🌐 Live Application
**Frontend URL:** http://daily-quote-frontend-1766764914.s3-website-us-east-1.amazonaws.com

### 🔗 API Endpoints
**Backend API:** https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/

**Test the API:**
```bash
# Generic quote
curl "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/"

# Personalized quote
curl "https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/?name=YourName"
```

**Quick Test Script:**
```bash
cd lambda-hello-world
./test_deployed_api.sh
```

## Frontend Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Accessibility**: WCAG compliant with proper ARIA labels and keyboard navigation
- **Input Validation**: Client-side validation with helpful error messages
- **Loading States**: Visual feedback during API calls with loading animations
- **Error Handling**: Graceful error handling with retry functionality
- **Personalization**: Dynamic quote generation based on user input
- **Modern UI**: Clean, minimalistic design with smooth animations

## Troubleshooting

### Frontend Issues
- **Website not loading**: Check S3 bucket policy and website hosting configuration
- **API calls failing**: Verify CORS headers and API Gateway endpoint
- **Quotes not personalizing**: Check name parameter is being sent correctly

### Backend Issues
- **Bedrock access denied**: Ensure your AWS account has Bedrock access enabled
- **Lambda timeout**: Check CloudWatch logs for detailed error information
- **CORS errors**: Verify API Gateway CORS configuration

### Common Solutions
```bash
# Redeploy backend
cd lambda-hello-world && ./deploy.sh

# Redeploy frontend
cd lambda-hello-world/frontend && ./deploy-frontend.sh

# Check CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/daily-quote"
```

## Important Notes

- **Bedrock Access**: Ensure your AWS account has access to Amazon Bedrock in your deployment region
- **Model Availability**: The function uses `amazon.titan-text-express-v1` (most cost-effective)
- **Fallback Quotes**: Built-in fallback system provides quotes even if Bedrock is unavailable
- **Cost Optimization**: Uses the cheapest Bedrock model with minimal token usage
- **Input Sanitization**: Name inputs are sanitized to prevent prompt injection attacks
- **CORS Configuration**: API Gateway configured to allow frontend access from S3 website
- **Responsive Design**: Frontend works on all device sizes with mobile-first approach

## License

This project is open source and available under the [MIT License](LICENSE).