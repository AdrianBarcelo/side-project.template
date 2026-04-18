from template.shared.domain.bus.query.query_bus import QueryBus
from template.shared.infrastructure.bus.query.in_memory_query_bus import InMemoryQueryBus


class QueryBusFactory:
    @staticmethod
    def create(
        # TODO: añadir repositorios de cada bounded context aquí
    ) -> QueryBus:
        query_bus = InMemoryQueryBus()

        # TODO: registrar query handlers de cada bounded context aquí
        # Ejemplo:
        # query_bus.register(
        #     GetExampleQuery,
        #     GetExampleQueryHandler(repository=example_repository),
        # )

        return query_bus
