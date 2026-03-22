import click

from health_backend.presentation.cli.run.server import run_server


@click.group(name='run')
def run() -> None: ...


run.add_command(run_server, name='server')
