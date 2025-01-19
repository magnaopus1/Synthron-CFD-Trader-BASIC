import logging
import traceback
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging for the exception handler
logger = logging.getLogger("exception_handler")
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler("exceptions.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(console_handler)

class NotificationHandler:
    """
    Handles sending notifications for critical exceptions.
    """
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = "your_email@example.com"  # Update with your email
    EMAIL_PASSWORD = "your_email_password"    # Update with your email password
    RECIPIENTS = ["admin@example.com"]       # Update with recipient email(s)

    @staticmethod
    def send_email(subject: str, body: str):
        """
        Sends an email notification.
        
        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = NotificationHandler.EMAIL_ADDRESS
            msg['To'] = ", ".join(NotificationHandler.RECIPIENTS)
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))
            with smtplib.SMTP(NotificationHandler.SMTP_SERVER, NotificationHandler.SMTP_PORT) as server:
                server.starttls()
                server.login(NotificationHandler.EMAIL_ADDRESS, NotificationHandler.EMAIL_PASSWORD)
                server.sendmail(NotificationHandler.EMAIL_ADDRESS, NotificationHandler.RECIPIENTS, msg.as_string())
            logger.info("Critical notification email sent successfully.")
        except Exception as email_exc:
            logger.error("Failed to send email notification: %s", email_exc)

class ExceptionHandler:
    """
    Handles exceptions gracefully to prevent system crashes.
    """
    @staticmethod
    def log_and_handle_exception(exc: Exception, context: str = "Unknown"):
        """
        Logs the exception details and gracefully handles the exception.

        Args:
            exc (Exception): The exception instance.
            context (str): Context in which the exception occurred.
        """
        logger.error("Exception occurred in context '%s': %s", context, exc)
        logger.error("Traceback: %s", traceback.format_exc())

    @staticmethod
    def handle_critical_exception(exc: Exception, context: str = "Critical"):
        """
        Handles critical exceptions by logging and optionally halting execution.

        Args:
            exc (Exception): The critical exception instance.
            context (str): Context in which the exception occurred.
        """
        logger.critical("Critical exception occurred in context '%s': %s", context, exc)
        logger.critical("Traceback: %s", traceback.format_exc())
        
        # Send notification
        subject = f"Critical Exception in {context}"
        body = f"Exception: {exc}\nTraceback:\n{traceback.format_exc()}"
        NotificationHandler.send_email(subject, body)

        # Halt execution
        raise SystemExit("Critical exception encountered. Terminating the system.")

    @staticmethod
    def suppress_exceptions(exc: Exception, context: str = "Suppressed"):
        """
        Suppresses exceptions while logging them for debugging purposes.

        Args:
            exc (Exception): The exception instance.
            context (str): Context in which the exception occurred.
        """
        logger.warning("Suppressed exception in context '%s': %s", context, exc)

    @staticmethod
    def capture_and_reraise(exc: Exception, context: Optional[str] = None):
        """
        Captures, logs, and re-raises an exception.

        Args:
            exc (Exception): The exception to capture.
            context (str, optional): The context in which the exception occurred.
        """
        context = context or "Unknown Context"
        logger.error("Exception in context '%s': %s", context, exc)
        logger.error("Traceback: %s", traceback.format_exc())
        raise exc

