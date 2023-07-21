import types

from abc import abstractmethod
from pydantic import BaseModel
from typing import Optional, Type

from kascade import enums

from kascade.config import settings as default_settings, Settings

try:
    import aiomysql
    AIOMYSQL = True
except ImportError:
    AIOMYSQL = False

try:
    import asyncpg
    ASYNCPG = True
except ImportError:
    ASYNCPG = False

try:
    import aiosqlite
    AIOSQLITE = True
except ImportError:
    AIOSQLITE = False


class BaseKascade(BaseModel):
    settings: Optional[Settings] = None
    _connection = None

    @abstractmethod
    async def _connect(self):
        raise NotImplementedError

    @abstractmethod
    async def _disconnect(self):
        raise NotImplementedError

    async def __aenter__(self) -> 'BaseKascade':
        await self._connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType]
    ) -> None:
        await self._disconnect()


class SqliteKascade(BaseKascade):

    async def _connect(self):
        settings = self.settings if self.settings is not None else default_settings
        if not AIOSQLITE:
            raise ImportError(
                'aiosqlite is not installed. '
                'Please install it with `pip install aiosqlite`'
            )

        self._connection = await aiosqlite.connect(
            settings.engine_settings.path
        )

    async def _disconnect(self):
        if self._connection is not None:
            await self._connection.close()
            self._connection = None


class MysqlKascade(BaseKascade):
    pass


class PostgresqlKascade(BaseKascade):
    pass


Kascade: Type[BaseKascade] = SqliteKascade
if default_settings.engine == enums.Engine.mysql:
    Kascade: Type[BaseKascade] = MysqlKascade
elif default_settings.engine == enums.Engine.postgresql:
    Kascade: Type[BaseKascade] = PostgresqlKascade
