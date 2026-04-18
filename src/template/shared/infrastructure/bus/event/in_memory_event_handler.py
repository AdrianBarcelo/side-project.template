from abc import abstractmethod
from typing import Generic, TypeVar

from template.shared.domain.bus.command.command import Command
from template.shared.domain.bus.event.domain_event import DomainEvent
from template.shared.domain.bus.event.event_handler import EventHandler

TDomainEvent = TypeVar("TDomainEvent", bound=DomainEvent)


class InMemoryEventHandler(EventHandler, Generic[TDomainEvent]):
    def handle(self, event: DomainEvent) -> None:
        from template.shared.infrastructure.dependencies_container import DependenciesContainer

        for command in self.get_commands(event):  # type: ignore[arg-type]
            DependenciesContainer().command_bus.dispatch(command)  # type: ignore[call-arg]

    @abstractmethod
    def get_commands(self, event: TDomainEvent) -> list[Command]:
        ...
