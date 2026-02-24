from typing import Any, Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.db import schemas
from app.crud.user_crud import user_crud


class UserService:
    """
    UserService - Layer xử lý business logic cho User
    (Tách biệt hoàn toàn khỏi Router/Controller)
    """

    def create_user(self, db: Session, user_in: schemas.UserCreate) -> Dict[str, Any]:
        """
        Tạo user mới
        - Kiểm tra username đã tồn tại chưa
        - Gọi CRUD để tạo (hash password nằm trong CRUD)
        - Chuẩn bị data response (jsonable + xóa password_hash)
        """
        # 1. Kiểm tra tồn tại
        existing_user = user_crud.get_by_username(db, username=user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # 2. Tạo user
        db_user = user_crud.create(db, obj_in=user_in)

        # 3. Chuẩn bị data response (xử lý datetime + bảo mật)
        data_response = jsonable_encoder(db_user)
        data_response.pop("password_hash", None)  # Bảo mật: không trả password_hash về client

        return data_response

    def get_user(self, db: Session, user_id: int):
        """Lấy thông tin user theo ID"""
        user = user_crud.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def activate_user(self, db: Session, user_id: int):
        """Kích hoạt tài khoản user"""
        user = user_crud.activate(db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def deactivate_user(self, db: Session, user_id: int):
        """Vô hiệu hóa tài khoản user"""
        user = user_crud.deactivate(db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user


# Instance tiện lợi để import (singleton style)
user_service = UserService()
