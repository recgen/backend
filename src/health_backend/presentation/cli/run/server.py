import click
import uvicorn


@click.command()
@click.option('--app', default='health_backend.main.server:main', help='Server app')
@click.option('--host', default='localhost', help='Server host')
@click.option('--port', default=8080, help='Server port')
def run_server(app: str, port: int, host: int) -> None:
    uvicorn.run(app=app, host=host, port=port)
