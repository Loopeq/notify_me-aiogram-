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
# """CREATE TABLE IF NOT EXISTS RunningSession(
# id INTEGER NOT NULL,
# user_id INTEGER NOT NULL UNIQUE,
# notification_id NOT NULL UNIQUE,
# created_at TIMESTAMP,
# FOREIGN KEY(user_id) REFERENCES UserConfig(user_id),
# FOREIGN KEY(notification_id) REFERENCES Notifications(id))


class RunningSessionDTO(BaseModel):
    user_id: int
    notification_id: int
    created_at: datetime.datetime


class RunningSessionGetDTO(RunningSessionDTO):
    id: int


