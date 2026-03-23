from dataclasses import dataclass


@dataclass
class YandexCloudConfig:
    api_url: str
    api_key: str
    folder: str
    model: str


@dataclass
class PostgresConfig:
    url: str


@dataclass
class JWTConfig:
    secret: str


@dataclass
class APIConfig:
    origins: list[str]
