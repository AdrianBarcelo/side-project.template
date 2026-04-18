from abc import ABC, abstractmethod


class DomainException(Exception, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def error_message(self) -> str:
        pass
