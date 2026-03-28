from sqlalchemy import Dialect, String, TypeDecorator

from health_backend.domain.common.vo import Email, Name


class NameType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Name | None, dialect: Dialect) -> str | None:  # noqa: ARG002
        if value is not None:
            return value.value
        return None

    def process_result_value(self, value: str | None, dialect: Dialect) -> Name | None:  # noqa: ARG002
        if value is not None:
            return Name(value)
        return None


class EmailType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Email | None, dialect: Dialect) -> str | None:  # noqa: ARG002
        if value is not None:
            return value.value
        return None

    def process_result_value(self, value: str | None, dialect: Dialect) -> Email | None:  # noqa: ARG002
        if value is not None:
            return Email(value)
        return None
