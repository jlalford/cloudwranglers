import os
import smtplib
from email.message import EmailMessage


class SMTPClient:
    """A simple SMTP client for sending emails."""

    def __init__(self, host=None, port=None, username=None, password=None, use_tls=True):
        self.host = host or os.getenv("SMTP_HOST", "localhost")
        self.port = int(port or os.getenv("SMTP_PORT", 587))
        self.username = username or os.getenv("SMTP_USERNAME")
        self.password = password or os.getenv("SMTP_PASSWORD")
        self.use_tls = use_tls

    def send_mail(self, sender, recipients, subject, body):
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = ", ".join(recipients) if isinstance(recipients, (list, tuple)) else recipients
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(self.host, self.port) as smtp:
            if self.use_tls:
                smtp.starttls()
            if self.username and self.password:
                smtp.login(self.username, self.password)
            smtp.send_message(msg)


def send_email(to_address, subject, message, sender=None):
    """Convenience function using environment configuration."""
    sender = sender or os.getenv("SMTP_FROM", "no-reply@example.com")
    client = SMTPClient()
    client.send_mail(sender, to_address, subject, message)


if __name__ == "__main__":
    # Example usage for manual testing
    send_email("recipient@example.com", "Test Email", "This is a test email.")
