from template.shared.domain.exceptions.domain_exception import DomainException


class InvalidId(DomainException):
    def __init__(self, value: str) -> None:
        self._value = value
        super().__init__()

    def error_message(self) -> str:
        return f"Id {self._value} must be a valid string"
