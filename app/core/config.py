# app/core/config.py
import os
import json 
from pathlib import Path
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# [QUAN TRỌNG] TÍNH TOÁN ĐƯỜNG DẪN GỐC (PROJECT ROOT)
# File này: .../app/core/config.py
# .parent -> core
# .parent.parent -> app
# .parent.parent.parent -> ROOT PROJECT (Thư mục chứa .env)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Đường dẫn tuyệt đối tới file .env
ENV_PATH = PROJECT_ROOT / ".env"

# [SỬA LẠI] Đường dẫn tuyệt đối tới file DB (Nằm ngay tại GỐC dự án)
# D:\Projects\OC\OC-BACkEND\adocv1.db
DB_FILE_PATH = PROJECT_ROOT / "adocv1.db"

class Settings(BaseSettings):
    # Server config
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # [FIX] Luôn dùng đường dẫn tuyệt đối trỏ về file ở GỐC
    DB_URL: str = f"sqlite:///{DB_FILE_PATH}"

    # JWT config
    JWT_SECRET: str = "default_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 6000

    # Logging
    LOG_LEVEL: str = "info"
    OPENCV_LOG_LEVEL: str = "OFF"
    OPENCV_VIDEOIO_PRIORITY_MSMF: int = 0

    # Pagination
    DEFAULT_PAGE: int = 0
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1500

    # CORS
    ALLOWED_ORIGINS: Union[List[str], str] = []

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if not v: return []
            try: return json.loads(v)
            except: return [origin.strip() for origin in v.split(",")]
        elif isinstance(v, list):
            return v
        return []

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# [FIX LOGIC - GHI ĐÈ CUỐI CÙNG]
# Bất kể file .env viết gì (kể cả viết sai thành ./app/db/...), 
# ta vẫn ép buộc nó quay về đúng DB_FILE_PATH đã định nghĩa ở trên.
settings.DB_URL = f"sqlite:///{DB_FILE_PATH}"

print("---------------------------------------------------")
print(f"📂 [Config] Project Root: {PROJECT_ROOT}")
print(f"📂 [Config] Database File: {DB_FILE_PATH}")
print(f"📂 [Config] FINAL DB URL: {settings.DB_URL}")
print("---------------------------------------------------")