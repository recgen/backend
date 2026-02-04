import json
from typing import Any

from health_backend.adapters.common.errors import LLMError
from health_backend.adapters.recommendation.generator.common.response_parser import ResponseParser
from health_backend.application.recommendation.dto import ThresholdsDTO


class YandexGPTResponseParser(ResponseParser):
    def parse(self, response: dict[Any, Any]) -> ThresholdsDTO:
        try:
            ranges = json.loads(response['choices'][0]['message']['content'])['ranges']
            return ThresholdsDTO(
                systolic_blood_pressure_min=ranges['systolic_blood_pressure_min'],
                systolic_blood_pressure_max=ranges['systolic_blood_pressure_max'],
                diastolic_blood_pressure_min=ranges['diastolic_blood_pressure_min'],
                diastolic_blood_pressure_max=ranges['diastolic_blood_pressure_max'],
                temperature_celsius_min=ranges['temperature_celsius_min'],
                temperature_celsius_max=ranges['temperature_celsius_max'],
            )
        except KeyError as e:
            raise LLMError from e
