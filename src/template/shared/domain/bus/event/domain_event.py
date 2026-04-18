from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, fields
from datetime import datetime, timezone
from typing import Self
from uuid import uuid4

from template.shared.domain.aggregate.value_objects.date_time import DateTime
from template.shared.domain.utils import Utils


@dataclass(frozen=True, kw_only=True)
class DomainEvent(ABC):
    aggregate_id: str | None = None
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_on: str = field(
        default_factory=lambda: DateTime(datetime.now(tz=timezone.utc)).to_string()
    )

    @property
    def event_name(self) -> str:
        return self.get_event_name()

    @classmethod
    def get_event_name(cls) -> str:
        return Utils.from_pascal_to_kebab_case(cls.__name__)

    @classmethod
    def full_event_name(cls) -> str:
        return f"{cls.aggregate_name()}.{cls.get_event_name()}"

    def to_primitives(self) -> dict:
        return asdict(self)

    @classmethod
    def from_primitives(cls, data: dict) -> Self:
        event_attributes_name = {f.name for f in fields(cls)}
        event_properties_in_dict = {
            key: value for key, value in data.items() if key in event_attributes_name
        }
        return cls(**event_properties_in_dict)

    @classmethod
    @abstractmethod
    def aggregate_name(cls) -> str:
        ...
