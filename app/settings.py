from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class AiEnum(str, Enum):
    OLLAMA = 'OLLAMA'
    GPT = 'GPT'


class Settings(BaseSettings):
    APP_PORT: int = 8000
    APP_HOST: str = '0.0.0.0'
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB:str
    DATABASE_URL: str
    OPENAI_API_KEY: str = 'not-needed-for-ollama'
    MODEL: AiEnum = AiEnum.OLLAMA 

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        use_enum_values=True,
    )


settings = Settings()
