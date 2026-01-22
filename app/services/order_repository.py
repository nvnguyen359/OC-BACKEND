# app/services/order_repository.py
from datetime import datetime
from typing import Optional
from app.db.session import SessionLocal
from app.db.models import Order
# Import Enum vừa tạo ở Bước 1
from app.core.oc_enums import OrderStatus, OrderNote

class OrderRepository:
    
    def get_latest_order_by_code(self, code: str) -> Optional[Order]:
        """
        Tìm đơn hàng mới nhất của mã vận đơn này trong Database.
        Dùng để kiểm tra xem mã này đã từng được đóng trong ngày chưa (Logic Sự kiện A).
        """
        db = SessionLocal()
        try:
            # Lấy đơn mới nhất (sắp xếp giảm dần theo thời gian tạo)
            # Chỉ lấy các đơn chưa bị Hủy (để tránh nối vào các đơn rác)
            order = db.query(Order)\
                      .filter(Order.code == code, Order.status != OrderStatus.CANCELLED)\
                      .order_by(Order.created_at.desc())\
                      .first()
            return order
        except Exception as e:
            print(f"⚠️ DB Error (get_latest): {e}")
            return None
        finally:
            db.close()

    def create_order(self, code: str, cam_id: int, parent_id: int = None, note: str = None) -> int:
        """
        Tạo đơn hàng mới (Sự kiện A).
        - parent_id: ID của đơn gốc (nếu là đóng lại).
        - note: Ghi chú khởi tạo (New/Repack).
        """
        db = SessionLocal()
        try:
            # Tự động gán Note mặc định nếu không truyền vào
            initial_note = note
            if not initial_note:
                # Nếu có parent_id -> Mặc định là Repack, ngược lại là New
                initial_note = OrderNote.REPACK if parent_id else OrderNote.NEW_ORDER

            new_order = Order(
                code=code, 
                camera_id=cam_id,
                parent_id=parent_id,            # [MỚI] Lưu liên kết cha-con
                status=OrderStatus.PACKING,     # [MỚI] Dùng Enum chuẩn
                note=initial_note,              # [MỚI] Lưu lý do tạo
                start_at=datetime.now(), 
                created_at=datetime.now()
            )
            
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            return new_order.id
        except Exception as e:
            print(f"❌ DB Error (create): {e}")
            return None
        finally:
            db.close()

    def close_order(self, order_id: int, reason_enum: str):
        """
        Kết thúc đơn hàng thành công (Sự kiện C1, C2, C3).
        reason_enum: Lấy từ OrderNote (TIMEOUT, SCAN_NEW, MANUAL...).
        """
        if not order_id: return
        db = SessionLocal()
        try:
            order = db.query(Order).get(order_id)
            if order and order.status == OrderStatus.PACKING:
                order.status = OrderStatus.CLOSED
                order.closed_at = datetime.now()
                order.note = reason_enum # Lưu lý do đóng chuẩn
                db.commit()
        except Exception as e:
            print(f"❌ DB Error (close): {e}")
        finally:
            db.close()

    def cancel_order(self, order_id: int):
        """
        [MỚI] Hủy đơn hàng (Sự kiện C4).
        Dùng khi hệ thống phát hiện 6s đầu chỉ là kiểm tra hàng, không phải đóng gói.
        """
        if not order_id: return
        db = SessionLocal()
        try:
            order = db.query(Order).get(order_id)
            if order:
                # Đánh dấu là Đã Hủy (Soft Delete)
                order.status = OrderStatus.CANCELLED
                order.closed_at = datetime.now()
                order.note = OrderNote.CHECKING_ONLY
                db.commit()
                print(f"🗑️ Order #{order_id} cancelled (Checking only).")
        except Exception as e:
            print(f"❌ DB Error (cancel): {e}")
        finally:
            db.close()

    def update_avatar(self, order_id: int, path: str):
            if not order_id: return
            db = SessionLocal()
            try:
                order = db.query(Order).get(order_id)
                if order:
                    order.path_avatar = path
                    db.commit()
                    # Thêm dòng này để confirm trên console
                    print(f"✅ DB Updated Avatar: Order #{order_id} -> {path}")
                else:
                    print(f"⚠️ Update Avatar Failed: Order #{order_id} not found")
            except Exception as e:
                print(f"❌ DB Error (update_avatar): {e}")
            finally:
                db.close()

# Singleton Instance
order_repo = OrderRepository()