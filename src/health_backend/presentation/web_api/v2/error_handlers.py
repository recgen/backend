from typing import Any, cast

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic.alias_generators import to_snake

from health_backend.adapters.common.errors import InfrastructureError, LLMError
from health_backend.application.common.errors import (
    ApplicationError,
    EmailAlreadyInUseError,
    NotFoundError,
    UnauthorizedError,
)
from health_backend.domain.common.errors import (
    DomainError,
    EmptyPatientHistoryError,
    FutureDateError,
    InactiveError,
    InvalidEmailError,
)

error_to_http_code: dict[type[Exception], int] = {
    EmptyPatientHistoryError: 422,
    LLMError: 422,
    EmailAlreadyInUseError: 409,
    UnauthorizedError: 401,
    NotFoundError: 404,
    InactiveError: 403,
    InvalidEmailError: 422,
    FutureDateError: 422,
}


def construct_body(err: Exception) -> dict[str, Any]:
    return {
        'code': to_snake(err.__class__.__name__).upper(),
    }


def get_http_code_for(err: Exception) -> int:
    return error_to_http_code.get(type(err), 500)


def domain_error_handler(_request: Request, err: Exception) -> JSONResponse:
    cast(DomainError, err)
    body = construct_body(err)
    return JSONResponse(
        body,
        status_code=get_http_code_for(err),
    )


def infrastructure_error_handler(_request: Request, err: Exception) -> JSONResponse:
    cast(InfrastructureError, err)
    body = construct_body(err)
    if isinstance(err, LLMError):
        body = {
            **body,
            'reason': err.reason,
        }
    return JSONResponse(
        body,
        status_code=get_http_code_for(err),
    )


def application_error_handler(_request: Request, err: Exception) -> JSONResponse:
    cast(ApplicationError, err)
    body = construct_body(err)
    return JSONResponse(
        body,
        status_code=get_http_code_for(err),
    )
