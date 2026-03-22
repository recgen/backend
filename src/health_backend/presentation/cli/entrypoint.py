import click
from dishka.integrations.click import setup_dishka

from health_backend.presentation.cli.di.container import make_cli_container
from health_backend.presentation.cli.migration import migration


@click.group()
@click.pass_context
def cli(context: click.Context) -> None:
    container = make_cli_container()
    setup_dishka(container, context=context)


cli.add_command(migration, 'migration')

if __name__ == '__main__':
    cli()
