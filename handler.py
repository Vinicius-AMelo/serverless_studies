import json
import boto3
import botocore.exceptions as exception


def hello(event, context):
    s3_client = boto3.client("s3")
    dynamo_client = boto3.client("dynamodb")

    try:
        # anomaly = event["body"]["anomaly"]
        # company = event["body"]["company"]
        # start_timestamp = event["queryStringParameters"]["start"]
        # end_timestamp = event["queryStringParameters"]["end"]
        # file_name = f"results_{anomaly}_{start_timestamp}_{end_timestamp}.json"

        start_timestamp = "2024-05-01"
        end_timestamp = "2024-05-21"
        partition_key = "0"
        region = "sa-east-1"
        table_name = "predictions_1234"
        bucket_name = "serverless-study"
        file_name = f"results_{start_timestamp}_{end_timestamp}.json"

        response = dynamo_client.query(
            TableName=table_name,
            KeyConditionExpression="id = :id AND #ts BETWEEN :start AND :end",
            ExpressionAttributeNames={
                "#ts": "timestamp",
                "#idx": "index",
                "#tsh": "threshold",
            },
            ExpressionAttributeValues={
                ":id": {"S": partition_key},
                ":start": {"S": start_timestamp},
                ":end": {"S": end_timestamp},
            },
            ProjectionExpression="#idx, #tsh, #ts",
        )

        data = json.dumps(response)
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=data)

        response_body = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "JSON saved successfully",
                    "url": f"https://{bucket_name}.s3.{region}.amazonaws.com/{file_name}",
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
