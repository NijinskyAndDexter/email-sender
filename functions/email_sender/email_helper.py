import os
import boto3
from aws_lambda_powertools import Logger

sns_client = boto3.client("sns")

logger = Logger(child=True)

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

def send_email(message, subject, reply_addy):
  formatted_message = f"reply address: {reply_addy} \n\n{message}"
  logger.append_keys(subject=subject, reply_addy=reply_addy)
  logger.info("publishing message") 
  sns_response = sns_client.publish(
    TopicArn=SNS_TOPIC_ARN,
    Message=formatted_message,
    Subject=subject,
  )
  logger.info("successfully sent message", extra={"sns_message_id": sns_response["MessageId"]})