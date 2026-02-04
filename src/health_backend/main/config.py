from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    yandex_cloud_url: str
    yandex_cloud_api_key: str
    yandex_cloud_folder: str
    yandex_cloud_model: str

    model_config = SettingsConfigDict(env_file='.env')


config = Config()  # ty: ignore missing-argument
