from pydantic import BaseModel

import enums


class Column(BaseModel):
    name: str
    type: enums.ColumnTypes


class Table(BaseModel):
    name: str
    columns: list[Column]
    metadata: dict
