from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_ignore_empty=True,
    )

    cloud_ws_url: str
    device_token: str

    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_username: str | None = None
    mqtt_password: str | None = None
    mqtt_client_id: str
    mqtt_clean_session: bool = False
    mqtt_keepalive: int = 60


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
