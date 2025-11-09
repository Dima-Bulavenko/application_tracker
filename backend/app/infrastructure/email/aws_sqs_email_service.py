import aioboto3

from app import env
from app.core.repositories.email_service import EmailMessage, IEmailService

SQS_QUEUE_URL = env.str("SQS_QUEUE_URL")


class SQSEmailService(IEmailService):
    def __init__(self):
        self.session = aioboto3.Session()

    async def send_email(self, message: EmailMessage) -> bool:
        async with self.session.client("sqs") as client:
            response = await client.send_message(
                QueueUrl=SQS_QUEUE_URL, MessageBody=message.model_dump_json(exclude_none=True)
            )
        return response.get("MessageId") is not None
