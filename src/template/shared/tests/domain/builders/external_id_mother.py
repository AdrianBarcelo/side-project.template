from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.external_id import ExternalId
from template.shared.domain.utils import Utils


class ExternalIdMother:
    @staticmethod
    def create(value: str = UNSET) -> ExternalId:
        if value is not UNSET:
            return ExternalId(value)

        return ExternalId(Utils.random_string())

    @classmethod
    def random(cls) -> ExternalId:
        return ExternalId(Utils.random_string())

    @classmethod
    def numeric(cls) -> ExternalId:
        return ExternalId(str(Utils.random_int(100000, 999999)))
