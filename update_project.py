import os
import sys

# ==========================================
# 1. 파일 내용 정의 (새로운 디자인 적용)
# ==========================================

# 1. requirements.txt
requirements_txt = """PyQt6
requests
"""

# 2. config/settings.py
settings_py = r"""# 설정 파일
APP_TITLE = "SysMon Pro"
APP_VERSION = "v2.0"
MOCK_DATA_COUNT = 50

# (기존 설정 유지를 위해 남겨둠)
LOGIN_URL = "https://your-system.com/login"
"""

# 3. utils/styles.py (수정됨: 따옴표 충돌 해결)
styles_py = r'''from PyQt6.QtGui import QColor

class AppStyle:
    # SysMon Pro 테마 색상 정의
    COLOR_BG_MAIN = "#1e1e2e"       # 메인 배경
    COLOR_BG_PANEL = "#262638"      # 패널 배경
    COLOR_BORDER = "#383850"        # 테두리
    COLOR_TEXT = "#cdd6f4"          # 기본 텍스트
    COLOR_HEADER = "#313244"        # 헤더 배경
    COLOR_ACCENT = "#89b4fa"        # 강조색 (Blue)
    COLOR_SUCCESS = "#a6e3a1"       # 성공 (Green)
    COLOR_ERROR = "#f38ba8"         # 에러 (Red)
    
    # f-string을 사용하여 색상 변수 적용
    DARK_THEME = f"""
    QWidget {{
        background-color: {COLOR_BG_MAIN};
        color: {COLOR_TEXT};
        font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
    }}
    
    /* 패널 및 컨테이너 */
    QFrame, QTableWidget, QTextEdit {{
        background-color: {COLOR_BG_PANEL};
        border: 1px solid {COLOR_BORDER};
        border-radius: 6px;
    }}

    /* 테이블 스타일 */
    QTableWidget {{
        gridline-color: {COLOR_BORDER};
        selection-background-color: #45475a;
    }}
    QHeaderView::section {{
        background-color: {COLOR_HEADER};
        color: #a6adc8;
        padding: 8px;
        border: none;
        font-weight: bold;
    }}
    QTableCornerButton::section {{
        background-color: {COLOR_HEADER};
        border: none;
    }}

    /* 버튼 스타일 */
    QPushButton {{
        background-color: #585b70;
        color: white;
        border-radius: 4px;
        padding: 6px 12px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #6c7086;
    }}
    QPushButton#primary {{
        background-color: {COLOR_ACCENT};
        color: #1e1e2e;
    }}
    
    /* 입력 필드 */
    QLineEdit, QDateEdit {{
        background-color: #181825;
        border: 1px solid {COLOR_BORDER};
        padding: 4px;
        color: {COLOR_TEXT};
    }}

    /* 스플리터 핸들 */
    QSplitter::handle {{
        background-color: {COLOR_BORDER};
        height: 2px;
        width: 2px;
    }}
    """
'''

# 4. core/mock_api.py
mock_api_py = r"""import random
import datetime
import uuid

class MockApiService:
    @staticmethod
    def get_log_data(count=30):
        data = []
        apps = ["Application", "System", "Network", "Database"]
        services = ["ServiceMsme", "AuthService", "DataSync", "PaymentGateway"]
        operations = ["Runtime Layout", "Login", "Data Fetch", "Transaction", "Health Check"]
        
        current_time = datetime.datetime.now()

        for _ in range(count):
            is_error = random.choice([True, False, False, False]) # 25% 확률로 에러
            
            log_item = {
                "timestamp": (current_time - datetime.timedelta(minutes=random.randint(1, 1000))).strftime("%Y-%m-%d %H:%M:%S"),
                "guid": str(uuid.uuid4()),
                "user_ip": f"192.168.1.{random.randint(100, 200)}",
                "error": is_error,
                "application": random.choice(apps),
                "service": random.choice(services),
                "operation": random.choice(operations),
                "raw_input": '{\n  "guid": "...",\n  "action": "REQ",\n  "payload": "encrypted_data_packet"\n}',
                "raw_output": '{\n  "status": "200",\n  "message": "success"\n}' if not is_error else '{\n  "status": "500",\n  "error": "Critical Exception: NullPointer"\n}',
                "detail_log": (
                    f"[INFO] Transaction started by user.\n"
                    f"[DEBUG] Validating session token...\n"
                    f"{'[ERROR] Connection timeout to DB instance #3.' if is_error else '[INFO] Data successfully committed.'}\n"
                    f"[INFO] Process finished in {random.randint(10, 500)}ms."
                )
            }
            data.append(log_item)
            
        data.sort(key=lambda x: x['timestamp'], reverse=True)
        return data
"""

# 5. ui/widgets/custom_widgets.py
custom_widgets_py = r"""from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel

class Panel(QFrame):
    def __init__(self, title, content_widget, parent=None):
        super().__init__(parent)
        self.init_ui(title, content_widget)

    def init_ui(self, title, content_widget):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 패널 헤더
        lbl_title = QLabel(f"  {title}")
        lbl_title.setStyleSheet("background-color: #313244; color: #a6adc8; font-weight: bold; padding: 6px;")
        lbl_title.setFixedHeight(30)
        
        layout.addWidget(lbl_title)
        layout.addWidget(content_widget)
"""

