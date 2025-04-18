from typing import ClassVar

from .base import BaseServiceException, HttpStatusCode, EntityMessage


class NotFoundException(BaseServiceException):
    #TODO: сделать фабрику для подобных exception
    status_code = HttpStatusCode.NOT_FOUND
    entity_name: ClassVar[str] = EntityMessage()

    @property
    def message(self):
        return f'{self.entity_name} not found'


class ChatNotFoundException(NotFoundException):
    entity_name = 'chat'

class GroupNotFoundException(NotFoundException):
    entity_name = 'group'

class MessageNotFoundException(NotFoundException):
    entity_name = 'message'

class UserNotFoundException(NotFoundException):
    entity_name = 'user'
