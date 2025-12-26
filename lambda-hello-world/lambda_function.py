import json
import boto3
import logging
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

def get_energizing_quote(name=None):
    """
    Generate an energizing daily quote using Amazon Bedrock
    Uses Titan Text Express (cheapest model)
    """
    try:
        # Create personalized prompt based on whether name is provided
        if name and name.strip():
            prompt = f"""Generate a personalized energizing daily quote for {name.strip()}. 
            The quote should be exactly two sentences long, motivational, and inspiring.
            Address {name.strip()} directly in the quote to make it personal and uplifting.
            Focus on positivity, growth, and achievement.
            
            Personalized Quote for {name.strip()}:"""
        else:
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
        quote = quote.replace('Quote:', '').replace(f'Personalized Quote for {name.strip() if name else ""}:', '').strip()
        
        logger.info(f"Generated quote for {name or 'anonymous'}: {quote}")
        return quote
        
    except ClientError as e:
        logger.error(f"Bedrock API error: {str(e)}")
        # Personalized fallback quote if Bedrock fails
        if name and name.strip():
            return f"Hey {name.strip()}, every new day is a chance to transform your dreams into reality! Embrace the possibilities and make today extraordinary."
        else:
            return "Every new day is a chance to transform your dreams into reality. Embrace the possibilities and make today extraordinary!"
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        # Personalized fallback quote for any other errors
        if name and name.strip():
            return f"{name.strip()}, success is not final, failure is not fatal: it is the courage to continue that counts! Today is your day to shine."
        else:
            return "Success is not final, failure is not fatal: it is the courage to continue that counts. Today is your day to shine!"

def lambda_handler(event, context):
    """
    AWS Lambda function that returns an energizing daily quote from Bedrock
    Supports personalization via name parameter
    """
    try:
        # Handle OPTIONS request for CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
                    'Access-Control-Max-Age': '600'
                },
                'body': ''
            }
        
        # Extract name from query parameters or POST body
        name = None
        
        # Check query string parameters
        if event.get('queryStringParameters'):
            name = event['queryStringParameters'].get('name')
        
        # Check POST body if no query parameter
        if not name and event.get('body'):
            try:
                body = json.loads(event['body'])
                name = body.get('name')
            except (json.JSONDecodeError, TypeError):
                pass
        
        # Sanitize name input to prevent prompt injection
        if name:
            name = sanitize_name_input(name)
        
        # Generate the daily quote (personalized or generic)
        daily_quote = get_energizing_quote(name)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token'
            },
            'body': json.dumps({
                'quote': daily_quote,
                'timestamp': context.aws_request_id if context else 'local-test',
                'model': 'amazon.titan-text-express-v1',
                'personalized': bool(name and name.strip())
            })
        }
        
    except Exception as e:
        logger.error(f"Lambda handler error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Failed to generate quote',
                'message': str(e)
            })
        }

def sanitize_name_input(name):
    """
    Sanitize name input to prevent prompt injection and ensure safety
    """
    if not name or not isinstance(name, str):
        return None
    
    # Remove excessive whitespace and limit length
    name = name.strip()[:50]  # Limit to 50 characters
    
    # Remove potentially harmful characters but keep basic punctuation
    import re
    # Allow letters, spaces, hyphens, apostrophes, and basic punctuation
    name = re.sub(r'[^\w\s\-\'\.]', '', name)
    
    # Remove multiple consecutive spaces
    name = re.sub(r'\s+', ' ', name)
    
    # Return None if name becomes empty after sanitization
    return name if name and len(name.strip()) > 0 else None