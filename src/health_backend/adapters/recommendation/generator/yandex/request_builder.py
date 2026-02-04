from dataclasses import dataclass, field
from typing import Any

from health_backend.adapters.recommendation.generator.common.request_builder import RequestBuilder

prompt = (
    'Ты профессиональный медицинский ассистент. Ты должен генерировать'
    'персонализированные диапазоны (пороги) на основе истории пациента.'
    'Твои рекомендации должны быть верны с медицинской точки зрения.'
)


@dataclass(slots=True)
class YandexGPTRequestBuilder(RequestBuilder):
    folder: str
    model: str
    api_key: str
    _model_uri: str = field(init=False)

    def __post_init__(self) -> None:
        self._model_uri = f'gpt://{self.folder}/{self.model}'

    def body(self, patient_history: str) -> dict[str, Any]:
        return {
            'messages': [
                {
                    'content': prompt,
                    'role': 'system',
                },
                {
                    'content': patient_history,
                    'role': 'user',
                },
            ],
            'model': self._model_uri,
            'response_format': {
                'type': 'json_schema',
                'json_schema': {
                    'name': 'patient_ranges',
                    'strict': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'ranges': {
                                'type': 'object',
                                'properties': {
                                    'temperature_celsius_min': {
                                        'type': 'number',
                                        'description': (
                                            'Minimum allowed temperature for the patient'
                                        ),
                                    },
                                    'temperature_celsius_max': {
                                        'type': 'number',
                                        'description': (
                                            'Maximum allowed temperature for the patient'
                                        ),
                                    },
                                    'systolic_blood_pressure_min': {
                                        'type': 'number',
                                        'description': 'Minimum systolic blood pressure allowed',
                                    },
                                    'systolic_blood_pressure_max': {
                                        'type': 'number',
                                        'description': 'Maximum systolic blood pressure allowed',
                                    },
                                    'diastolic_blood_pressure_min': {
                                        'type': 'number',
                                        'description': 'Minimum diastolic blood pressure allowed',
                                    },
                                    'diastolic_blood_pressure_max': {
                                        'type': 'number',
                                        'description': 'Maximum diastolic blood pressure allowed',
                                    },
                                },
                                'required': [
                                    'systolic_blood_pressure_min',
                                    'systolic_blood_pressure_max',
                                    'diastolic_blood_pressure_min',
                                    'diastolic_blood_pressure_max',
                                    'temperature_celsius_min',
                                    'temperature_celsius_max',
                                ],
                            }
                        },
                        'required': ['ranges'],
                        'additionalProperties': False,
                    },
                },
            },
        }

    def headers(self) -> dict[str, Any]:
        return {
            'Authorization': f'Api-Key {self.api_key}',
        }
