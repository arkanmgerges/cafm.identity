"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
from abc import ABC, abstractmethod

from src.domain_model.user.User import User


class Mailer(ABC):
    @abstractmethod
    def send(self, toEmail: str, subject: str, content: str):
        """Send an email

        Args:
            toEmail (str): The email that will receive the email
            subject (str): The subject of the email
            content (str): The content of the email
        """
