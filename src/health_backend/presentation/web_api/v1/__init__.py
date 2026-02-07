from fastapi import FastAPI

from health_backend.adapters.common.errors import InfrastructureError
from health_backend.application.common.errors import ApplicationError
from health_backend.domain.common.errors import DomainError
from health_backend.presentation.web_api.v1.error_handlers import (
    application_error_handler,
    domain_error_handler,
    infrastructure_error_handler,
)
from health_backend.presentation.web_api.v1.routes import auth, recommendation


def include_routers(app: FastAPI) -> None:
    app.include_router(recommendation.router)
    app.include_router(auth.router)


def include_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(InfrastructureError, infrastructure_error_handler)
    app.add_exception_handler(ApplicationError, application_error_handler)
