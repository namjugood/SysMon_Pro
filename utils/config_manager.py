import json
import os

URLS_FILE = "login_urls.json"
SESSION_FILE = "session.json"

class ConfigManager:
    # ---------------------------------------------------------
    # 1. URL 관리 (옵션 팝업용)
    # ---------------------------------------------------------
    @staticmethod
    def load_urls():
        """저장된 URL 목록 불러오기"""
        if not os.path.exists(URLS_FILE):
            return []
        try:
            with open(URLS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def save_urls(data):
        """URL 목록 저장하기"""
        with open(URLS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ---------------------------------------------------------
    # 2. 세션 관리 (자동 로그인용) - [이 부분이 누락되었습니다]
    # ---------------------------------------------------------
    @staticmethod
    def save_session(url, cookies, page_name):
        """마지막 로그인 세션 정보 저장"""
        data = {
            "base_url": url,
            "cookies": cookies,
            "page_name": page_name
        }
        try:
            with open(SESSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Failed to save session: {e}")

    @staticmethod
    def load_session():
        """저장된 세션 정보 불러오기"""
        if not os.path.exists(SESSION_FILE):
            return None
        try:
            with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    @staticmethod
    def clear_session():
        """세션 파일 삭제 (로그아웃 시)"""
        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)
            except:
                pass