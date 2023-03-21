import os

import boto3
from slack_sdk import WebClient


def lambda_handler(event, context):
    # AWS Lambda 환경변수 사용 시, 아래와 같이 environ 객체 사용
    QUEUE_URL = os.environ.get("SQS_QUEUE_URL")
    sqs = boto3.client("sqs")

    if "Records" in event:
        message = event["Records"][0]
        receipt_handle = message["receiptHandle"]
        payload = message["body"]

        try:
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt_handle)
            print("메세지 전송!")
            slack_post_message(text=payload)
            print("이상없음")
        except Exception as e:
            print("에러!")
            print(e)
            slack_post_message(text=str(e))

        return {"statusCode": 200, "body": payload}
    else:
        print("메세지 없음!")
        slack_post_message(text="메세지 없음!")

        return {"statusCode": 500, "body": "메세지 없음!"}


def slack_post_message(text):
    SLACK_OAUTH_TOKEN = os.environ.get("SLACK_OAUTH_TOKEN")
    SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

    slack_bot_client = WebClient(token=SLACK_OAUTH_TOKEN)

    return slack_bot_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=text)
