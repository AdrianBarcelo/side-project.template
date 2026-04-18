from typing import Any, Type

from template.shared.domain.bus.query.query import Query
from template.shared.domain.bus.query.query_bus import QueryBus
from template.shared.domain.bus.query.query_handler import QueryHandler


class InMemoryQueryBus(QueryBus):
    def __init__(self, handlers: dict[Type[Query], QueryHandler] | None = None) -> None:
        self._handlers = handlers if handlers is not None else {}

    def register(self, query_type: Type[Query], handler: QueryHandler) -> None:
        self._handlers[query_type] = handler

    def dispatch(self, query: Query) -> Any:
        handler = self._handlers.get(query.__class__)
        if not handler:
            raise ValueError(f"No handler found for query: {query.__class__.__name__}")

        return handler.handle(query)
