import json
from decimal import Decimal

from attrs import asdict
from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import TypeDecorator

from health_backend.adapters.persistence.db.registry import mapper_registry
from health_backend.domain.common.vo import Range
from health_backend.domain.patient.vo import PatientHistory
from health_backend.domain.recommendation.entity import Recommendation
from health_backend.domain.recommendation.vo import Thresholds


class PatientHistoryType(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value: PatientHistory | None, dialect) -> str | None:
        if value is not None:
            return json.dumps(asdict(value))
        return None

    def process_result_value(self, value: str | None, dialect) -> PatientHistory | None:
        if value is not None:
            return PatientHistory(**json.loads(value))
        return None


class ThresholdsType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Thresholds | None, dialect) -> str | None:
        if value is None:
            return None
        return json.dumps(
            {
                'systolic_blood_pressure': {
                    'minimum': str(value.systolic_blood_pressure.minimum),
                    'maximum': str(value.systolic_blood_pressure.maximum),
                },
                'diastolic_blood_pressure': {
                    'minimum': str(value.diastolic_blood_pressure.minimum),
                    'maximum': str(value.diastolic_blood_pressure.maximum),
                },
                'temperature_celsius': {
                    'minimum': str(value.temperature_celsius.minimum),
                    'maximum': str(value.temperature_celsius.maximum),
                },
            }
        )

    def process_result_value(self, value: str | None, dialect) -> Thresholds | None:
        if value is None:
            return None
        data = json.loads(value)
        return Thresholds(
            systolic_blood_pressure=Range(
                Decimal(data['systolic_blood_pressure']['minimum']),
                Decimal(data['systolic_blood_pressure']['maximum']),
            ),
            diastolic_blood_pressure=Range(
                Decimal(data['diastolic_blood_pressure']['minimum']),
                Decimal(data['diastolic_blood_pressure']['maximum']),
            ),
            temperature_celsius=Range(
                Decimal(data['temperature_celsius']['minimum']),
                Decimal(data['temperature_celsius']['maximum']),
            ),
        )


recommendation_table = Table(
    'recommendation',
    mapper_registry.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('patient_id', UUID(as_uuid=True), ForeignKey('patient.id'), nullable=False),
    Column('patient_history', PatientHistoryType, nullable=False),
    Column('thresholds', ThresholdsType, nullable=False),
)


def start_recommendation_mapping() -> None:
    mapper_registry.map_imperatively(Recommendation, recommendation_table)
