from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from template.shared.domain.bus.query.query import Query

TQuery = TypeVar("TQuery", bound="Query")
TResponse = TypeVar("TResponse")


class QueryHandler(ABC, Generic[TQuery, TResponse]):
    @abstractmethod
    def handle(self, query: TQuery) -> TResponse:
        ...
