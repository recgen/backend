import json

from sqlalchemy import String, TypeDecorator

from health_backend.domain.common.vo import Email, Name


class NameType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, name: Name | None, dialect) -> str | None:
        if name is not None:
            return name.value
        return None

    def process_result_value(self, value: str | None, dialect) -> Name | None:
        if value is not None:
            return Name(value)
        return None


class EmailType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, email: Email | None, dialect) -> str | None:
        if email is not None:
            return email.value
        return None

    def process_result_value(self, value: str | None, dialect) -> Email | None:
        if value is not None:
            return Email(value)
        return None
