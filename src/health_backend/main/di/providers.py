from dishka import Provider, Scope, provide, provide_all

from health_backend.adapters.recommendation.generator.openrouter import OpenRouterGeneratorService
from health_backend.application.recommendation.generate import GenerateRecommendation
from health_backend.application.recommendation.generator import (
    GeneratorService,
    ThresholdsGenerator,
)
from health_backend.main.config import config


class UseCaseProvider(Provider):
    scope = Scope.REQUEST
    use_cases = provide_all(
        GenerateRecommendation,
    )


class UOWProvider:
    scope = Scope.REQUEST


class GeneratorProvider(Provider):
    scope = Scope.APP

    @provide
    def get_generator_service(self) -> GeneratorService:
        return OpenRouterGeneratorService(
            api_url=config.openrouter_url,
            model=config.openrouter_model,
            api_key=config.openrouter_api_key,
        )

    @provide
    def get_generator(self, service: GeneratorService) -> ThresholdsGenerator:
        return ThresholdsGenerator(service)
