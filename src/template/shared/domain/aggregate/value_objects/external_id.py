from dataclasses import dataclass

from template.shared.domain.aggregate.value_objects.string_id import StringId


@dataclass(frozen=True)
class ExternalId(StringId):
    pass
