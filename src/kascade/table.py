from pydantic import BaseModel, validator
from typing import Dict, List, Optional
from typing_extensions import Self


from kascade import enums


class Column(BaseModel):
    name: str
    type: enums.ColumnTypes


class Table(BaseModel):

    @classmethod
    def get_table_name(cls) -> str:
        return cls.__name__.lower()
