import datetime

from pydantic import BaseModel


class UserDTO(BaseModel):
    user_id: int
    username: str
    language: str
    created_at: datetime.datetime


class UserGetDTO(UserDTO):
    id: int


class NotificationDTO(BaseModel):
    user_id: int
    minutes: int
    title: str
    created_at: datetime.datetime


class NotificationGetDTO(NotificationDTO):
    id: int

class RunningSessionDTO(BaseModel):
    user_id: int
    notification_id: int
    created_at: datetime.datetime


class RunningSessionGetDTO(RunningSessionDTO):
    id: int


