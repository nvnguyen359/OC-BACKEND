# app/crud/order_crud.py
import os
import pytz
from typing import List, Tuple, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_, or_, func, extract
from datetime import datetime, timedelta
from app.db import models, schemas
from app.crud.base import CRUDBase

class CRUDOrder(CRUDBase[models.Order, schemas.OrderCreate, schemas.OrderUpdate]):
    """
    CRUD Order Nâng Cao:
    - Xử lý múi giờ Việt Nam (ICT).
    - Logic "Hydration": Tự động nạp thêm cha/con/anh em bị thiếu do phân trang.
    - Logic "Consolidation": Gom nhóm theo Code (Mới nhất làm Chính, Cũ làm History).
    - Optimization: Loại bỏ object Parent lồng nhau để giảm tải JSON.
    - Tự động dọn dẹp Video/Avatar khi xóa dữ liệu.
    - [NEW] Bộ lọc theo Tháng, Quý, Năm.
    """

    def _get_vn_now(self):
        """Lấy thời gian hiện tại chuẩn Asia/Ho_Chi_Minh"""
        return datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))

    def remove_all(self, db: Session) -> int:
        """
        Xóa toàn bộ dữ liệu Order và dọn dẹp file vật lý trên ổ đĩa.
        """
        all_orders = db.query(self.model).all()
        base_path = os.getcwd()

        for order in all_orders:
            # Xử lý xóa cả Video và Avatar
            for file_attr in [order.path_video, order.path_avatar]:
                if file_attr:
                    full_path = file_attr if os.path.isabs(file_attr) else os.path.join(base_path, file_attr)
                    try:
                        if os.path.exists(full_path):
                            os.remove(full_path)
                    except Exception as e:
                        print(f"[OrderCRUD] ⚠️ Không thể xóa file: {full_path} | {e}")

        # Xóa bản ghi trong database
        rows_deleted = db.query(self.model).delete()
        db.commit()
        return rows_deleted

    def filter_orders(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        code: str = None,
        status: str = None,
        date_preset: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        month: int = None,    # [NEW] Lọc theo tháng (1-12)
        quarter: int = None,  # [NEW] Lọc theo quý (1-4)
        year: int = None,     # [NEW] Lọc theo năm (ví dụ: 2024)
        sort_by: str = "created_at",
        sort_dir: str = "desc",
    ) -> Tuple[List[models.Order], int]:
        """
        Lọc đơn hàng -> Bù đắp dữ liệu (Hydration) -> Gom nhóm & Tối ưu (Consolidation).
        """
        vn_now = self._get_vn_now()
        
        # --- BƯỚC 1: XÂY DỰNG QUERY CHÍNH (PRIMARY QUERY) ---
        # Query này chịu trách nhiệm Lọc và Phân trang
        query = select(self.model).options(joinedload(self.model.parent))

        # 1.1. Filter by Code
        if code:
            code_list = [c.strip() for c in code.split(",") if c.strip()]
            conditions = [self.model.code.contains(c) for c in code_list]
            query = query.where(or_(*conditions))
        
        else:
            # 1.2. Filter by Date
            
            # --- [NEW LOGIC] Lọc theo Năm/Tháng/Quý ---
            # Sử dụng extract của SQLAlchemy để lấy phần ngày tháng từ DB
            if year:
                query = query.where(extract('year', self.model.created_at) == year)
            
            if month:
                query = query.where(extract('month', self.model.created_at) == month)
            
            if quarter:
                # Logic tính quý: (month - 1) / 3 + 1. Ví dụ: Tháng 4 -> (3)/3 + 1 = 2 (Quý 2)
                query = query.where(
                    func.floor((extract('month', self.model.created_at) - 1) / 3) + 1 == quarter
                )

            # --- Logic Date Preset & Range (Chỉ chạy nếu không có bộ lọc Năm/Tháng/Quý cụ thể để tránh xung đột) ---
            # (Hoặc bạn có thể bỏ 'if not' nếu muốn kết hợp, nhưng thường thì đã lọc tháng rồi thì không cần lọc 'last7days')
            if not (year or month or quarter):
                today_start = vn_now.replace(hour=0, minute=0, second=0, microsecond=0)
                
                if date_preset == "today":
                    query = query.where(and_(self.model.created_at >= today_start, 
                                             self.model.created_at < today_start + timedelta(days=1)))
                elif date_preset == "yesterday":
                    start = today_start - timedelta(days=1)
                    query = query.where(and_(self.model.created_at >= start, self.model.created_at < today_start))
                elif date_preset == "last7days":
                    query = query.where(self.model.created_at >= today_start - timedelta(days=7))
                elif date_preset == "last15days":
                    query = query.where(self.model.created_at >= today_start - timedelta(days=15))

                # Lọc theo Range ngày cụ thể (Start/End)
                if start_date and end_date:
                    query = query.where(
                        and_(
                            self.model.created_at >= start_date,
                            or_(self.model.closed_at <= end_date, self.model.closed_at.is_(None))
                        )
                    )

        # 1.3. Filter Status
        if status:
            query = query.where(self.model.status == status)

        # 1.4. Sorting (Áp dụng cho phân trang chính)
        if hasattr(self.model, sort_by):
            sort_col = getattr(self.model, sort_by)
            query = query.order_by(sort_col.desc() if sort_dir == "desc" else sort_col.asc())

        # --- BƯỚC 2: THỰC THI QUERY CHÍNH ---
        
        # Đếm tổng (cho phân trang UI)
        count_query = select(func.count()).select_from(query.subquery())
        total = db.execute(count_query).scalar() or 0
        
        # Lấy dữ liệu trang hiện tại (Primary Items)
        primary_items = db.execute(query.offset(skip).limit(limit)).scalars().all()

        if not primary_items:
            return [], total

        # --- BƯỚC 3: HYDRATION (TRUY VẤN BỔ SUNG) ---
        # Mục tiêu: Tìm cha/con/anh em của primary_items mà CHƯA có trong list này
        
        collected_ids = {item.id for item in primary_items}
        collected_codes = {item.code for item in primary_items if item.code}
        collected_parent_ids = {item.parent_id for item in primary_items if item.parent_id}

        hydration_conditions = []
        if collected_codes:
            hydration_conditions.append(self.model.code.in_(collected_codes))
        if collected_ids:
            hydration_conditions.append(self.model.parent_id.in_(collected_ids)) # Tìm con
        if collected_parent_ids:
            hydration_conditions.append(self.model.id.in_(collected_parent_ids)) # Tìm cha

        missing_items = []
        if hydration_conditions:
            # Query này KHÔNG lọc theo ngày tháng/status để đảm bảo tìm đủ gia phả
            hydrate_query = select(self.model).options(joinedload(self.model.parent))
            hydrate_query = hydrate_query.where(
                and_(
                    or_(*hydration_conditions),
                    self.model.id.notin_(collected_ids) # Tránh lấy trùng đơn đã có
                )
            )
            missing_items = db.execute(hydrate_query).scalars().all()

        # --- BƯỚC 4: CONSOLIDATION (GOM NHÓM & TỐI ƯU DUNG LƯỢNG) ---
        # Gộp list chính và list bổ sung
        flat_list = list(primary_items) + list(missing_items)
        
        grouped_orders: Dict[str, List[models.Order]] = {}
        standalone_items: List[models.Order] = []

        # 4.1. Phân loại item vào các nhóm
        for item in flat_list:
            if item.code:
                if item.code not in grouped_orders:
                    grouped_orders[item.code] = []
                grouped_orders[item.code].append(item)
            else:
                standalone_items.append(item)

        consolidated_result = []

        # 4.2. Xử lý từng nhóm (Logic Mới nhất làm Chính - Cũ làm History)
        for code, items in grouped_orders.items():
            # Sắp xếp giảm dần theo thời gian (Mới nhất lên đầu)
            items.sort(key=lambda x: x.created_at or datetime.min, reverse=True)

            # Phần tử đầu tiên là MAIN (Mới nhất)
            main_item = items[0]
            
            # Các phần tử còn lại là HISTORY
            history_items = items[1:]
            
            # [QUAN TRỌNG] TỐI ƯU HÓA JSON: CẮT BỎ PARENT OBJECT
            # Vì dữ liệu đã được gom vào history, việc giữ object parent lồng nhau là dư thừa
            main_item.parent = None 
            for h_item in history_items:
                h_item.parent = None

            # Gán danh sách phụ vào thuộc tính động 'history_logs'
            setattr(main_item, "history_logs", history_items)
            
            consolidated_result.append(main_item)

        # 4.3. Xử lý các item lẻ (Không có code)
        for item in standalone_items:
            item.parent = None # Clean up
            setattr(item, "history_logs", [])
            consolidated_result.append(item)

        # --- BƯỚC 5: SORT LẠI KẾT QUẢ CUỐI CÙNG ---
        # Sắp xếp lại danh sách kết quả dựa trên item chính
        reverse_sort = True if sort_dir == "desc" else False
        
        def get_sort_key(obj):
            val = getattr(obj, sort_by, None)
            return val if val is not None else (datetime.min if sort_by == 'created_at' else '')

        consolidated_result.sort(key=get_sort_key, reverse=reverse_sort)

        return consolidated_result, total

    def start_order(self, db: Session, order_id: int):
        db_obj = self.get(db, id=order_id)
        if db_obj:
            db_obj.status = "processing"
            db_obj.start_at = self._get_vn_now()
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def close_order(self, db: Session, order_id: int, status: str = "closed"):
        db_obj = self.get(db, id=order_id)
        if db_obj:
            db_obj.status = status
            db_obj.closed_at = self._get_vn_now()
            db.commit()
            db.refresh(db_obj)
        return db_obj

order_crud = CRUDOrder(models.Order)