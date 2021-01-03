"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.port_adapter.email.Mailer import Mailer


class SendGrid(Mailer):
    def __init__(self):
        self._apiClientCode = os.getenv('SENDGRID_API_KEY',
                                        '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')
        self._fromEmail = os.getenv('CAFM_SEND_GRID_FROM_EMAIL', 'bounces+19695021@em5198.supercafm.com')

    def send(self, toEmail: str, subject: str, content: ''):
        message = Mail(
            from_email=self._fromEmail,
            to_emails=toEmail,
            subject=subject,
            html_content=content)
        sg = SendGridAPIClient(self._apiClientCode)
        _response = sg.send(message)
