from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4

from template.shared.domain.aggregate.value_objects.exceptions.invalid_uuid import InvalidUuid
from template.shared.domain.aggregate.value_objects.value_object import ValueObject


@dataclass(frozen=True)
class Uuid(ValueObject):
    value: str

    def _assert_valid(self) -> None:
        super()._assert_valid()
        if not self._is_valid_uuid(self.value):
            raise InvalidUuid(self.value)

    @classmethod
    def _is_valid_uuid(cls, uuid: str) -> bool:
        try:
            UUID(uuid, version=4)
            return True
        except ValueError:
            return False

    @classmethod
    def from_primitives(cls, uuid: str) -> Self:
        return cls(uuid)

    @classmethod
    def random(cls) -> Self:
        return cls(str(uuid4()))

    @classmethod
    def raw_uuid(cls) -> str:
        return str(uuid4())
