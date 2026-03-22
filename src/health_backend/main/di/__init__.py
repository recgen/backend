from dishka import AsyncContainer, Container, make_async_container, make_container
from dishka.integrations.fastapi import FastapiProvider

from health_backend.main.di.providers import (
    AlembicConfigProvider,
    AuthProvider,
    DBProvider,
    GeneratorProvider,
    RepoProvider,
    UseCaseProvider,
)


def make_http_container() -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        UseCaseProvider(),
        GeneratorProvider(),
        AuthProvider(),
        RepoProvider(),
        DBProvider(),
    )


def make_cli_container() -> Container:
    return make_container(
        AlembicConfigProvider(),
    )
