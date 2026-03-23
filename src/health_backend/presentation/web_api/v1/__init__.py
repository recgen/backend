from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from health_backend.adapters.common.errors import InfrastructureError
from health_backend.application.common.errors import ApplicationError
from health_backend.domain.common.errors import DomainError
from health_backend.presentation.web_api.v1.error_handlers import (
    application_error_handler,
    domain_error_handler,
    infrastructure_error_handler,
)
from health_backend.presentation.web_api.v1.routes import auth, patient, recommendation


def include_routers(app: FastAPI) -> None:
    app.include_router(recommendation.router, prefix='/api/v1', deprecated=True)
    app.include_router(auth.router, prefix='/api/v1', deprecated=True)
    app.include_router(patient.router, prefix='/api/v1', deprecated=True)


def include_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(InfrastructureError, infrastructure_error_handler)
    app.add_exception_handler(ApplicationError, application_error_handler)


def add_cors_middleware(app: FastAPI, origins: list[str]) -> None:
    app.add_middleware(
        CORSMiddleware,  # ty: ignore
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
