from template.shared.domain.exceptions.domain_exception import DomainException


class InvalidMilliseconds(DomainException):
    def __init__(self, value: int) -> None:
        self._value = value
        super().__init__()

    def error_message(self) -> str:
        return f"{self._value} are not valid milliseconds"
