from enum import Enum, auto


class StrEnum(Enum):
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list[str],
    ):
        return name


class Engine(StrEnum):
    mysql = auto()
    postgresql = auto()
    sqlite = auto()


class ColumnTypes(StrEnum):
    null = auto()
    integer = auto()
    real = auto()
    text = auto()
    blob = auto()
    boolean = auto()
    date = auto()
    datetime = auto()
    time = auto()
    timestamp = auto()
