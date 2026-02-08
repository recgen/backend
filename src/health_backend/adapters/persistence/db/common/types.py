import json

from attr import asdict
from sqlalchemy import String, TypeDecorator

from health_backend.domain.common.vo import Email, Name


class NameType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Name | None, dialect) -> str | None:
        if value is not None:
            return json.dumps(asdict(value))
        return None

    def process_result_value(self, value: str | None, dialect) -> Name | None:
        if value is not None:
            return Name(**json.loads(value))
        return None


class EmailType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Email | None, dialect) -> str | None:
        if value is not None:
            return json.dumps(asdict(value))
        return None

    def process_result_value(self, value: str | None, dialect) -> Email | None:
        if value is not None:
            return Email(**json.loads(value))
        return None
