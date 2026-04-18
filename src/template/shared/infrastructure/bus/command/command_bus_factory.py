from typing import Type

from template.shared.domain.bus.command.command import Command
from template.shared.domain.bus.command.command_bus import CommandBus
from template.shared.domain.bus.command.command_handler import CommandHandler
from template.shared.domain.bus.event.event_bus import EventBus
from template.shared.domain.bus.query.query_bus import QueryBus
from template.shared.domain.uuid_generator import UuidGenerator
from template.shared.infrastructure.bus.command.in_memory_command_bus import InMemoryCommandBus


class CommandBusFactory:
    @staticmethod
    def create(
        event_bus: EventBus,
        query_bus: QueryBus,
        uuid_generator: UuidGenerator,
        # TODO: añadir repositorios de cada bounded context aquí
    ) -> CommandBus:
        handlers: dict[Type[Command], CommandHandler] = {
            # TODO: registrar command handlers de cada bounded context aquí
            # Ejemplo:
            # CreateExampleCommand: CreateExampleCommandHandler(
            #     repository=example_repository,
            #     event_bus=event_bus,
            # ),
        }

        return InMemoryCommandBus(handlers=handlers)
