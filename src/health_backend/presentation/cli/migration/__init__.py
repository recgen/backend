import click

from health_backend.presentation.cli.migration.make import make_migration
from health_backend.presentation.cli.migration.upgrade import upgrade_migration


@click.group('migration')
def migration() -> None: ...


migration.add_command(make_migration, 'make')
migration.add_command(upgrade_migration, 'upgrade')