# 6. ui/main_window.py
main_window_py = r"""from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QTextEdit, QLabel, QFrame, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from config.settings import APP_TITLE
from utils.styles import AppStyle
from core.mock_api import MockApiService
from ui.widgets.custom_widgets import Panel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1400, 850)
        
        # 스타일 적용
        self.setStyleSheet(AppStyle.DARK_THEME)
        
        self.api_service = MockApiService()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. 상단 헤더
        main_layout.addWidget(self.create_header())

        # 2. 메인 컨텐츠 (스플리터)
        # 전체 구조: [왼쪽: 테이블 + 상세 JSON] <-> [오른쪽: 로그 텍스트]
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 2-1. 왼쪽 영역 (테이블 / JSON 상세)
        left_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 로그 테이블
        self.table = self.create_table()
        left_splitter.addWidget(Panel("System Logs", self.table))
        
        # 상세 정보 (JSON View)
        detail_container = QWidget()
        detail_layout = QHBoxLayout(detail_container)
        detail_layout.setContentsMargins(0,5,0,0)
        
        self.txt_input = QTextEdit()
        self.txt_output = QTextEdit()
        # 폰트 설정
        mono_style = "font-family: Consolas, monospace; font-size: 11px;"
        self.txt_input.setStyleSheet(mono_style)
        self.txt_output.setStyleSheet(mono_style)

        detail_layout.addWidget(Panel("Input (RAW)", self.txt_input))
        detail_layout.addWidget(Panel("Output (RAW)", self.txt_output))
        
        left_splitter.addWidget(detail_container)
        left_splitter.setStretchFactor(0, 6) # 테이블 영역 비율
        left_splitter.setStretchFactor(1, 4) # 상세 영역 비율

        # 2-2. 오른쪽 영역 (로그 텍스트)
        self.txt_full_log = QTextEdit()
        self.txt_full_log.setReadOnly(True)
        self.txt_full_log.setStyleSheet("font-family: Consolas, monospace; line-height: 140%;")
        
        self.main_splitter.addWidget(left_splitter)
        self.main_splitter.addWidget(Panel("Detailed Log View", self.txt_full_log))
        
        self.main_splitter.setStretchFactor(0, 7)
        self.main_splitter.setStretchFactor(1, 3)

        main_layout.addWidget(self.main_splitter)
        self.setCentralWidget(main_widget)

    def create_header(self):
        container = QFrame()
        container.setFixedHeight(50)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 로고/타이틀
        title = QLabel(APP_TITLE)
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {AppStyle.COLOR_ACCENT};")
        
        # 검색바 (데모용)
        search_box = QLineEdit()
        search_box.setPlaceholderText("GUID, IP, or Service name...")
        search_box.setFixedWidth(300)
        
        btn_search = QPushButton("🔍 Search")
        btn_search.setObjectName("primary")
        btn_search.clicked.connect(self.load_data)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(QLabel("Start: 2025-11-28 09:00"))
        layout.addWidget(QLabel(" ~ "))
        layout.addWidget(QLabel("End: 2025-11-28 18:00"))
        layout.addSpacing(20)
        layout.addWidget(search_box)
        layout.addWidget(btn_search)
        
        return container

    def create_table(self):
        table = QTableWidget()
        columns = ["Timestamp", "GUID", "User IP", "Error", "Application", "Service", "Operation"]
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.itemClicked.connect(self.on_row_clicked)
        return table

    def load_data(self):
        self.data_list = self.api_service.get_log_data()
        self.table.setRowCount(0)
        
        for row_idx, item in enumerate(self.data_list):
            self.table.insertRow(row_idx)
            
            # 데이터 매핑
            mapping = [item['timestamp'], item['guid'], item['user_ip'], "", item['application'], item['service'], item['operation']]
            
            for col_idx, val in enumerate(mapping):
                if col_idx == 3: # Error Column
                    status_text = "FAIL" if item['error'] else "OK"
                    cell = QTableWidgetItem(status_text)
                    cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    # 상태에 따른 색상 처리
                    if item['error']:
                        cell.setForeground(QColor(AppStyle.COLOR_ERROR))
                    else:
                        cell.setForeground(QColor(AppStyle.COLOR_SUCCESS))
                    self.table.setItem(row_idx, col_idx, cell)
                else:
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(val))

    def on_row_clicked(self, item):
        row = item.row()
        data = self.data_list[row]
        
        self.txt_input.setText(data['raw_input'])
        self.txt_output.setText(data['raw_output'])
        self.txt_full_log.setText(data['detail_log'])
"""

# 7. main.py
main_py = r"""import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 윈도우 스타일 퓨전으로 설정 (기본보다 깔끔함)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
"""

# ==========================================
# 2. 프로젝트 업데이트 실행
# ==========================================
def update_current_project():
    base_dir = "."
    
    structure = {
        "requirements.txt": requirements_txt,
        "main.py": main_py,
        "config/settings.py": settings_py,
        "core/mock_api.py": mock_api_py,
        "ui/main_window.py": main_window_py,
        "ui/widgets/custom_widgets.py": custom_widgets_py,
        "utils/styles.py": styles_py,
        # 필요한 __init__.py 파일들 생성
        "config/__init__.py": "",
        "core/__init__.py": "",
        "ui/__init__.py": "",
        "ui/widgets/__init__.py": "",
        "utils/__init__.py": "",
    }

    print(f"🚀 현재 폴더({os.getcwd()})에 파일 업데이트 시작...")

    for path, content in structure.items():
        full_path = os.path.join(base_dir, path)
        dir_name = os.path.dirname(full_path)
        
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        # 파일 쓰기 (덮어쓰기 모드)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 업데이트/생성됨: {path}")

    print("\n🎉 프로젝트 업데이트가 완료되었습니다!")
    print("------------------------------------------")
    print("1. 필요한 라이브러리 설치:")
    print("   pip install -r requirements.txt")
    print("\n2. 프로그램 실행:")
    print("   python main.py")
    print("------------------------------------------")

if __name__ == "__main__":
    update_current_project()