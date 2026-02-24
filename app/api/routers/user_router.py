from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db import schemas
from app.db.session import get_db
from app.crud.user_crud import user_crud
from app.utils.response import response_success

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=dict)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra tồn tại
    existing_user = user_crud.get_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # 2. Tạo user (Logic hash password nằm trong CRUD)
    db_user = user_crud.create(db, obj_in=user_in)

    # 3. Chuyển đổi sang JSON-compatible dict
    data_response = jsonable_encoder(db_user)

    # Bảo mật: Xóa hash password
    data_response.pop("password_hash", None)

    return response_success(data=data_response)


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
        
    # [FIX]: Encode object thành dict và xóa password_hash
    data_response = jsonable_encoder(user)
    data_response.pop("password_hash", None)
    
    return response_success(data=data_response)


@router.post("/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.activate(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # [FIX]: Encode object thành dict và xóa password_hash
    data_response = jsonable_encoder(user)
    data_response.pop("password_hash", None)
    
    return response_success(data=data_response)


@router.post("/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.deactivate(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # [FIX]: Encode object thành dict và xóa password_hash
    data_response = jsonable_encoder(user)
    data_response.pop("password_hash", None)
    
    return response_success(data=data_response)


@router.get("", response_model=dict)
def get_all_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,  # ?search=admin
    role: Optional[str] = None,  # ?role=operator
):
    users = user_crud.get_multi(db, skip=skip, limit=limit, search=search, role=role)
    
    # [FIX]: Encode list các object thành list các dict
    data_response = jsonable_encoder(users)
    
    # Bảo mật: Lặp qua từng user và xóa password_hash trước khi trả về
    for u in data_response:
        u.pop("password_hash", None)
        
    return response_success(data=data_response)
@router.patch("/{user_id}", response_model=dict)
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Chuyển đổi dữ liệu gửi lên thành dict, loại bỏ các trường bị rỗng (không cập nhật)
    update_data = user_in.model_dump(exclude_unset=True)
    
    # Nếu có gửi password mới -> Băm (hash) mật khẩu
    if "password" in update_data and update_data["password"]:
        from app.core.security import hash_password
        update_data["password_hash"] = hash_password(update_data.pop("password"))
    elif "password" in update_data:
        update_data.pop("password") # Nếu gửi pass rỗng thì bỏ qua
        
    # Gọi hàm update từ CRUD
    db_user = user_crud.update(db, db_obj=db_user, obj_in=update_data)
    
    data_response = jsonable_encoder(db_user)
    data_response.pop("password_hash", None)
    
    return response_success(data=data_response, mes="Cập nhật thành công")