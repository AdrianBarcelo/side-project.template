from datetime import date, timedelta

from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.date import Date


class DateMother:
    @staticmethod
    def create(value: date = UNSET) -> Date:
        if value is not UNSET:
            return Date(value)

        return Date.today()

    @classmethod
    def today(cls) -> Date:
        return Date.today()

    @classmethod
    def yesterday(cls) -> Date:
        return Date(date.today() - timedelta(days=1))

    @classmethod
    def tomorrow(cls) -> Date:
        return Date(date.today() + timedelta(days=1))

    @classmethod
    def random_past(cls, days_ago: int = 30) -> Date:
        return Date(date.today() - timedelta(days=days_ago))

    @classmethod
    def from_string(cls, date_string: str) -> Date:
        return Date.from_string(date_string)
