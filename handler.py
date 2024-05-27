import json
import boto3
import botocore.exceptions as exception


def hello(event, context):
    s3_client = boto3.client("s3")
    dynamo_client = boto3.client("dynamodb")

    try:

        partition_key = "0"
        start_timestamp = "2024-05-21 15:11:00"
        end_timestamp = "2024-05-21 15:15:00"
        table_name = "predictions_1234"

        response = dynamo_client.query(
            TableName=table_name,
            KeyConditionExpression="id = :id AND #ts BETWEEN :start AND :end",
            ExpressionAttributeNames={
                "#ts": "timestamp",
            },
            ExpressionAttributeValues={
                ":id": {"S": partition_key},
                ":start": {"S": start_timestamp},
                ":end": {"S": end_timestamp},
            },
        )

        response_body = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Go Serverless v2.0! Your function executed successfully!",
                    "table_itens": response,
                }
            ),
        }
    except exception.ClientError as e:
        response_body = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "An client error occurred!",
                    "error": e.response,
                }
            ),
        }
    except Exception as e:
        response_body = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "An exception occurred!",
                    "error": e,
                }
            ),
        }

    return response_body
