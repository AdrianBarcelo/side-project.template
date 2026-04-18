import uuid

from template.shared.domain.uuid_generator import UuidGenerator


class UUID4Generator(UuidGenerator):
    def generate(self) -> str:
        return str(uuid.uuid4())
