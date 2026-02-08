from dataclasses import dataclass, field
from typing import Any

from health_backend.adapters.recommendation.generator.common.request_builder import RequestBuilder

prompt = (
    'You are a professional medical assistant. You must generate personalized '
    "critical ranges based on patient's history."
    "Patient's history may be given either as a name of the illness or a full description."
    "If the request does not contain patient's history or it contains swear words "
    'then you must invalidate the request.'
    'Respond exclusively in Russian '
    'Never switch language. Never translate. '
    'No additional explanations about language. '
    'Reply about errors in a very short manner '
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
                            'result': {
                                'type': 'object',
                                'anyOf': [
                                    {
                                        'type': 'object',
                                        'properties': {
                                            'ranges': {
                                                'type': 'object',
                                                'properties': {
                                                    'temperature_celsius_min': {'type': 'number'},
                                                    'temperature_celsius_max': {'type': 'number'},
                                                    'systolic_blood_pressure_min': {
                                                        'type': 'number'
                                                    },
                                                    'systolic_blood_pressure_max': {
                                                        'type': 'number'
                                                    },
                                                    'diastolic_blood_pressure_min': {
                                                        'type': 'number'
                                                    },
                                                    'diastolic_blood_pressure_max': {
                                                        'type': 'number'
                                                    },
                                                },
                                                'required': [
                                                    'temperature_celsius_min',
                                                    'temperature_celsius_max',
                                                    'systolic_blood_pressure_min',
                                                    'systolic_blood_pressure_max',
                                                    'diastolic_blood_pressure_min',
                                                    'diastolic_blood_pressure_max',
                                                ],
                                                'additionalProperties': False,
                                            }
                                        },
                                        'required': ['ranges'],
                                        'additionalProperties': False,
                                    },
                                    {
                                        'type': 'object',
                                        'properties': {
                                            'error': {
                                                'type': 'object',
                                                'properties': {'reason': {'type': 'string'}},
                                                'required': ['reason'],
                                                'additionalProperties': False,
                                            }
                                        },
                                        'required': ['error'],
                                        'additionalProperties': False,
                                    },
                                ],
                            }
                        },
                        'required': ['result'],
                        'additionalProperties': False,
                    },
                },
            },
        }

    def headers(self) -> dict[str, Any]:
        return {
            'Authorization': f'Api-Key {self.api_key}',
        }
