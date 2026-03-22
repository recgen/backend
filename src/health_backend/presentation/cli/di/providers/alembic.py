from pathlib import Path

from alembic.config import Config as AlembicConfig
from dishka import Provider, Scope, provide


class AlembicConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_alembic_config(self) -> AlembicConfig:
        ini_file_path = str(
            Path(__file__).parent.parent.parent.parent.parent.parent.parent / 'alembic.ini'
        )
        scripts_path = str(
            Path(__file__).parent.parent.parent.parent.parent.parent.parent / 'alembic'
        )
        config = AlembicConfig(file_=ini_file_path)
        config.set_main_option('script_location', scripts_path)
        return config
