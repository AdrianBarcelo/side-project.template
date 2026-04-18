from template.constants import UNSET
from template.shared.domain.aggregate.value_objects.aggregate_id import AggregateId


class AggregateIdMother:
    @staticmethod
    def create(value: str = UNSET) -> AggregateId:
        if value is not UNSET:
            return AggregateId(value)

        return AggregateId.random()
