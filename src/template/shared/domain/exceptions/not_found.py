from abc import ABC, abstractmethod

from template.shared.domain.exceptions.domain_exception import DomainException


class NotFound(DomainException, ABC):
    def __init__(self, aggregate_id: str) -> None:
        self._aggregate_id = aggregate_id
        super().__init__()

    @abstractmethod
    def aggregate_class_name(self) -> str:
        ...

    def error_message(self) -> str:
        return f"{self.aggregate_class_name()} with id {self._aggregate_id} not found"
