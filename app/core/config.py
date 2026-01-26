# app/core/config.py

import os
import json 
from pathlib import Path
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# [FIX] XÁC ĐỊNH ĐƯỜNG DẪN TUYỆT ĐỐI TỚI FILE .ENV
# __file__ = .../app/core/config.py
# .parent  = .../app/core
# .parent.parent = .../app
# .parent.parent.parent = .../ (Thư mục gốc chứa .env)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # Server config
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # Database
    DB_URL: str = "sqlite:///./app/db/adocv1.db"

    # JWT config (CHỮ IN HOA)
    JWT_SECRET: str = "default_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 6000

    # Logging
    LOG_LEVEL: str = "info"
    OPENCV_LOG_LEVEL: str = "OFF"
    OPENCV_VIDEOIO_PRIORITY_MSMF: int = 0

    # Pagination defaults
    DEFAULT_PAGE: int = 0
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1500

    # CORS origins
    ALLOWED_ORIGINS: Union[List[str], str] = []

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if not v: return []
            if v.strip().startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    return []
            return [origin.strip() for origin in v.split(",")]
        elif isinstance(v, list):
            return v
        return []

    model_config = SettingsConfigDict(
        # [QUAN TRỌNG] Trỏ thẳng vào đường dẫn tuyệt đối của file .env
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

# Khởi tạo settings ở cuối file
settings = Settings()

# [DEBUG LOG] In ra để kiểm tra
print("---------------------------------------------------")
print(f"✅ [Config] Config File: {__file__}")
print(f"✅ [Config] Env Path Target: {ENV_PATH}")
print(f"✅ [Config] Env Exists: {ENV_PATH.exists()}")
print(f"🔓 [Config] ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS}")
print("---------------------------------------------------")