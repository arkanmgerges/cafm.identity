"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import (
    UnAuthorizedException,
)
from src.domain_model.user.User import User
from src.port_adapter.email.Mailer import Mailer
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.common.handler.Handler import Handler
from src.resource.common.DateTimeHelper import DateTimeHelper
from src.resource.logging.logger import logger


class SendEmailOneTimeUserPasswordHandler(Handler):
    def __init__(self):
        self._commandConstant = CommonCommandConstant.SEND_EMAIL_ONE_TIME_USER_PASSWORD

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleMessage(self, messageData: dict, extraData: dict = None) -> dict:
        name = messageData["name"]
        data = messageData["data"]
        metadata = messageData["metadata"]

        logger.debug(
            f"[{SendEmailOneTimeUserPasswordHandler.handleMessage.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}"
        )
        appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if "token" not in metadataDict:
            raise UnAuthorizedException()

        obj: User = appService.userById(
            id=dataDict["user_id"], token=metadataDict["token"]
        )
        email = obj.email()
        domain = email[email.rfind('.') + 1:]
        if domain in ['test', 'me', 'local']:
            return None

        password = obj.stripOneTimePasswordTag()
        content = f"Hi, this is your one time login password <strong>{password}</strong>, use it to login and to create new one"

        mailer: Mailer = AppDi.instance.get(Mailer)
        mailer.send(
            toEmail=obj.email(),
            subject="CAFM User Creation - One time login password",
            content=content,
        )

        return {
            "name": self._commandConstant.value,
            "created_on": DateTimeHelper.utcNow(),
            "data": obj.toMap(),
            "metadata": metadataDict,
        }
