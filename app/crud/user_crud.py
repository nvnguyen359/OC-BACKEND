from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db import models, schemas
from app.crud.base import CRUDBase
from app.core.security import hash_password


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    
    def get_by_username(self, db: Session, username: str):
        """Lấy user theo username (dùng cho login & kiểm tra tồn tại)"""
        return db.query(self.model).filter(self.model.username == username).first()

    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,      # ← Tìm kiếm theo username hoặc full_name
        role: Optional[str] = None         # ← Lọc theo role (admin, supervisor, operator)
    ) -> List[models.User]:
        """
        Lấy danh sách user có hỗ trợ tìm kiếm và lọc
        - search: tìm trong username hoặc full_name (không phân biệt hoa thường)
        - role: lọc chính xác theo role
        """
        query = db.query(self.model)

        # Tìm kiếm
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    self.model.username.ilike(search_term),
                    self.model.full_name.ilike(search_term)
                )
            )

        # Lọc theo role
        if role:
            query = query.filter(self.model.role == role)

        # Phân trang
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: schemas.UserCreate) -> models.User:
        """Tạo user mới - Hash password chỉ 1 lần ở đây"""
        obj_in_data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in.dict()
        
        raw_password = obj_in_data.pop("password")
        obj_in_data["password_hash"] = hash_password(raw_password)
        
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def activate(self, db: Session, user_id: int):
        """Kích hoạt user"""
        user = self.get(db, id=user_id)
        if user:
            user.is_active = 1
            db.commit()
            db.refresh(user)
        return user

    def deactivate(self, db: Session, user_id: int):
        """Vô hiệu hóa user"""
        user = self.get(db, id=user_id)
        if user:
            user.is_active = 0
            db.commit()
            db.refresh(user)
        return user


# Instance dùng toàn app
user_crud = CRUDUser(models.User)