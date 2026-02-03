import json
from dataclasses import dataclass
from typing import Any

import aiohttp

from health_backend.application.recommendation.dto import ThresholdsDTO
from health_backend.application.recommendation.generator import GeneratorService
from health_backend.domain.recommendation.entity import Recommendation

prompt = (
    "You're a professional medical assistant, you need to generate personalized"
    "measuring ranges based on provider patient's history, you must be very accurate"
)


@dataclass(frozen=True, slots=True)
class OpenRouterGeneratorService(GeneratorService):
    api_url: str
    model: str
    api_key: str

    async def generate(self, patient_history: str) -> ThresholdsDTO:
        body = self.construct_request(patient_history)
        async with aiohttp.ClientSession(
            headers={'Authorization': f'Bearer {self.api_key}'}
        ) as session:
            async with session.post(self.api_url, json=body) as response:
                # TODO: error handling
                json_content = await response.json()
                ranges = json.loads(json_content['choices'][0]['message']['content'])['ranges']
                return ThresholdsDTO(
                    systolic_blood_pressure_min=ranges['systolic_blood_pressure_min'],
                    systolic_blood_pressure_max=ranges['systolic_blood_pressure_max'],
                    diastolic_blood_pressure_min=ranges['diastolic_blood_pressure_min'],
                    diastolic_blood_pressure_max=ranges['diastolic_blood_pressure_max'],
                    temperature_celsius_min=ranges['temperature_celsius_min'],
                    temperature_celsius_max=ranges['temperature_celsius_max'],
                )

    def construct_request(self, patient_history: str) -> dict[str, Any]:
        return {
            'model': self.model,
            'provider': {
                'require_parameters': True,
            },
            'messages': [
                {
                    'role': 'user',
                    'content': prompt,
                },
                {'role': 'user', 'content': patient_history},
            ],
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
                                    'heart_rate_min': {
                                        'type': 'number',
                                        'description': 'Minimum heart rate allowed',
                                    },
                                    'heart_rate_max': {
                                        'type': 'number',
                                        'description': 'Maximum heart rate allowed',
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
