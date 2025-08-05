"""Development email service implementation."""

from app.core.repositories.email_service import EmailMessage, IEmailService


class DevelopmentEmailService(IEmailService):
    """Development email service that outputs emails to terminal.

    This implementation is useful during development as it allows you to see
    what emails would be sent without actually sending them to real email addresses.
    """

    def __init__(self, enable_colors: bool = True):
        """Initialize the development email service.

        Args:
            enable_colors: Whether to use ANSI color codes for terminal output
        """
        self.enable_colors = enable_colors
        self.email_count = 0

    async def send_email(self, message: EmailMessage) -> bool:
        """Send email by printing it to terminal.

        Args:
            message: The email message to "send"

        Returns:
            bool: Always returns True (simulates successful sending)
        """
        try:
            self.email_count += 1

            # Print email to terminal with formatting
            self._print_email_details(message)
            self._print_email_body(message)

            return True

        except Exception as e:
            self._print_error(f"Failed to 'send' email: {e}")
            return False

    def _print_email_details(self, message: EmailMessage) -> None:
        """Print email metadata (to, from, subject)."""
        from_email = message.from_email or "noreply@applicationtracker.dev"
        to_emails = ", ".join(message.to_emails)

        if self.enable_colors:
            print(f"{self._color('yellow', 'From:')} {from_email}")
            print(f"{self._color('yellow', 'To:')} {to_emails}")
            print(f"{self._color('yellow', 'Subject:')} {message.subject}")
        else:
            print(f"From: {from_email}")
            print(f"To: {to_emails}")
            print(f"Subject: {message.subject}")

        print("-" * 40)

    def _print_email_body(self, message: EmailMessage) -> None:
        """Print email body content."""
        if self.enable_colors:
            print(f"{self._color('green', 'TEXT BODY:')}")
        else:
            print("TEXT BODY:")

        print(message.body)

        if message.html_body:
            print()
            if self.enable_colors:
                print(f"{self._color('blue', 'HTML BODY:')}")
            else:
                print("HTML BODY:")
            print(message.html_body)

    def _print_error(self, error_message: str) -> None:
        """Print error message."""
        if self.enable_colors:
            print(f"\n{self._color('red', f'❌ ERROR: {error_message}')}\n")
        else:
            print(f"\nERROR: {error_message}\n")

    def _color(self, color: str, text: str) -> str:
        """Apply ANSI color codes to text if colors are enabled.

        Args:
            color: Color name (red, green, yellow, blue, cyan, etc.)
            text: Text to colorize

        Returns:
            str: Colorized text or plain text if colors disabled
        """
        if not self.enable_colors:
            return text

        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "cyan": "\033[96m",
            "reset": "\033[0m",
        }

        color_code = colors.get(color, "")
        reset_code = colors["reset"]

        return f"{color_code}{text}{reset_code}"
