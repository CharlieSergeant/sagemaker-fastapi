import os
from dotenv import load_dotenv
import secrets
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = os.environ.get('PROJECT_NAME','sagemaker-fastapi')
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL','INFO')
    ROOT_PATH: str = None
    REGION: str = os.environ.get('REGION','us-west-2')
    RAW_BUCKET: str = os.environ.get('RAW_BUCKET')
    ARTIFACTS_BUCKET: str = os.environ.get('ARTIFACTS_BUCKET')
    OUTPUT_BUCKET: str = os.environ.get('OUTPUT_BUCKET')
    class Config:
        case_sensitive = True

settings = Settings()
