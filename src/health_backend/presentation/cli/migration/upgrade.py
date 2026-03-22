import click
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from dishka import FromDishka
from dishka.integrations.click import inject


@click.command()
@click.option('--revision', default='head', help='Migration revision')
@inject
def upgrade_migration(revision: str, config: FromDishka[AlembicConfig]) -> None:
    upgrade(config=config, revision=revision)
