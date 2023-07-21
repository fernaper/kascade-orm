import os

from pydantic import validator
from pydantic_settings import BaseSettings
from typing import Optional

from kascade import enums

KASCADE_ENV_FILE = os.getenv('KASCADE_ENV_FILE', '.env')


class DatabaseSettings(BaseSettings):
    pass


class MySQLSettings(DatabaseSettings):
    host: str = 'localhost'
    port: int = 3306
    username: str = 'root'
    password: str = 'root'
    database: str = 'kascade'


class PostgreSQLSettings(DatabaseSettings):
    host: str = 'localhost'
    port: int = 5432
    username: str = 'root'
    password: str = 'root'
    database: str = 'kascade'


class SQLiteSettings(DatabaseSettings):
    path: str = 'kascade.db'


class Settings(BaseSettings):
    engine: enums.Engine = enums.Engine.sqlite
    engine_settings: Optional[DatabaseSettings] = None

    @validator('engine_settings', pre=True)
    def set_engine_settings(cls, v, values):
        if v is not None:
            if not isinstance(v, DatabaseSettings):
                raise ValueError('Invalid engine settings')
            return v

        settings = None
        if values['engine'] == enums.Engine.mysql:
            settings =  MySQLSettings
        elif values['engine'] == enums.Engine.postgresql:
            settings = PostgreSQLSettings
        elif values['engine'] == enums.Engine.sqlite:
            settings = SQLiteSettings

        if settings is None:
            raise ValueError('Invalid engine')

        return settings(
            _env_prefix='KASCADE_',
            _env_file=KASCADE_ENV_FILE,
            _env_file_encoding='utf-8',
        )


settings = Settings(
    _env_prefix='KASCADE_',
    _env_file=KASCADE_ENV_FILE,
    _env_file_encoding='utf-8'
)
