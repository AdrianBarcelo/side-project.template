from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast

from sqlalchemy.orm import Session

from template.shared.domain.bus.query.query import Query
from template.shared.domain.bus.query.response import Response as QueryResponse
from template.shared.infrastructure.dependencies_container import DependenciesContainer
from databases import SessionFactory

TQuery = TypeVar("TQuery", bound=Query)
TResponse = TypeVar("TResponse", bound=QueryResponse)


class QueryView(ABC, Generic[TQuery, TResponse]):
    @abstractmethod
    def build_query(self, *args: Any, **kwargs: Any) -> TQuery:
        pass

    def execute(self, *args: Any, **kwargs: Any) -> TResponse:
        session: Session = SessionFactory.create()
        try:
            query = self.build_query(*args, **kwargs)
            container = DependenciesContainer(session=session)
            result = cast(TResponse, container.query_bus.dispatch(query))
            return result
        finally:
            session.close()
