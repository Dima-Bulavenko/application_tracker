"""Email service repository interface."""

from abc import ABC, abstractmethod

from pydantic import BaseModel


class EmailMessage(BaseModel):
    """Email message data structure."""

    to_emails: list[str]
    subject: str
    body: str
    html_body: str | None = None
    from_email: str | None = None


class IEmailService(ABC):
    """Repository interface for email service.

    This interface defines the contract for email sending capabilities
    without specifying the implementation details. Concrete implementations
    should be placed in the infrastructure layer.
    """

    @abstractmethod
    async def send_email(self, message: EmailMessage) -> bool:
        """Send an email message.

        Args:
            message: The email message to send

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        ...
