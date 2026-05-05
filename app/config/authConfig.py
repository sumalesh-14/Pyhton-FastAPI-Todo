from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )
    
    secret_key : SecretStr
    algorithm : str = "HS256"
    access_token_expire_minutes : int = 10
    
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    LOG_FILE: str = "app.log"
    LOG_TO_FILE: bool = True
    LOG_TO_CONSOLE: bool = True

settings = Settings()