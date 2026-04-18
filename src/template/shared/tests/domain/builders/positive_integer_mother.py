from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.positive_integer import PositiveInteger
from template.shared.domain.utils import Utils


class PositiveIntegerMother:
    @staticmethod
    def create(value: int = UNSET) -> PositiveInteger:
        if value is not UNSET:
            return PositiveInteger(value)

        return PositiveInteger(Utils.random_int(1, 1000))
