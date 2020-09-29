"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import time

from src.application.UserApplicationService import UserApplicationService
import src.portadapter.AppDi as AppDi
from src.portadapter.messaging.listener.handler.Handler import Handler


class CreateUserHandler(Handler):

    def canHandle(self, name: str) -> bool:
        return name == 'createUser'

    def handleCommand(self, name: str, data: dict) -> dict:
        appService: UserApplicationService = AppDi.instance.get(UserApplicationService)
        obj = appService.createObjectOnly(username=data['username'], password=data['password'])
        return {'name': 'createUser', 'createdOn': time.time() * 1000, 'data': {'id': obj.id(), 'username': obj.username(), 'password': obj.password()}}