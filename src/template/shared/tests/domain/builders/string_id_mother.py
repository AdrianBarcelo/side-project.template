from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.string_id import StringId
from template.shared.domain.utils import Utils


class StringIdMother:
    @staticmethod
    def create(value: str = UNSET) -> StringId:
        if value is not UNSET:
            return StringId(value)

        return StringId(Utils.random_string())
