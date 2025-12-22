import json

def lambda_handler(event, context):
    """
    AWS Lambda function that returns "Hello World"
    """
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello World'
        })
    }