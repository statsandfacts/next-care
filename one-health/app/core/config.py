from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Next Care"
    API_V1_STR: str = "/api/v1"
    # SECRET_KEY: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int
    # USERS_OPEN_REGISTRATION: str
    #
    # ENVIRONMENT: Optional[str]
    #
    # FIRST_SUPER_ADMIN_EMAIL: str
    # FIRST_SUPER_ADMIN_PASSWORD: str
    # FIRST_SUPER_ADMIN_ACCOUNT_NAME: str

    DB_HOST: str = "database-2.clyyseo20cva.us-east-2.rds.amazonaws.com"
    DB_USER: str = "admin"
    DB_PASSWORD: str = "12345678"
    

    SQLALCHEMY_DATABASE_URI: Optional[str] = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}/{values.get('DB_NAME')}"

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
