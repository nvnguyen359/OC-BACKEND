# app/services/gdrive_service.py
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json' 

# Đã xóa dòng TARGET_FOLDER_ID ở đây để dùng cấu hình động

class GDriveService:
    def __init__(self):
        self.creds = None
        self.service = None
        try:
            if os.path.exists(TOKEN_FILE):
                self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                    with open(TOKEN_FILE, 'w') as token:
                        token.write(self.creds.to_json())
                else:
                    print("❌ Lỗi: Không tìm thấy token.json hoặc bị hỏng. Hãy tạo lại từ máy tính.")
                    return
            
            self.service = build('drive', 'v3', credentials=self.creds)
            print("✅ Đã kết nối Google Drive API (OAuth 2.0) thành công.")
        except Exception as e:
            print(f"❌ Lỗi khởi tạo Google Drive: {e}")

    # [NEW] Thêm tham số folder_id vào hàm
    def upload_file_and_get_link(self, file_path: str, folder_id: str, mime_type: str = 'video/mp4') -> str:
        if not self.service or not os.path.exists(file_path):
            return None

        file_name = os.path.basename(file_path)
        
        # Sử dụng folder_id truyền vào thay vì hằng số
        file_metadata = {
            'name': file_name,
            'parents': [folder_id] 
        }
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        try:
            print(f"☁️ Đang upload {file_name} lên Drive (OAuth)...")
            uploaded_file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()

            file_id = uploaded_file.get('id')
            
            self.service.permissions().create(
                fileId=file_id,
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()

            link = uploaded_file.get('webViewLink')
            print(f"✅ Upload thành công! Link: {link}")
            return link

        except Exception as e:
            print(f"❌ Lỗi khi upload Drive: {e}")
            return None

gdrive_service = GDriveService()