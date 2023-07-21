import types

from pydantic import BaseModel
from typing import Optional, Type

import enums

from config import settings as default_settings, Settings

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


class Kascade(BaseModel):
    settings: Optional[Settings] = None
    _connection = None

    async def _connect(self):
        settings = self.settings if self.settings is not None else default_settings

        if settings.engine == enums.Engine.mysql:
            pass
        elif settings.engine == enums.Engine.postgresql:
            pass
        elif settings.engine == enums.Engine.sqlite:
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

    async def __aenter__(self):
        await self._connect()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType]
    ):
        await self._disconnect()

    async def create_table(self):
        pass

    def find(self):
        pass

    def find_many(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def create_many(self):
        pass

    def update_many(self):
        pass

    def count(self):
        pass
