from typing import Type

from template.shared.domain.bus.event.domain_event import DomainEvent
from template.shared.domain.bus.event.event_bus import EventBus
from template.shared.domain.bus.event.event_handler import EventHandler


class InMemoryEventBus(EventBus):
    HANDLERS: dict[Type[DomainEvent], set[Type[EventHandler]]] = {
        # TODO: registrar event handlers aquí
        # Ejemplo:
        # ExampleCreated: {HandleExampleCreated},
    }

    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            handlers: set[Type[EventHandler]] = self.HANDLERS.get(event.__class__, set())
            for handler in handlers:
                handler().handle(event)

        self.flush()

    def flush(self) -> None:
        self._events.clear()
