import click
from alembic.command import revision
from alembic.config import Config as AlembicConfig
from dishka import FromDishka
from dishka.integrations.click import inject


@click.command()
@click.option('--message', help='Revision message')
@click.option('--autogenerate', default=True, help='Autogenerate migration flag')
@inject
def make_migration(
    message: str | None, autogenerate: bool, config: FromDishka[AlembicConfig]
) -> None:
    revision(config=config, message=message, autogenerate=autogenerate)
