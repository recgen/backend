from dishka import Container, make_container

from health_backend.presentation.cli.di.providers.alembic import AlembicConfigProvider


def make_cli_container() -> Container:
    return make_container(
        AlembicConfigProvider(),
    )
