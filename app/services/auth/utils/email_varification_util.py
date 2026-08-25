import secrets
import smtplib
from email.message import EmailMessage

from app.core import get_settings
settings = get_settings()



class EmailVerificationUtil:

    @staticmethod
    def generate_otp() -> str:

        return f"{secrets.randbelow(1_000_000):06d}"


    @staticmethod
    def send_otp(recipient: str, otp: str) -> None:

        message = EmailMessage()

        message["Subject"] = "ExperimentOS Email Verification"
        message["From"] = settings.SMTP_USERNAME
        message["To"] = recipient

        message.set_content(
            f"""
Your ExperimentOS verification code is:

{otp}

This code will expire shortly.

If you did not request this code, you can safely ignore this email.
""".strip()
        )

        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
        ) as smtp:

            smtp.starttls()
            smtp.login(
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
            )

            smtp.send_message(message)