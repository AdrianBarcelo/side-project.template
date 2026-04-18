from template.shared.domain.exceptions.domain_exception import DomainException


class InvalidDate(DomainException):
    def __init__(self, value: str) -> None:
        self._value = value
        super().__init__()

    def error_message(self) -> str:
        return f"Date {self._value} is not valid"
