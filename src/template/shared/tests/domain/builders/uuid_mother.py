from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.uuid import Uuid


class UuidMother:
    @staticmethod
    def create(value: str = UNSET) -> Uuid:
        if value is not UNSET:
            return Uuid(value)

        return Uuid.random()

    @classmethod
    def random(cls) -> Uuid:
        return Uuid.random()

    @classmethod
    def raw_uuid(cls) -> str:
        return Uuid.raw_uuid()
