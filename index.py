import json
import datetime
import boto3

dynamodb_client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')

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
    # todo make this an env variable using cloudformation   
    table = dynamodb.Table('GodMessagesTable')
    if (event['resource'] == "/msgs"):
        response = table.scan()
        print('Response from scan is : ' + json.dumps(response))
        if "ResponseMetadata" in response:
            del response["ResponseMetadata"]
        return {
            'statusCode': '200',
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    elif (event['resource'] == "/msg/{msgid}" and event['httpMethod'] == "GET"):
        # msgid the url parameter passed to API gateway. All the URL paramteres ap pear under pathParameters
        msgid = event['pathParameters']['msgid']
        print('Getting the message with ID {}.'.format(msgid))
        response = table.get_item(Key={'msgid':str(msgid)})
        print('Response from get_item is : ' + json.dumps(response))
        if 'Item' in response:
            # If there is an Item key in that response then we have found the item
            item = response['Item']
        else:
            # If there is no Item key in the response then we have not found the item
            return result(400, "Msg not found")

        print('Constructed result is : ' + json.dumps(item))
        return result(200, json.dumps(item))
    else:
        return result(500, "The resource {} is no handled by lambda.".format(event['resource']))
