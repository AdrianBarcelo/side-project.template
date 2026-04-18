from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Optional, Self

from template.shared.domain.aggregate.value_objects.value_object import ValueObject


@dataclass(frozen=True)
class DateTime(ValueObject):
    value: datetime

    DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

    @classmethod
    def now(cls) -> Self:
        return cls(datetime.now(tz=UTC))

    @classmethod
    def from_string(cls, date_time: str, date_format: Optional[str] = None) -> Self:
        format_to_use = date_format or cls.DATE_TIME_FORMAT
        return cls(datetime.strptime(date_time, format_to_use))

    @classmethod
    def from_timestamp(cls, timestamp: float) -> Self:
        return cls(datetime.fromtimestamp(timestamp, tz=UTC))

    @classmethod
    def from_string_or_null(cls, date_time: str | None, date_format: Optional[str] = None) -> Self | None:
        if date_time is None:
            return None

        return cls.from_string(date_time, date_format)

    def to_string(self, date_format: Optional[str] = None) -> str:
        format_to_use = date_format or self.DATE_TIME_FORMAT
        return self.value.strftime(format_to_use)

    @classmethod
    def create_or_null(cls, value: datetime | None) -> Self | None:
        if value is None:
            return None

        return cls(value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DateTime) and self.value == other.value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DateTime):
            return NotImplemented

        return self.value < other.value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, DateTime):
            return NotImplemented

        return self.value <= other.value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, DateTime):
            return NotImplemented

        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, DateTime):
            return NotImplemented

        return self.value >= other.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_string()})"
