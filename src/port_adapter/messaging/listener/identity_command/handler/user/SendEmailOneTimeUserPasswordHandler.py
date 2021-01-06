"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import json
import time

import src.port_adapter.AppDi as AppDi
from src.application.UserApplicationService import UserApplicationService
from src.domain_model.resource.exception.UnAuthorizedException import UnAuthorizedException
from src.domain_model.user.User import User
from src.port_adapter.email.Mailer import Mailer
from src.port_adapter.messaging.listener.CommandConstant import CommonCommandConstant
from src.port_adapter.messaging.listener.identity_command.handler.Handler import Handler
from src.resource.logging.logger import logger


class SendEmailOneTimeUserPasswordHandler(Handler):

    def __init__(self):
        self._commandConstant = CommonCommandConstant.SEND_EMAIL_ONE_TIME_USER_PASSWORD

    def canHandle(self, name: str) -> bool:
        return name == self._commandConstant.value

    def handleCommand(self, messageData: dict) -> dict:
        name = messageData['name']
        data = messageData['data']
        metadata = messageData['metadata']

        logger.debug(
            f'[{SendEmailOneTimeUserPasswordHandler.handleCommand.__qualname__}] - received args:\ntype(name): {type(name)}, name: {name}\ntype(data): {type(data)}, data: {data}\ntype(metadata): {type(metadata)}, metadata: {metadata}')
        appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
        dataDict = json.loads(data)
        metadataDict = json.loads(metadata)

        if 'token' not in metadataDict:
            raise UnAuthorizedException()

        obj: User = appService.userById(id=dataDict['id'], token=metadataDict['token'])
        password = obj.stripOneTimePasswordTag()
        content = f'Hi, this is your one time login password <strong>{password}</strong>, use it to login and to create new one'

        mailer: Mailer = AppDi.instance.get(Mailer)
        mailer.send(toEmail=obj.email(), subject='CAFM User Creation - One time login password', content=content)

        return {'name': self._commandConstant.value, 'created_on': round(time.time() * 1000),
                'data': {'id': obj.id(), 'email': obj.email()},
                'metadata': metadataDict}

