import json
import datetime
import boto3

dynamodb_client = boto3.client('dynamodb')

def result(status, message):
    return {
        'statusCode': status,
        'body': message,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }

def handler(event, context):
    print('Received event is : '+ json.dumps(event))
    existing_tables = dynamodb_client.list_tables()
    data = {
        'event': event,
        'tables': existing_tables,
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return result(200, json.dumps(data)) 
