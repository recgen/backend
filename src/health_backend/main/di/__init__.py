from dishka import make_async_container

from health_backend.main.di.providers import GeneratorProvider, UseCaseProvider

container = make_async_container(
    UseCaseProvider(),
    GeneratorProvider(),
)
