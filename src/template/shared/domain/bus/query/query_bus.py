from abc import ABC, abstractmethod

from template.shared.domain.bus.query.query import Query
from template.shared.domain.bus.query.response import Response


class QueryBus(ABC):
    @abstractmethod
    def dispatch(self, query: Query) -> Response:
        ...
