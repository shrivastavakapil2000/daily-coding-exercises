import json
import boto3
import logging
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

def get_energizing_quote():
    """
    Generate an energizing daily quote using Amazon Bedrock
    Uses Titan Text Express (cheapest model)
    """
    try:
        # Prompt for generating energizing quotes
        prompt = """Generate an energizing daily quote that motivates and inspires. 
        The quote should be exactly two sentences long and focus on positivity, growth, or achievement.
        Make it uplifting and powerful.
        
        Quote:"""
        
        # Request body for Titan Text Express
        request_body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 100,
                "temperature": 0.7,
                "topP": 0.9,
                "stopSequences": ["\n\n"]
            }
        }
        
        # Call Bedrock with Titan Text Express (cheapest model)
        response = bedrock_client.invoke_model(
            modelId='amazon.titan-text-express-v1',
            body=json.dumps(request_body),
            contentType='application/json'
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        quote = response_body['results'][0]['outputText'].strip()
        
        # Clean up the quote (remove any extra formatting)
        quote = quote.replace('Quote:', '').strip()
        
        logger.info(f"Generated quote: {quote}")
        return quote
        
    except ClientError as e:
        logger.error(f"Bedrock API error: {str(e)}")
        # Fallback quote if Bedrock fails
        return "Every new day is a chance to transform your dreams into reality. Embrace the possibilities and make today extraordinary!"
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        # Fallback quote for any other errors
        return "Success is not final, failure is not fatal: it is the courage to continue that counts. Today is your day to shine!"

def lambda_handler(event, context):
    """
    AWS Lambda function that returns an energizing daily quote from Bedrock
    """
    try:
        # Generate the daily quote
        daily_quote = get_energizing_quote()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'quote': daily_quote,
                'timestamp': context.aws_request_id if context else 'local-test',
                'model': 'amazon.titan-text-express-v1'
            })
        }
        
    except Exception as e:
        logger.error(f"Lambda handler error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to generate quote',
                'message': str(e)
            })
        }
