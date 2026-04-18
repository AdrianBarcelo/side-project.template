from abc import ABC, abstractmethod

from template.shared.domain.bus.command.command import Command


class CommandBus(ABC):
    @abstractmethod
    def dispatch(self, command: Command) -> None:
        ...
