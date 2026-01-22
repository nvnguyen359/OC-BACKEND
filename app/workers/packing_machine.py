# app/workers/packing_machine.py
import time
from datetime import datetime

# Import Enum từ file chung
from app.core.oc_enums import MachineState, Action

class PackingStateMachine:
    def __init__(self):
        self.state = MachineState.IDLE
        self.current_code = None
        
        # --- CẤU HÌNH TỐI ƯU ---
        # [FIX] Giảm Vote xuống 0.5s để bắt đơn cực nhanh
        self.VOTE_DURATION = 0.5 
        # [FIX] Cooldown ngắn lại để scan đơn tiếp theo nhanh hơn
        self.COOLDOWN_DURATION = 1.0
        self.SNAPSHOT_DELAY = 5.0
        
        # Biến cấu hình động
        self.TIMEOUT_DURATION = 60.0
        self.WORK_END_TIME = "18:30"
        
        # --- BIẾN RUNTIME ---
        self.buffer_start_time = 0
        self.buffer_votes = {}
        self.packing_start_time = 0
        self.last_human_seen_time = 0
        self.snapshot_taken = False
        self.scan_new_code_counter = 0
        self.last_closed_code = None
        self.last_closed_time = 0

    def update_config(self, timeout_sec: int, end_time_str: str):
        try:
            if timeout_sec > 10: self.TIMEOUT_DURATION = float(timeout_sec)
            datetime.strptime(end_time_str, "%H:%M")
            self.WORK_END_TIME = end_time_str
        except: pass

    def _is_shift_ended(self) -> bool:
        try:
            now = datetime.now()
            end_h, end_m = map(int, self.WORK_END_TIME.split(':'))
            if now.hour > end_h or (now.hour == end_h and now.minute >= end_m):
                return True
            return False
        except: return False

    def process(self, detected_codes: list, has_human: bool) -> tuple[MachineState, Action, str, str]:
        now = time.time()
        action = Action.NONE
        reason = ""
        target_code = self.current_code

        is_ended = self._is_shift_ended()

        # 1. Check Hết ca
        if self.state in [MachineState.IDLE, MachineState.BUFFERING]:
            if is_ended:
                self.state = MachineState.IDLE
                return self.state, Action.NONE, None, "SHIFT_ENDED"

        if self.state == MachineState.PACKING and is_ended:
            action = Action.STOP_ORDER
            reason = "END_SHIFT"
            self._reset_state(save_history=True)
            return self.state, action, target_code, reason

        # 2. Logic Máy Trạng Thái
        if self.state == MachineState.IDLE:
            if detected_codes:
                self.state = MachineState.BUFFERING
                self.buffer_start_time = now
                self.buffer_votes = {}
        
        elif self.state == MachineState.BUFFERING:
            for code in detected_codes:
                self.buffer_votes[code] = self.buffer_votes.get(code, 0) + 1
            
            # Kiểm tra thời gian Vote (Đã giảm xuống 0.5s)
            if now - self.buffer_start_time >= self.VOTE_DURATION:
                if not self.buffer_votes:
                    self.state = MachineState.IDLE
                else:
                    best_code = max(self.buffer_votes, key=self.buffer_votes.get)
                    
                    # Check Cooldown để không bắt lại đơn vừa đóng
                    if best_code == self.last_closed_code and (now - self.last_closed_time < self.COOLDOWN_DURATION):
                        self.state = MachineState.IDLE
                    else:
                        self._start_internal(best_code, now)
                        action = Action.START_ORDER
                        target_code = best_code

        elif self.state == MachineState.PACKING:
            # Keep-Alive
            if has_human:
                self.last_human_seen_time = now
            elif (now - self.last_human_seen_time > self.TIMEOUT_DURATION):
                action = Action.STOP_ORDER
                reason = "TIMEOUT"
                self._reset_state(save_history=True)
                return self.state, action, target_code, reason

            # Snapshot
            if not self.snapshot_taken and (now - self.packing_start_time >= self.SNAPSHOT_DELAY):
                self.snapshot_taken = True
                action = Action.SNAPSHOT

            # Scan New Code (Chuyển đơn nhanh)
            found_new_persistent = False
            for code in detected_codes:
                if code != self.current_code:
                    self.scan_new_code_counter += 1
                    found_new_persistent = True
                    # Giảm ngưỡng counter xuống 10 frame (0.5s) để chuyển đơn nhanh hơn
                    if self.scan_new_code_counter > 10:
                        old_code = self.current_code
                        new_code = code
                        self.last_closed_code = old_code
                        self.last_closed_time = now
                        self._start_internal(new_code, now)
                        return self.state, Action.SWITCH_ORDER, new_code, "SCAN_NEW"
            if not found_new_persistent:
                self.scan_new_code_counter = 0

        return self.state, action, target_code, reason

    def force_start(self, code: str):
        now = time.time()
        self._start_internal(code, now)
        return Action.START_ORDER

    def manual_stop(self):
        if self.state == MachineState.PACKING:
            code = self.current_code
            self._reset_state(save_history=True)
            return Action.STOP_ORDER, code
        return Action.NONE, None

    def _start_internal(self, code, now_time):
        self.state = MachineState.PACKING
        self.current_code = code
        self.packing_start_time = now_time
        self.last_human_seen_time = now_time
        self.snapshot_taken = False
        self.scan_new_code_counter = 0

    def _reset_state(self, save_history=False):
        if save_history:
            self.last_closed_code = self.current_code
            self.last_closed_time = time.time()
        self.state = MachineState.IDLE
        self.current_code = None
        self.buffer_votes = {}