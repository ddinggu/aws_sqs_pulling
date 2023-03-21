import os
from time import sleep

import boto3
from dotenv import load_dotenv

load_dotenv()

sqs_client = boto3.client("sqs")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# SNS가 자동으로 SQS의 큐 메세지를 Pulling하지 않으므로, 수동으로 Pulling 후 SNS로 전달
sns_client = boto3.client("sns")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")


def pulling_q_message():
    try:
        queue_msg_response = sqs_client.receive_message(QueueUrl=SQS_QUEUE_URL)

        if "Messages" in queue_msg_response:
            for message in queue_msg_response["Messages"]:
                q_message = message["Body"]
                # print(f"Received and deleted message: {q_message}")
                # 큐의 메세지를 제거하기 위해선 messageId가 아닌, ReceiptHandle값이 필요(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/message/delete.html)
                receipt_handle = message["ReceiptHandle"]
                q_message_id = message["MessageId"]

                # SNS는 SQS 큐를 자동으로 Pulling하는 방법이 없으므로 직접 데이터를 받아서 Publish
                response = sns_client.publish(TopicArn=SNS_TOPIC_ARN, Message=q_message)
                print(
                    f"Queue Message {q_message_id} To {SNS_TOPIC_ARN}: {q_message}."
                    f"\n\n Response: {response}"
                )

                # SQS Queue에 저장된 메세지는 자동으로 제거되지 않기 때문에 수동 제거
                sqs_client.delete_message(
                    QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle
                )

        else:
            print("None Delete Message!")
    except Exception as e:
        print(e)


# Q에 쌓여있는 메세지의 수를 모르므로 재귀로 돌아갈 수 있도록 함수 실행
t = 0

while t < 100:
    pulling_q_message()
    t += 1
    sleep(5)
