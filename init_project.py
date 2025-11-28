import os
import sys

# ==========================================
# 프로젝트 파일 내용 정의 (Raw String 적용)
# ==========================================

# 1. requirements.txt
requirements_txt = """PyQt6
PyQt6-WebEngine
requests
pyinstaller
"""

# 2. .gitignore
gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
venv/
env/

# PyInstaller
*.spec
dist/
build/

# IDE
.idea/
.vscode/
*.swp
"""

# 3. README.md
readme_md = r"""# 사내 시스템 모니터링 도구 (System Monitor)

Postman 스타일의 API 모니터링 도구입니다. 내장 브라우저를 통해 로그인 세션을 획득하고, 다수의 API 상태를 일괄 점검합니다.

## 기술 스택
- Language: Python 3.9+
- GUI: PyQt6
- Browser Engine: PyQt6-WebEngine
- HTTP Client: Requests
- Build: PyInstaller

## 설치 및 실행 방법

1. 라이브러리 설치
   python -m pip install -r requirements.txt

2. 실행
   python main.py

## 설정 관리
- config/settings.py 파일에서 API 목록을 수정하세요.

## 배포 파일 생성 (exe)
   pyinstaller --noconsole --onedir --clean --name="SystemMonitor" main.py
"""

# 4. config/settings.py
settings_py = r"""# 시스템 설정 파일
LOGIN_URL = "https://your-system.com/login"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

TARGET_APIS = [
    {"name": "사용자 정보 API", "url": "https://your-system.com/api/v1/user/info"},
    {"name": "대시보드 통계",   "url": "https://your-system.com/api/v1/dashboard"},
    {"name": "알림 센터",       "url": "https://your-system.com/api/v1/notifications"},
]
"""

# 5. utils/logger.py
logger_py = r"""import logging
import sys

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger
"""

# 6. core/api_scanner.py
api_scanner_py = r"""import requests
from PyQt6.QtCore import QThread, pyqtSignal
from config.settings import TARGET_APIS, DEFAULT_HEADERS
from utils.logger import get_logger

log = get_logger("ApiScanner")

class ApiScannerThread(QThread):
    result_signal = pyqtSignal(str, str, int, str)
    finished_signal = pyqtSignal()

    def __init__(self, cookies):
        super().__init__()
        self.cookies = cookies

    def run(self):
        log.info("API 스캔 시작")
        session = requests.Session()
        session.headers.update(DEFAULT_HEADERS)
        
        for k, v in self.cookies.items():
            session.cookies.set(k, v)

        for api in TARGET_APIS:
            name = api['name']
            url = api['url']
            
            try:
                res = session.get(url, timeout=10)
                code = res.status_code
                status = "성공" if 200 <= code < 300 else "실패"
                
                log.debug(f"[{status}] {name} ({code})")
                self.result_signal.emit(name, url, code, status)
                
            except Exception as e:
                log.error(f"Error on {name}: {e}")
                self.result_signal.emit(name, url, 0, f"에러: {str(e)}")
        
        log.info("API 스캔 종료")
        self.finished_signal.emit()
"""

# 7. ui/login_dialog.py
login_dialog_py = r"""from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl
from config.settings import LOGIN_URL

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로그인 (사내 시스템)")
        self.resize(1024, 768)
        self.cookies = {}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.webview = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        
        self.cookie_store = profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.on_cookie_added)
        
        self.webview.setUrl(QUrl(LOGIN_URL))
        layout.addWidget(self.webview)

        btn = QPushButton("로그인 완료 및 닫기")
        btn.setStyleSheet("height: 40px; font-weight: bold; background-color: #007bff; color: white;")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

        self.setLayout(layout)

    def on_cookie_added(self, cookie):
        name = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')
        self.cookies[name] = value

    def get_cookies(self):
        return self.cookies
"""

# 8. ui/main_window.py
main_window_py = r"""from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox, QLabel)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

from ui.login_dialog import LoginDialog
from core.api_scanner import ApiScannerThread
from config.settings import TARGET_APIS

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cookies = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('사내 시스템 모니터링 도구 v1.0')
        self.resize(900, 600)
        
        layout = QVBoxLayout()

        self.lbl_status = QLabel(f"모니터링 대상: {len(TARGET_APIS)}개 API | 상태: 로그인 필요")
        self.lbl_status.setFont(QFont("Arial", 10))
        self.lbl_status.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.lbl_status)

        self.btn_login = QPushButton("1. 로그인 (Browser)")
        self.btn_login.clicked.connect(self.show_login_dialog)
        layout.addWidget(self.btn_login)

        self.btn_scan = QPushButton("2. 점검 시작 (Start)")
        self.btn_scan.clicked.connect(self.start_scan)
        self.btn_scan.setEnabled(False)
        layout.addWidget(self.btn_scan)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['API 명', 'Status', '결과', 'URL'])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def show_login_dialog(self):
        dlg = LoginDialog(self)
        if dlg.exec():
            self.cookies = dlg.get_cookies()
            if self.cookies:
                self.lbl_status.setText(f"로그인 완료 (세션 확보됨). 점검을 시작하세요.")
                self.lbl_status.setStyleSheet("padding: 10px; background-color: #d4edda; color: #155724;")
                self.btn_scan.setEnabled(True)
            else:
                QMessageBox.warning(self, "주의", "쿠키가 없습니다.")

    def start_scan(self):
        self.table.setRowCount(0)
        self.btn_scan.setEnabled(False)
        self.btn_scan.setText("스캔 진행 중...")

        self.scanner = ApiScannerThread(self.cookies)
        self.scanner.result_signal.connect(self.update_table)
        self.scanner.finished_signal.connect(self.on_scan_finished)
        self.scanner.start()

    def update_table(self, name, url, code, result):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(str(code)))
        self.table.setItem(row, 2, QTableWidgetItem(result))
        self.table.setItem(row, 3, QTableWidgetItem(url))

        if result != "성공":
            for i in range(4):
                self.table.item(row, i).setBackground(QColor(255, 200, 200))

    def on_scan_finished(self):
        self.btn_scan.setEnabled(True)
        self.btn_scan.setText("2. 점검 시작 (Start)")
        QMessageBox.information(self, "완료", "모니터링이 완료되었습니다.")
"""

# 9. main.py
main_py = r"""import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())
"""

# ==========================================
# [중요] 실제 파일 생성 로직
# ==========================================
def create_project():
    structure = {
        "requirements.txt": requirements_txt,
        ".gitignore": gitignore,
        "README.md": readme_md,
        "main.py": main_py,
        "config/settings.py": settings_py,
        "core/api_scanner.py": api_scanner_py,
        "ui/login_dialog.py": login_dialog_py,
        "ui/main_window.py": main_window_py,
        "utils/logger.py": logger_py,
    }

    print("🚀 프로젝트 생성 시작...")

    for path, content in structure.items():
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        # [중요] utf-8 인코딩 지정
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 생성됨: {path}")

    print("\n🎉 프로젝트 생성이 완료되었습니다!")
    print("------------------------------------------")
    print("1. 아래 명령어로 라이브러리 설치:")
    print("   python -m pip install -r requirements.txt")
    print("\n2. 실행:")
    print("   python main.py")
    print("------------------------------------------")

if __name__ == "__main__":
    create_project()