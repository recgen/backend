from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    openrouter_url: str
    openrouter_model: str
    openrouter_api_key: str

    model_config = SettingsConfigDict(env_file='.env')


config = Config()  # ty: ignore missing-argument
