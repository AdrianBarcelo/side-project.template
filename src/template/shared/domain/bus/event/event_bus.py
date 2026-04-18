from abc import ABC, abstractmethod

from template.shared.domain.bus.event.domain_event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    def publish(self, events: list[DomainEvent]) -> None:
        ...

    @abstractmethod
    def flush(self) -> None:
        ...
