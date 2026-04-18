from abc import ABC
from typing import List

from template.shared.domain.bus.event.domain_event import DomainEvent


class AggregateRoot(ABC):
    def __init__(self) -> None:
        self._events: List[DomainEvent] = []

    def record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_domain_events(self) -> List[DomainEvent]:
        events = self._events
        self._events = []
        return events
