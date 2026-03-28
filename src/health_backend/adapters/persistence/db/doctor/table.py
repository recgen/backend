from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import UUID

from health_backend.adapters.persistence.db.common.types import EmailType, NameType
from health_backend.adapters.persistence.db.registry import mapper_registry
from health_backend.domain.doctor.entity import Doctor

doctor_table = Table(
    'doctor',
    mapper_registry.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('name', NameType, nullable=False),
    Column('email', EmailType, nullable=False, unique=True),
    Column('hashed_password', String, nullable=False),
)


def start_doctor_mapping() -> None:
    mapper_registry.map_imperatively(
        Doctor,
        doctor_table,
    )
