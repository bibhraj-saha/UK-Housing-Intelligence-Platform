from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv(
        "APP_NAME",
        "UK Housing Intelligence Platform",
    )
    app_env: str = os.getenv(
        "APP_ENV",
        "development",
    )
    api_host: str = os.getenv(
        "API_HOST",
        "127.0.0.1",
    )
    api_port: int = int(
        os.getenv(
            "API_PORT",
            "8000",
        )
    )
    log_level: str = os.getenv(
        "LOG_LEVEL",
        "DEBUG",
    )


settings = Settings()