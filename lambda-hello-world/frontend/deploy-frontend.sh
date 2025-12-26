#!/bin/bash

# Frontend Deployment Script for Daily Quote Generator
# Deploys static files to S3 bucket with website hosting

set -e

# Configuration
STACK_NAME="hello-world-lambda"
REGION="us-east-1"
FRONTEND_DIR="$(dirname "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if AWS CLI is installed
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    log_success "AWS CLI found"
}

# Check if user is authenticated
check_aws_auth() {
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS CLI is not configured or you're not authenticated."
        log_info "Run 'aws configure' to set up your credentials."
        exit 1
    fi
    log_success "AWS authentication verified"
}

# Get S3 bucket name from CloudFormation stack
get_bucket_name() {
    log_info "Getting S3 bucket name from CloudFormation stack..."
    
    BUCKET_NAME=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$REGION" \
        --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' \
        --output text 2>/dev/null)
    
    if [ -z "$BUCKET_NAME" ] || [ "$BUCKET_NAME" = "None" ]; then
        log_error "Could not find S3 bucket name in CloudFormation stack '$STACK_NAME'"
        log_info "Make sure the stack is deployed with the S3 bucket resource."
        exit 1
    fi
    
    log_success "Found S3 bucket: $BUCKET_NAME"
}

# Validate frontend files exist
validate_frontend_files() {
    log_info "Validating frontend files..."
    
    local required_files=("index.html" "style.css" "script.js")
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$FRONTEND_DIR/$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -ne 0 ]; then
        log_error "Missing required frontend files:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi
    
    log_success "All required frontend files found"
}

# Upload files to S3
upload_files() {
    log_info "Uploading frontend files to S3..."
    
    # Upload HTML file with proper content type
    aws s3 cp "$FRONTEND_DIR/index.html" "s3://$BUCKET_NAME/index.html" \
        --content-type "text/html" \
        --cache-control "no-cache" \
        --region "$REGION"
    
    # Upload CSS file with proper content type
    aws s3 cp "$FRONTEND_DIR/style.css" "s3://$BUCKET_NAME/style.css" \
        --content-type "text/css" \
        --cache-control "max-age=86400" \
        --region "$REGION"
    
    # Upload JavaScript file with proper content type
    aws s3 cp "$FRONTEND_DIR/script.js" "s3://$BUCKET_NAME/script.js" \
        --content-type "application/javascript" \
        --cache-control "max-age=86400" \
        --region "$REGION"
    
    log_success "Files uploaded successfully"
}

# Get website URL
get_website_url() {
    log_info "Getting website URL..."
    
    WEBSITE_URL=$(aws cloudformation describe-stacks \
        --stack-name "$STACK_NAME" \
        --region "$REGION" \
        --query 'Stacks[0].Outputs[?OutputKey==`FrontendWebsiteURL`].OutputValue' \
        --output text 2>/dev/null)
    
    if [ -z "$WEBSITE_URL" ] || [ "$WEBSITE_URL" = "None" ]; then
        # Fallback: construct URL manually
        WEBSITE_URL="http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
        log_warning "Could not get URL from stack outputs, using constructed URL"
    fi
    
    log_success "Website URL: $WEBSITE_URL"
}

# Test website accessibility
test_website() {
    log_info "Testing website accessibility..."
    
    # Wait a moment for S3 to propagate
    sleep 3
    
    if curl -s --head "$WEBSITE_URL" | head -n 1 | grep -q "200 OK"; then
        log_success "Website is accessible!"
    else
        log_warning "Website might not be immediately accessible. This is normal for new deployments."
        log_info "Try accessing the URL in a few minutes: $WEBSITE_URL"
    fi
}

# Display deployment summary
show_summary() {
    echo ""
    echo "🎉 Frontend Deployment Complete!"
    echo "=================================="
    echo "📦 Bucket Name: $BUCKET_NAME"
    echo "🌐 Website URL: $WEBSITE_URL"
    echo "📁 Files Deployed:"
    echo "   - index.html (HTML page)"
    echo "   - style.css (Styles)"
    echo "   - script.js (JavaScript logic)"
    echo ""
    echo "🔗 You can now access your personalized quote generator at:"
    echo "   $WEBSITE_URL"
    echo ""
    echo "💡 Tips:"
    echo "   - Bookmark the URL for easy access"
    echo "   - Share it with friends and family"
    echo "   - The website works on mobile and desktop"
    echo ""
}

# Main deployment function
main() {
    echo "🚀 Starting Frontend Deployment"
    echo "==============================="
    echo "Stack: $STACK_NAME"
    echo "Region: $REGION"
    echo "Frontend Dir: $FRONTEND_DIR"
    echo ""
    
    # Run deployment steps
    check_aws_cli
    check_aws_auth
    validate_frontend_files
    get_bucket_name
    upload_files
    get_website_url
    test_website
    show_summary
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Frontend Deployment Script for Daily Quote Generator"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --bucket NAME  Override bucket name (optional)"
        echo "  --region NAME  Override AWS region (default: us-east-1)"
        echo ""
        echo "Environment Variables:"
        echo "  STACK_NAME     CloudFormation stack name (default: hello-world-lambda)"
        echo "  REGION         AWS region (default: us-east-1)"
        echo ""
        exit 0
        ;;
    --bucket)
        if [ -n "${2:-}" ]; then
            BUCKET_NAME="$2"
            log_info "Using provided bucket name: $BUCKET_NAME"
        else
            log_error "Bucket name required after --bucket flag"
            exit 1
        fi
        ;;
    --region)
        if [ -n "${2:-}" ]; then
            REGION="$2"
            log_info "Using provided region: $REGION"
        else
            log_error "Region required after --region flag"
            exit 1
        fi
        ;;
esac

# Run main function
main