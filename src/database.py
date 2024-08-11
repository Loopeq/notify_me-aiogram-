import asyncio
import datetime
from typing import List

import aiosqlite
from pathlib import Path

from aiosqlite import cursor, Cursor

from settings import logger
from src.models import UserDTO, NotificationDTO, NotificationGetDTO, RunningSessionDTO, RunningSessionGetDTO

CURRENT_PATH = Path(__file__).resolve()
ROOT = CURRENT_PATH.parent.parent
DB_PATH = ROOT / "storage.db"


class ORM(object):

    @staticmethod
    async def setup():
        async with aiosqlite.connect(database=DB_PATH) as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS UserConfig(
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE, 
                username TEXT NOT NULL UNIQUE,
                language TEXT NOT NULL, 
                created_at TIMESTAMP
                )""")

            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS Notifications(
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                minutes INTEGER NOT NULL,
                title TEXT NOT NULL DEFAULT Hey, 
                created_at TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES UserConfig(user_id)
                )
                """
            )
            await db.execute(
                """CREATE TABLE IF NOT EXISTS RunningSession(
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                notification_id NOT NULL UNIQUE,
                created_at TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES UserConfig(user_id),
                FOREIGN KEY(notification_id) REFERENCES Notifications(id))
                """
            )
            await db.commit()

    @staticmethod
    async def insert_user_config(user: UserDTO):
        async with aiosqlite.connect(database=DB_PATH) as db:
            try:
                cur: cursor = await db.execute(
                    "SELECT * FROM UserConfig WHERE user_id = ?",
                    (user.user_id,)
                )

                exist_user = await cur.fetchone()

                if exist_user is not None:
                    await db.execute(
                        "UPDATE UserConfig SET language = ? WHERE user_id = ?",
                        (user.language, user.user_id)
                    )
                    await db.commit()
                    return

                await db.execute(
                    "INSERT INTO UserConfig(user_id, username, language, created_at) VALUES(?, ?, ?, ?)",
                    (user.user_id, user.username, user.language, user.created_at)
                )

                await db.commit()

            except Exception as error:
                pass

    @staticmethod
    async def select_user_language(user_id: int):
        async with aiosqlite.connect(database=DB_PATH) as db:
            cur: cursor = await db.execute("SELECT language FROM UserConfig WHERE user_id = ?",
                                           (user_id,))
            language = await cur.fetchone()
            return language[0]

    @staticmethod
    async def insert_notification(notification: NotificationDTO):
        async with aiosqlite.connect(database=DB_PATH) as db:
            try:

                cur: Cursor = await db.execute("INSERT INTO Notifications(user_id, minutes, title, created_at)"
                                               "VALUES(?, ?, ?, ?)",
                                               (notification.user_id, notification.minutes, notification.title,
                                                notification.created_at))
                not_id = cur.lastrowid
                await db.commit()
                return not_id

            except Exception as error:
                pass

    @staticmethod
    async def select_user_notifications(user_id: int) -> List[NotificationGetDTO]:
        async with aiosqlite.connect(database=DB_PATH) as db:
            conn: cursor = await db.execute("SELECT * FROM Notifications WHERE user_id = ?",
                                            (user_id,))
            notifications = await conn.fetchall()
            result = []
            for notification in notifications:
                result.append(NotificationGetDTO(id=notification[0], user_id=notification[1], minutes=notification[2],
                                                 title=notification[3], created_at=notification[4]))
            return result

    @staticmethod
    async def select_notification_by_id(not_id: int) -> NotificationGetDTO:
        async with aiosqlite.connect(database=DB_PATH) as db:
            conn: cursor = await db.execute("SELECT * FROM Notifications WHERE id=?",
                                            (not_id,))
            notification = await conn.fetchone()
            return NotificationGetDTO(id=notification[0], user_id=notification[1], minutes=notification[2],
                                      title=notification[3], created_at=notification[4])

    @staticmethod
    async def update_running_session(session: RunningSessionDTO,
                                     max_user_sessions: int = 3) -> bool:
        async with aiosqlite.connect(database=DB_PATH) as db:
            conn: Cursor = await db.execute('SELECT * FROM RunningSession WHERE user_id = ?',
                                            (session.user_id,))
            sessions = await conn.fetchall()
            sessions = list(sessions)
            if len(sessions) <= max_user_sessions - 1:
                await db.execute(
                    "INSERT INTO RunningSession(user_id, notification_id, created_at) VALUES(?, ?, ?)",
                    (session.user_id, session.notification_id, session.created_at)
                )
                await db.commit()
                return True
            return False

    @staticmethod
    async def get_running_session(user_id: int) -> RunningSessionGetDTO | None:
        async with aiosqlite.connect(database=DB_PATH) as db:
            conn: cursor = await db.execute("SELECT * FROM RunningSession WHERE user_id=?",
                                            (user_id,))
            notification = await conn.fetchone()
            if not notification:
                return
            return RunningSessionGetDTO(id=notification[0], user_id=notification[1],
                                        notification_id=notification[2],
                                        created_at=notification[3])

    @staticmethod
    async def kill_running_session(notification_id: int):
        async with aiosqlite.connect(database=DB_PATH) as db:
            await db.execute("DELETE FROM RunningSession WHERE notification_id=?",
                             (notification_id, ))
            await db.commit()

    @staticmethod
    async def delete_notification_by_id(not_id: int):
        async with aiosqlite.connect(database=DB_PATH) as db:
            await db.execute("DELETE FROM Notifications WHERE id=?",
                             (not_id,))
            await db.commit()
            await ORM.kill_running_session(notification_id=not_id)



async def get_logg():
    await ORM.setup()


if __name__ == "__main__":
    asyncio.run(get_logg())
