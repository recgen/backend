from dishka import Provider, Scope, provide, provide_all

from health_backend.adapters.common.http.aiohttp import AioHttpClient
from health_backend.adapters.common.http.client import HttpClient
from health_backend.adapters.recommendation.generator.yandex.request_builder import (
    YandexGPTRequestBuilder,
)
from health_backend.adapters.recommendation.generator.yandex.response_parser import (
    YandexGPTResponseParser,
)
from health_backend.adapters.recommendation.generator.yandex.service import (
    YandexGPTGeneratorService,
)
from health_backend.application.recommendation.generate import GenerateRecommendationForPatient
from health_backend.application.recommendation.generator import (
    GeneratorService,
    ThresholdsGenerator,
)
from health_backend.main.config import config


class UseCaseProvider(Provider):
    scope = Scope.REQUEST
    use_cases = provide_all(
        GenerateRecommendationForPatient,
    )


class UOWProvider:
    scope = Scope.REQUEST


class GeneratorProvider(Provider):
    scope = Scope.APP

    @provide
    def get_generator_service(self, service: YandexGPTGeneratorService) -> GeneratorService:
        return service

    @provide
    def get_generator(self, service: GeneratorService) -> ThresholdsGenerator:
        return ThresholdsGenerator(service)

    @provide
    def get_yandex_generator(
        self,
        http_client: HttpClient,
        request_builder: YandexGPTRequestBuilder,
        response_parser: YandexGPTResponseParser,
    ) -> YandexGPTGeneratorService:
        return YandexGPTGeneratorService(
            api_url=config.yandex_cloud_url,
            http_client=http_client,
            request_builder=request_builder,
            response_parser=response_parser,
        )

    @provide
    def get_http_client(self) -> HttpClient:
        return AioHttpClient()

    @provide
    def get_yandex_request_builder(self) -> YandexGPTRequestBuilder:
        return YandexGPTRequestBuilder(
            folder=config.yandex_cloud_folder,
            model=config.yandex_cloud_model,
            api_key=config.yandex_cloud_api_key,
        )

    @provide
    def get_yandex_response_parser(self) -> YandexGPTResponseParser:
        return YandexGPTResponseParser()
