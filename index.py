import json
import datetime
import boto3
import uuid


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
    ddb_resource = boto3.resource('dynamodb', 'us-east-1')
    # todo make this an env variable using cloudformation   
    ddb_table = ddb_resource.Table('awscodestar-thegodproject-lambda-GodMessagesTable-183ORF0JZ5VMK')
    if (event['resource'] == "/msgs"):
        response = ddb_table.scan()
        if "ResponseMetadata" in response:
            del response["ResponseMetadata"]
        return {
            'statusCode': 200,
            'body': response,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    elif (event['resource'] == "/msg/{msgid}" and event['httpMethod'] == "GET"):
        # msgid the url parameter passed to API gateway. All the URL paramteres ap pear under pathParameters
        msgid = event['pathParameters']['msgid']
        response = ddb_table.get_item(Key={'msgid':str(msgid)})
        if 'Item' in response:
            # If there is an Item key in that response then we have found the item
            item = response['Item']
        else:
            # If there is no Item key in the response then we have not found the item
            return result(400, "Msg not found")
        return result(200, item)
    elif (event['resource'] == "/msg" and event['httpMethod'] == "POST"):
        # msgid the url parameter passed to API gateway. All the URL paramteres ap pear under pathParameters
        msg_payload = json.loads(event['body'])
        put_response = ddb_table.put_item(Item={'msgid':str(uuid.uuid1()), 'value': msg_payload['msg_content']})
        return result(200, json.dumps(put_response))
    else:
        return result(500, "The resource {} is no handled by lambda. Event data: {}".format(event['resource'], json.dumps(event)))
