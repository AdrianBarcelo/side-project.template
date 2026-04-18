import json
import random
import string
import uuid
from datetime import datetime
from random import randint
from re import sub
from typing import Any, Dict, Optional


class Utils:
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    @staticmethod
    def date_to_string(date: datetime, date_format: Optional[str] = None) -> str:
        format_to_use = date_format or Utils.DATE_FORMAT
        return date.strftime(format_to_use)

    @staticmethod
    def string_to_date(date: str, date_format: Optional[str] = None) -> datetime:
        format_to_use = date_format or Utils.DATE_FORMAT
        return datetime.strptime(date, format_to_use)

    @staticmethod
    def json_encode(values: Dict[str, Any]) -> str:
        return json.dumps(values, ensure_ascii=False)

    @staticmethod
    def json_decode(json_string: str) -> Any:
        return json.loads(json_string)

    @staticmethod
    def from_pascal_to_snake_case(string: str) -> str:
        return sub(r"(?<!^)(?=[A-Z])", "_", string).lower()

    @staticmethod
    def from_pascal_to_kebab_case(string: str) -> str:
        return sub(r"(?<!^)(?=[A-Z])", "-", string).lower()

    @staticmethod
    def random_string(
        length: int | None = None, min_length: int | None = None, max_length: int | None = None
    ) -> str:
        length = length or randint(
            1 if min_length is None else min_length, 64 if max_length is None else max_length
        )
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def random_uuid() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def random_int(min_value: int = -9999999, max_value: int = 9999999) -> int:
        return randint(min_value, max_value)

    @staticmethod
    def random_float(min_value: float = 0.0, max_value: float = 9999999.0) -> float:
        return random.uniform(min_value, max_value)

    @staticmethod
    def random_bool() -> bool:
        return random.choice([True, False])
