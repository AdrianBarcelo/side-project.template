from dataclasses import dataclass

from template.shared.domain.aggregate.value_objects.uuid import Uuid


@dataclass(frozen=True)
class AggregateId(Uuid):
    pass
