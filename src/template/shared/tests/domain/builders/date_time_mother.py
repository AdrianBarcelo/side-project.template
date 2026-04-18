from datetime import UTC, datetime, timedelta

from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.date_time import DateTime


class DateTimeMother:
    @staticmethod
    def create(value: datetime = UNSET) -> DateTime:
        if value is not UNSET:
            return DateTime(value)

        return DateTime.now()

    @classmethod
    def now(cls) -> DateTime:
        return DateTime.now()

    @classmethod
    def random_past(cls, hours_ago: int = 24) -> DateTime:
        return DateTime(datetime.now(tz=UTC) - timedelta(hours=hours_ago))

    @classmethod
    def random_future(cls, hours_ahead: int = 24) -> DateTime:
        return DateTime(datetime.now(tz=UTC) + timedelta(hours=hours_ahead))

    @classmethod
    def from_string(cls, date_time_string: str) -> DateTime:
        return DateTime.from_string(date_time_string)
