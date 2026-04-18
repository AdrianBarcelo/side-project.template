from pydantic.dataclasses import dataclass

from template.shared.domain.aggregate.value_objects.exceptions.invalid_id import InvalidId
from template.shared.domain.aggregate.value_objects.value_object import ValueObject


@dataclass(frozen=True)
class StringId(ValueObject):
    value: str

    def _assert_valid(self) -> None:
        if not isinstance(self.value, str) or not self.value:
            raise InvalidId(self.value)
