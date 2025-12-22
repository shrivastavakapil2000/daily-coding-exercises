# Hello World AWS Lambda Function

A simple AWS Lambda function that returns "Hello World" with CI/CD pipeline.

## Project Structure

```
lambda-hello-world/
├── lambda_function.py      # Main Lambda function
├── requirements.txt        # Python dependencies
├── template.yaml          # SAM template for infrastructure
├── deploy.sh              # Local deployment script
├── .github/workflows/     # GitHub Actions CI/CD
│   └── deploy.yml
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