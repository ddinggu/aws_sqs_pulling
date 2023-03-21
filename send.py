import os

import boto3
from dotenv import load_dotenv

# 환경변수 값 불러오기
load_dotenv()


client = boto3.client("sqs")
queue_url = os.getenv("SQS_QUEUE_URL")

body = "데이터"
attr = {"Key": {"StringValue": "Value", "DataType": "String"}}

try:
    response = client.send_message(
        QueueUrl=queue_url, MessageBody=body, MessageAttributes=attr
    )
    print(response)
except client.exceptions.InvalidMessageContents as e:
    print(f"Failed to deliver event to SQS: Invalid Message Contents ({queue_url}: {e}")
except client.exceptions.ClientError as e:
    print(f"Failed to deliver event to SQS ({queue_url}: {e}")
