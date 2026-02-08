from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    yandex_cloud_url: str
    yandex_cloud_api_key: str
    yandex_cloud_folder: str
    yandex_cloud_model: str

    secret: str

    frontend_origin: str

    host: str = 'localhost'
    port: int = 8000

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @property
    def db_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.db_user}:{self.db_password}'
            f'@{self.db_host}:{self.db_port}/{self.db_name}'
        )

    model_config = SettingsConfigDict(env_file='.env')


config = Config()  # ty: ignore missing-argument
