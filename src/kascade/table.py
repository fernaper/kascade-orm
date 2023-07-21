from pydantic import BaseModel, validator
from typing import Dict, List, Optional

from kascade import enums


class Column(BaseModel):
    name: str
    type: enums.ColumnTypes


class Table(BaseModel):
    table_name: Optional[str] = None

    @validator('table_name', pre=True, always=True)
    def use_class_name_by_default(cls, v, values):
        if v is None:
            return cls.__name__.lower()
        return v
