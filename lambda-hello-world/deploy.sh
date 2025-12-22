#!/bin/bash

# Local deployment script for AWS Lambda Hello World function
# Make sure you have AWS CLI configured with proper credentials

set -e

STACK_NAME="hello-world-lambda"
REGION="us-east-1"

echo "Building SAM application..."
sam build

echo "Deploying to AWS..."
sam deploy \
  --stack-name $STACK_NAME \
  --capabilities CAPABILITY_IAM \
  --region $REGION \
  --guided

echo "Deployment complete!"
echo "You can test your function by visiting the API Gateway URL shown above."