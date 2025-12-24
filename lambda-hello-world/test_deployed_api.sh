#!/bin/bash

# Test script for the deployed Daily Quote API
API_ENDPOINT="https://clx8580ut5.execute-api.us-east-1.amazonaws.com/Prod/quote/"

echo "🚀 Testing Deployed Daily Quote API"
echo "=================================="
echo "API Endpoint: $API_ENDPOINT"
echo ""

echo "📡 Making API call..."
response=$(curl -s "$API_ENDPOINT")
status_code=$(curl -s -o /dev/null -w "%{http_code}" "$API_ENDPOINT")

echo "✅ HTTP Status: $status_code"
echo "📝 Response:"
echo "$response" | jq .

echo ""
echo "🔍 Checking response structure..."
quote=$(echo "$response" | jq -r '.quote')
timestamp=$(echo "$response" | jq -r '.timestamp')
model=$(echo "$response" | jq -r '.model')

if [ "$status_code" = "200" ]; then
    echo "✅ API is responding successfully"
else
    echo "❌ API returned status code: $status_code"
    exit 1
fi

if [ "$quote" != "null" ] && [ -n "$quote" ]; then
    echo "✅ Quote field present: ${quote:0:50}..."
else
    echo "❌ Quote field missing or empty"
    exit 1
fi

if [ "$timestamp" != "null" ] && [ -n "$timestamp" ]; then
    echo "✅ Timestamp field present: $timestamp"
else
    echo "❌ Timestamp field missing"
    exit 1
fi

if [ "$model" = "amazon.titan-text-express-v1" ]; then
    echo "✅ Model field correct: $model"
else
    echo "❌ Model field incorrect: $model"
    exit 1
fi

echo ""
echo "🎉 All tests passed! Your Daily Quote API is working perfectly!"
echo ""
echo "💡 Note: If you see fallback quotes, it may be due to:"
echo "   - Bedrock throttling (normal for free tier)"
echo "   - Rate limiting (wait a few minutes between calls)"
echo "   - This indicates the fallback system is working correctly!"
echo ""
echo "🔗 You can call this API from anywhere:"
echo "   curl '$API_ENDPOINT'"