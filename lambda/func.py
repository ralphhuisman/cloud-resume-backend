import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VisitorCountTable-Test')

    try:
        # Update the visitor count in the DynamoDB table.
        response = table.update_item(
            Key={'CounterId': 'SiteTotal'},
            UpdateExpression='ADD #count :inc',
            ExpressionAttributeNames={'#count': 'Count'},
            ExpressionAttributeValues={':inc': Decimal(1)},
            ReturnValues='UPDATED_NEW'
        )
        # Convert the Decimal object to int for JSON serialization.
        response['Attributes']['Count'] = int(response['Attributes']['Count'])
        return {
            'statusCode': 200,
            'body': json.dumps(response['Attributes'])
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps("Error updating the visitor count")
        }
