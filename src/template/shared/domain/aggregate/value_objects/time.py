from dataclasses import dataclass
from typing import Self

from template.shared.domain.aggregate.value_objects.exceptions.invalid_milliseconds import InvalidMilliseconds
from template.shared.domain.aggregate.value_objects.exceptions.invalid_minutes import InvalidMinutes
from template.shared.domain.aggregate.value_objects.exceptions.invalid_seconds import InvalidSeconds
from template.shared.domain.aggregate.value_objects.exceptions.time_not_valid import InvalidTime
from template.shared.domain.aggregate.value_objects.value_object import ValueObject


@dataclass(frozen=True)
class Time(ValueObject):
    value: None = None
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0

    def _assert_valid(self) -> None:
        if not (0 <= self.minutes < 60):
            raise InvalidMinutes(self.minutes)

        if not (0 <= self.seconds < 60):
            raise InvalidSeconds(self.seconds)

        if not (0 <= self.milliseconds < 1000):
            raise InvalidMilliseconds(self.milliseconds)

    @classmethod
    def from_string(cls, time: str) -> Self:
        try:
            minutes, seconds = time.split(":")
            seconds, milliseconds = seconds.split(".")
            return cls(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
        except Exception:
            raise InvalidTime(time)

    @classmethod
    def from_string_or_null(cls, time: str | None) -> Self | None:
        if not time:
            return None

        try:
            minutes, seconds = time.split(":")
            seconds, milliseconds = seconds.split(".")
            return cls(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
        except Exception:
            raise InvalidTime(time)

    def to_string(self) -> str:
        return f"{self.minutes:02}:{self.seconds:02}.{self.milliseconds:03}"
