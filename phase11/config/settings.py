from dataclasses import dataclass
import os

from dotenv import load_dotenv


environment = os.getenv("APP_ENV", "development")

if environment == "production":
    load_dotenv(".env.production")
elif environment == "test":
    load_dotenv(".env.test")
else:
    load_dotenv(".env.development")


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