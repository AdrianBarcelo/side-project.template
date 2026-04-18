from datetime import datetime
from random import choice

from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.month import Month


class MonthMother:
    @staticmethod
    def create(value: int = UNSET) -> Month:
        if value is not UNSET:
            return Month(value)

        return choice(list(Month))

    @classmethod
    def current(cls) -> Month:
        return Month(datetime.now().month)

    @classmethod
    def random(cls) -> Month:
        return choice(list(Month))
