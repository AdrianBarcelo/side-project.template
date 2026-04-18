from sqlalchemy.orm import Session

from template.shared.domain.bus.command.command_bus import CommandBus
from template.shared.domain.bus.event.event_bus import EventBus
from template.shared.domain.bus.query.query_bus import QueryBus
from template.shared.domain.uuid_generator import UuidGenerator


class DependenciesContainer:
    def __init__(self, session: Session) -> None:
        self._session = session
        # TODO: instanciar repositorios de cada bounded context aquí
        # Ejemplo:
        # self._example_repository = SqlAlchemyExampleRepository(session=self._session)

    @property
    def command_bus(self) -> CommandBus:
        from template.shared.infrastructure.bus.command.command_bus_factory import CommandBusFactory

        return CommandBusFactory.create(
            event_bus=self.event_bus,
            query_bus=self.query_bus,
            uuid_generator=self.uuid_generator,
            # TODO: pasar repositorios aquí
        )

    @property
    def event_bus(self) -> EventBus:
        from template.shared.infrastructure.bus.event.in_memory_event_bus import InMemoryEventBus

        return InMemoryEventBus()

    @property
    def query_bus(self) -> QueryBus:
        from template.shared.infrastructure.bus.query.query_bus_factory import QueryBusFactory

        return QueryBusFactory.create(
            # TODO: pasar repositorios aquí
        )

    @property
    def uuid_generator(self) -> UuidGenerator:
        from template.shared.infrastructure.uuid4_generator import UUID4Generator

        return UUID4Generator()
