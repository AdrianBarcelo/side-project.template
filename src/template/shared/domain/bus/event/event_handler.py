from abc import ABC, abstractmethod

from template.shared.domain.bus.event.domain_event import DomainEvent


class EventHandler(ABC):
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        ...
