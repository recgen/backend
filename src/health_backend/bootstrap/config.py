from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    )


config = Config()  # type: ignore
