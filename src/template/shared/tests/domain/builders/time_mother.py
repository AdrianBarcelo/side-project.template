from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.time import Time
from template.shared.domain.utils import Utils


class TimeMother:
    @staticmethod
    def create(minutes: int = UNSET, seconds: int = UNSET, milliseconds: int = UNSET) -> Time:
        return Time(
            minutes=Utils.random_int(0, 59) if minutes is UNSET else minutes,
            seconds=Utils.random_int(0, 59) if seconds is UNSET else seconds,
            milliseconds=Utils.random_int(0, 999) if milliseconds is UNSET else milliseconds,
        )

    @classmethod
    def from_string(cls, time_string: str) -> Time:
        return Time.from_string(time_string)
