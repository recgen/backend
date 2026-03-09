from dataclasses import dataclass, field
from typing import Any

from health_backend.adapters.recommendation.generator.common.request_builder import RequestBuilder

prompt = (
    'Ты — клиническая система поддержки принятия врачебных решений.\n\n'
    'Задача: на основе истории болезни пациента определить индивидуальные '
    'ЦЕЛЕВЫЕ диапазоны трёх показателей:\n'
    '- систолическое артериальное давление (мм рт. ст.)\n'
    '- диастолическое артериальное давление (мм рт. ст.)\n'
    '- температура тела (°C)\n\n'
    '## Критически важные правила\n\n'
    '1. ПЕРСОНАЛИЗАЦИЯ. Диапазоны строго индивидуальны. '
    'Учитывай ВСЕ указанные факторы: диагнозы, стадии заболеваний, '
    'принимаемые препараты, возраст, пол, осложнения. '
    'Если история болезни краткая (только название диагноза), '
    'определяй диапазоны на основе типичного профиля пациента с данным заболеванием.\n\n'
    '2. УЗОСТЬ ДИАПАЗОНОВ. Допустимая разница между min и max:\n'
    '   - Систолическое АД: 10–15 мм рт. ст.\n'
    '   - Диастолическое АД: 5–10 мм рт. ст.\n'
    '   - Температура: 0.5–1.0 °C\n'
    '   Широкие общепопуляционные диапазоны (например, 110–140) — это грубая ошибка. '
    'Давай только клинически целевые значения для конкретного пациента.\n\n'
    '3. КЛИНИЧЕСКИЕ РЕКОМЕНДАЦИИ, на которые необходимо опираться:\n'
    '   - ESC/ESH 2018 (артериальная гипертензия)\n'
    '   - Клинические рекомендации Минздрава РФ\n'
    '   - ADA Standards of Care (при сахарном диабете)\n'
    '   - KDIGO (при хронической болезни почек)\n\n'
    '4. ОКРУГЛЕНИЕ:\n'
    '   - АД: до целых чисел (например: 120, 130)\n'
    '   - Температура: до одного знака после запятой (например: 36.0, 36.5, 37.0)\n'
    '   Дробные значения АД и температура с более чем одним знаком после запятой недопустимы.\n\n'
    '## Валидация входных данных\n\n'
    'Если запрос не содержит никакой медицинской информации о пациенте '
    'или содержит нецензурную лексику, ответь с ошибкой'
    'Язык ответа: исключительно русский. Не переключай язык ни при каких условиях.'
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
