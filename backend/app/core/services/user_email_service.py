"""User email service for handling user-related email communications."""

from app.core.repositories.email_service import EmailMessage, IEmailService
from app.core.security import ITokenProvider
from app.utils.template_loader import TemplateLoader


class UserEmailService:
    """Service for handling user-related email operations.

    This service encapsulates the business logic for sending user-specific
    emails such as verification emails, welcome messages, and password resets.
    """

    def __init__(
        self,
        email_service: IEmailService,
        token_provider: ITokenProvider,
        base_url: str = "http://localhost:8000",
    ) -> None:
        """Initialize the user email service.

        Args:
            email_service: Email service implementation for sending emails
            base_url: Base URL for generating verification links
        """
        self.email_service = email_service
        self.base_url = base_url
        self.token_provider = token_provider
        self.template_loader = TemplateLoader()

    async def send_verification_email(self, email: str, user_name: str | None = None) -> bool:
        """Send email verification message to user.

        Args:
            email: User's email address
            user_name: Optional user name for personalization

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        verification_token = self.token_provider.create_verification_token(email)

        verification_url = f"{self.base_url}/verify-email?token={verification_token.token}"

        context = {
            "verification_url": verification_url,
            "user_name": user_name,
        }

        html_body = self.template_loader.render_template("emails/user_verification.html", context)
        text_body = self.template_loader.render_template("emails/user_verification.txt", context)

        message = EmailMessage(
            to_emails=[email],
            subject="Please verify your email address - Application Tracker",
            body=text_body,
            html_body=html_body,
        )

        return await self.email_service.send_email(message)
