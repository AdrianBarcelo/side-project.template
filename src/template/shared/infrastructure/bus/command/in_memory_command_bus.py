from typing import Any, Type

from template.shared.domain.bus.command.command import Command
from template.shared.domain.bus.command.command_bus import CommandBus
from template.shared.domain.bus.command.command_handler import CommandHandler


class InMemoryCommandBus(CommandBus):
    def __init__(self, handlers: dict[Type[Command], CommandHandler] | None = None) -> None:
        self._handlers = handlers if handlers is not None else {}

    def register(self, command_type: Type[Command], handler: CommandHandler) -> None:
        self._handlers[command_type] = handler

    def dispatch(self, command: Command) -> Any:
        handler = self._handlers.get(command.__class__)
        if handler:
            return handler.handle(command)
