from template.shared.domain.exceptions.domain_exception import DomainException


class InvalidUuid(DomainException):
    def __init__(self, string: str) -> None:
        self._string = string
        super().__init__()

    def error_message(self) -> str:
        return f"{self._string} is not a valid UUID"
