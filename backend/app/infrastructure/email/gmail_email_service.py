"""Development email service implementation."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app import env
from app.core.repositories.email_service import EmailMessage, IEmailService

EMAIL_USER = env.str("EMAIL_USER")
EMAIL_PASSWORD = env.str("EMAIL_PASSWORD")


class GmailEmailService(IEmailService):
    async def send_email(self, message: EmailMessage) -> bool:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.subject
        msg["From"] = message.from_email or EMAIL_USER
        msg["To"] = ", ".join(message.to_emails)

        # Plain text part (fallback)
        text_part = MIMEText(message.body, "plain")
        msg.attach(text_part)

        # HTML part (optional)
        if message.html_body:
            html_part = MIMEText(message.html_body, "html")
            msg.attach(html_part)
        try:
            # Send email securely
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASSWORD)
                smtp.send_message(msg)
        except Exception:
            return False

        return True
