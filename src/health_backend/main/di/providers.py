import os
from pathlib import Path
from typing import AsyncIterator

from alembic.config import Config as AlembicConfig
from dishka import Provider, Scope, provide, provide_all
from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from health_backend.adapters.common.access_token_generator import JWTGenerator
from health_backend.adapters.common.http.aiohttp import AioHttpClient
from health_backend.adapters.common.http.client import HttpClient
from health_backend.adapters.common.idp import JWTIdProvider, JWTParser
from health_backend.adapters.common.password_hasher import ArgonPasswordHasher
from health_backend.adapters.persistence.db.doctor.repository import SADoctorRepository
from health_backend.adapters.persistence.db.patient.repository import SAPatientRepository
from health_backend.adapters.persistence.db.recommendation.repository import (
    SARecommendationRepository,
)
from health_backend.adapters.persistence.in_memory.doctor.repository import InMemoryDoctorRepository
from health_backend.adapters.recommendation.generator.yandex.request_builder import (
    YandexGPTRequestBuilder,
)
from health_backend.adapters.recommendation.generator.yandex.response_parser import (
    YandexGPTResponseParser,
)
from health_backend.adapters.recommendation.generator.yandex.service import (
    YandexGPTGeneratorService,
)
from health_backend.application.common.access_token_generator import AccessTokenGenerator
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.common.password_hasher import PasswordHasher
from health_backend.application.common.uow import UnitOfWork
from health_backend.application.doctor.get_me import GetMe
from health_backend.application.doctor.login import DoctorLogin
from health_backend.application.doctor.signup import DoctorSignup
from health_backend.application.patient.create import CreatePatient
from health_backend.application.patient.delete import DeletePatient
from health_backend.application.patient.get import GetPaginatedPatients, GetPatient
from health_backend.application.recommendation.generate import GenerateRecommendationForPatient
from health_backend.application.recommendation.generator import (
    GeneratorService,
    ThresholdsGenerator,
)
from health_backend.application.recommendation.get import GetPaginatedRecommendationsForPatient
from health_backend.domain.doctor.repository import DoctorRepository
from health_backend.domain.patient.repository import PatientRepository
from health_backend.domain.recommendation.repository import RecommendationRepository
from health_backend.main.config import (
    APIConfig,
    JWTConfig,
    PostgresConfig,
    YandexCloudConfig,
)


class UseCaseProvider(Provider):
    scope = Scope.REQUEST
    use_cases = provide_all(
        GenerateRecommendationForPatient,
        DoctorSignup,
        DoctorLogin,
        GetMe,
        CreatePatient,
        GetPaginatedPatients,
        GetPaginatedRecommendationsForPatient,
        GetPatient,
        DeletePatient,
    )


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, config: PostgresConfig) -> AsyncEngine:
        print(config.url)
        return create_async_engine(url=config.url)

    @provide(scope=Scope.APP)
    def get_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
        return session_maker

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        session = session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @provide(scope=Scope.REQUEST)
    async def get_uow(self, session: AsyncSession) -> UnitOfWork:
        return session


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
        config: YandexCloudConfig,
        http_client: HttpClient,
        request_builder: YandexGPTRequestBuilder,
        response_parser: YandexGPTResponseParser,
    ) -> YandexGPTGeneratorService:
        return YandexGPTGeneratorService(
            api_url=config.api_url,
            http_client=http_client,
            request_builder=request_builder,
            response_parser=response_parser,
        )

    @provide
    def get_http_client(self) -> HttpClient:
        return AioHttpClient()

    @provide
    def get_yandex_request_builder(self, config: YandexCloudConfig) -> YandexGPTRequestBuilder:
        return YandexGPTRequestBuilder(
            folder=config.folder,
            model=config.model,
            api_key=config.api_key,
        )

    @provide
    def get_yandex_response_parser(self) -> YandexGPTResponseParser:
        return YandexGPTResponseParser()


class AuthProvider(Provider):
    @provide(scope=Scope.APP)
    def get_password_hasher(self) -> PasswordHasher:
        return ArgonPasswordHasher()

    @provide(scope=Scope.APP)
    def get_access_token_generator(self, config: JWTConfig) -> AccessTokenGenerator:
        return JWTGenerator(config.secret)

    @provide(scope=Scope.APP)
    def get_jwt_parser(self, config: JWTConfig) -> JWTParser:
        return JWTParser(config.secret)

    @provide(scope=Scope.REQUEST)
    def get_idp(self, request: Request, parser: JWTParser) -> DoctorIdProvider:
        token = request.cookies.get('access_token')
        return JWTIdProvider(parser=parser, token=token)


class RepoProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_doctor_repo(self, session: AsyncSession) -> DoctorRepository:
        return SADoctorRepository(session)

    @provide
    def get_patient_repo(self, session: AsyncSession) -> PatientRepository:
        return SAPatientRepository(session)

    @provide
    def get_recommendation_repo(self, session: AsyncSession) -> RecommendationRepository:
        return SARecommendationRepository(session)


class AlembicConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_alembic_config(self) -> AlembicConfig:
        ini_file_path = str(Path(__file__).parent.parent.parent.parent.parent / 'alembic.ini')
        scripts_path = str(Path(__file__).parent.parent.parent.parent.parent / 'alembic')
        config = AlembicConfig(file_=ini_file_path)
        config.set_main_option('script_location', scripts_path)
        return config


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_yandex_cloud_config(self) -> YandexCloudConfig:
        return YandexCloudConfig(
            api_url=os.getenv('YANDEX_CLOUD_API_URL'),
            api_key=os.getenv('YANDEX_CLOUD_API_KEY'),
            folder=os.getenv('YANDEX_CLOUD_FOLDER'),
            model=os.getenv('YANDEX_CLOUD_MODEL'),
        )

    @provide
    def get_postgres_config(self) -> PostgresConfig:
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        name = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        url = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}'
        return PostgresConfig(url=url)

    @provide
    def get_jwt_config(self) -> JWTConfig:
        return JWTConfig(secret=os.getenv('SECRET'))

    @provide
    def get_api_config(self) -> APIConfig:
        return APIConfig(
            host=os.getenv('HOST'),
            port=int(os.getenv('PORT')),
            origins=os.getenv('ORIGINS').split(','),
        )
