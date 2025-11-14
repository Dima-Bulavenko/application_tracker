"""User email service for handling user-related email communications."""

from app import FRONTEND_ORIGIN
from app.core.dto import UserRead
from app.core.repositories.email_service import EmailMessage, IEmailService
from app.utils.template_loader import TemplateLoader

from .verification_token_service import VerificationTokenService


class UserEmailService:
    """Service for handling user-related email operations.

    This service encapsulates the business logic for sending user-specific
    emails such as verification emails, welcome messages, and password resets.
    """

    def __init__(
        self,
        email_service: IEmailService,
        verification_token_service: VerificationTokenService,
    ) -> None:
        """Initialize the user email service.

        Args:
            email_service: Email service implementation for sending emails
            base_url: Base URL for generating verification links
        """
        self.email_service = email_service
        self.verification_token_service = verification_token_service
        self.template_loader = TemplateLoader()

    async def send_verification_email(self, user: UserRead) -> bool:
        """Send email verification message to user.

        Args:
            user: User object containing email, ID, and optional first name

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        assert user.id is not None, "User ID must be set to issue verification token"
        raw_token = await self.verification_token_service.issue(user.id)
        verification_url = f"{FRONTEND_ORIGIN}/verify-email?token={raw_token}"

        context = {
            "verification_url": verification_url,
            "user_name": user.first_name or "User",
        }

        html_body = self.template_loader.render_template("emails/user_verification.html", context)
        text_body = self.template_loader.render_template("emails/user_verification.txt", context)

        message = EmailMessage(
            to_emails=[user.email],
            subject="Please verify your email address - Application Tracker",
            body=text_body,
            html_body=html_body,
        )

        return await self.email_service.send_email(message)

    async def send_duplicate_registration_warning(self, email: str) -> bool:
        """Send warning email when someone tries to register with an existing email.

        Args:
            email: Email address that someone tried to register with

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # Link to the frontend sign-in page
        login_url = f"{FRONTEND_ORIGIN}/sign-in"

        context = {
            "email": email,
            "login_url": login_url,
        }

        html_body = self.template_loader.render_template("emails/duplicate_registration_warning.html", context)
        text_body = self.template_loader.render_template("emails/duplicate_registration_warning.txt", context)

        message = EmailMessage(
            to_emails=[email],
            subject="Account Security Alert - Application Tracker",
            body=text_body,
            html_body=html_body,
        )

        return await self.email_service.send_email(message)
