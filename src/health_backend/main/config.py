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

    model_config = SettingsConfigDict(env_file='.env')


config = Config()  # ty: ignore missing-argument
