import ssl
import smtplib
import logging

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from settings import (
    SMPT_SERVER,
    SMPT_SSL_PORT,
    SENDER_EMAIL,
    SENDER_EMAIL_PASSWORD,
    RECEIVER_EMAIL, TODAY_DATETIME,
)


def _prepare_email(email: str) -> MIMEMultipart:
    message = MIMEMultipart()

    message['Subject'] = f'Feed // {TODAY_DATETIME.strftime("%d-%b-%Y")}'
    message['From'] = SENDER_EMAIL
    message['To'] = RECEIVER_EMAIL

    message.attach(MIMEText(email, 'html'))

    return message


def send_email(email: str) -> None:
    message = _prepare_email(email)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMPT_SERVER, SMPT_SSL_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())

        logging.info('Email feed was successfully sent.')
