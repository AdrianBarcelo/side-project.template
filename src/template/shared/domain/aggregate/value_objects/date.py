from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Self

from template.shared.domain.aggregate.value_objects.exceptions.invalid_date import InvalidDate
from template.shared.domain.aggregate.value_objects.value_object import ValueObject


@dataclass(frozen=True)
class Date(ValueObject):
    value: date

    DATE_TIME_FORMAT = "%Y-%m-%d"

    @classmethod
    def today(cls) -> Self:
        return cls(datetime.now().date())

    @classmethod
    def from_string(cls, date_time: str, date_format: Optional[str] = None) -> Self:
        format_to_use = date_format or cls.DATE_TIME_FORMAT
        try:
            return cls(datetime.strptime(date_time, format_to_use).date())
        except ValueError:
            raise InvalidDate(date_time)

    def to_string(self, date_format: Optional[str] = None) -> str:
        format_to_use = date_format or self.DATE_TIME_FORMAT
        return self.value.strftime(format_to_use)

    @classmethod
    def create_or_null(cls, value: date | None) -> Self | None:
        if value is None:
            return None

        return cls(value)

    @classmethod
    def from_string_or_null(cls, value: str | None) -> Self | None:
        if value is None:
            return None

        return cls.from_string(value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Date) and self.value == other.value

    def __gt__(self, other: object) -> bool:
        return isinstance(other, Date) and self.value > other.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.to_string()})"
