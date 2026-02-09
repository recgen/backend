from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic.alias_generators import to_snake

from health_backend.adapters.common.errors import InfrastructureError, LLMError
from health_backend.application.common.errors import (
    ApplicationError,
    EmailAlreadyInUse,
    NotFound,
    Unauthorized,
)
from health_backend.domain.common.errors import DomainError, EmptyPatientHistory, Inactive

error_to_http_code = {
    EmptyPatientHistory: 422,
    LLMError: 422,
    EmailAlreadyInUse: 409,
    Unauthorized: 401,
    NotFound: 404,
    Inactive: 403,
}


def construct_body(err: Exception) -> dict[str, Any]:
    return {
        'code': to_snake(err.__class__.__name__).upper(),
    }


def get_http_code_for(err: Exception) -> int:
    return error_to_http_code[err.__class__]


def domain_error_handler(request: Request, err: Exception) -> JSONResponse:
    assert isinstance(err, DomainError)
    body = construct_body(err)
    return JSONResponse(
        body,
        status_code=get_http_code_for(err),
    )


def infrastructure_error_handler(request: Request, err: Exception) -> JSONResponse:
    assert isinstance(err, InfrastructureError)
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


def application_error_handler(request: Request, err: Exception) -> JSONResponse:
    assert isinstance(err, ApplicationError)
    body = construct_body(err)
    return JSONResponse(
        body,
        status_code=get_http_code_for(err),
    )
