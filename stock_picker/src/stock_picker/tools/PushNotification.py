from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from twilio.rest import Client
from dotenv import load_dotenv
import os


class PushNotificationModel(BaseModel):
    """Input schema for MyCustomTool."""

    message: str = Field(
        ..., description="The message to be sent in the push notification."
    )


class PushNotificationTool(BaseTool):
    name: str = "Push Notification Tool"
    description: str = (
        "Tool for sending push notifications, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = PushNotificationModel

    def _run(self, message: str) -> str:
        """Sends a push notification with the given message."""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_FROM_NUMBER")
        to_number = os.getenv("TWILIO_TO_NUMBER")

        client = Client(account_sid, auth_token)
        try:
            client.messages.create(body=message, from_=from_number, to=to_number)
            return "Push notification sent successfully."
        except Exception as e:
            return f"Failed to send push notification: {str(e)}"
