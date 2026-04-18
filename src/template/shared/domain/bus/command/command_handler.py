from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from template.shared.domain.bus.command.command import Command

T = TypeVar("T", bound="Command")


class CommandHandler(ABC, Generic[T]):
    @abstractmethod
    def handle(self, command: T) -> None:
        ...
