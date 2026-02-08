from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from health_backend.main.di.providers import (
    AuthProvider,
    DBProvider,
    GeneratorProvider,
    RepoProvider,
    UseCaseProvider,
)

container = make_async_container(
    FastapiProvider(),
    UseCaseProvider(),
    GeneratorProvider(),
    AuthProvider(),
    RepoProvider(),
    DBProvider(),
)
