from moto import mock_dynamodb2
import unittest
import index
import json
import os
import boto3


class TestHandlerLocal(unittest.TestCase):
    def setUp(self):
        self.table_name = 'awscodestar-thegodproject-lambda-GodMessagesTable-183ORF0JZ5VMK'
        self.first_item = {}
        self.first_item["msgid"] = {"S": "1"}
        self.first_item["value"] = {"S": "Test 1"}
        self.second_item = {}
        self.second_item["msgid"] = {"S": "2"}
        self.second_item["value"] = {"S": "Test 2"}

    @mock_dynamodb2
    def __moto_setup(self):
        # setting up the dynamoDb database
        dynamodb = boto3.client('dynamodb', 'us-east-1')
        table = dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'msgid',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'msgid',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Adding item 1: {}".format(str(self.first_item)))
        dynamodb.put_item(TableName=self.table_name, Item=self.first_item)
        print("Adding item 2: {}".format(str(self.second_item)))
        dynamodb.put_item(TableName=self.table_name, Item=self.second_item)

    @mock_dynamodb2
    def test_msgs_get_event(self):
        self.__moto_setup()
        msgs_get_event_data = read_events_data('msgs_get_event.json')
        result = index.handler(msgs_get_event_data, None)
        print("Result of action get on resource /msgs/ is \n" + json.dumps(result, indent=2))
        self.assertEqual(result['statusCode'], '200')
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertEqual(result['body']["Count"], 2)
        for item in result['body']['Items']:
            self.assertEqual(item['value'], 'Test ' + item['msgid'])


def read_events_data(event_name):
    '''
    Reads the sample json event data from the events directory. 
    '''
    event_dir = os.path.abspath("events/")
    print("Reading event data from {}".format(event_dir))
    with open(os.path.join(event_dir, event_name)) as f:
        event_data = json.load(f)
    return event_data
