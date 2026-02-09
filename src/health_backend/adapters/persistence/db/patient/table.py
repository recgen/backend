from sqlalchemy import Boolean, Column, DateTime, Enum, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String

from health_backend.adapters.persistence.db.common.types import NameType
from health_backend.adapters.persistence.db.registry import mapper_registry
from health_backend.domain.common.vo import Gender
from health_backend.domain.patient.entity import Patient

patient_table = Table(
    'patient',
    mapper_registry.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('name', NameType, nullable=False),
    Column('birth_date', DateTime(timezone=True), nullable=False),
    Column('gender', Enum(Gender, name='gender_enum'), nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
)


def start_patient_mapping() -> None:
    mapper_registry.map_imperatively(Patient, patient_table)
