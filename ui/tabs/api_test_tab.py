from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                             QLabel, QPushButton, QLineEdit, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from datetime import datetime
import json

from config.settings import APP_TITLE, LOGIN_URL
# utils나 core는 경로에 맞춰 임포트
from utils.styles import AppStyle

class ApiTestTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window # 메인 윈도우 참조 (쿠키, 로그 등 접근용)
        self.api_service = main_window.api_service
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 1. URL 및 전송 바
        url_bar = QWidget()
        url_bar.setObjectName("transparent_container")
        url_layout = QHBoxLayout(url_bar)
        url_layout.setContentsMargins(0, 0, 0, 0)

        self.edt_test_url = QLineEdit()
        self.edt_test_url.setPlaceholderText("Target API URL (e.g. https://.../bxmAdmin/json)")
        
        # 메인 윈도우에 저장된 URL이 있으면 가져오기
        if self.main_window.current_base_url:
            self.edt_test_url.setText(f"{self.main_window.current_base_url.rstrip('/')}/bxmAdmin/json")

        btn_template = QPushButton("Template")
        btn_template.setToolTip("Insert BXM default payload")
        btn_template.clicked.connect(self.set_api_template)

        btn_send = QPushButton("Send Request")
        btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_send.clicked.connect(self.execute_api_test)

        url_layout.addWidget(QLabel("URL:"))
        url_layout.addWidget(self.edt_test_url)
        url_layout.addWidget(btn_template)
        url_layout.addWidget(btn_send)

        layout.addWidget(url_bar)

        # 2. Payload / Response (Splitter)
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Payload 영역
        payload_widget = QWidget()
        payload_layout = QVBoxLayout(payload_widget)
        payload_layout.setContentsMargins(0,0,0,0)
        
        self.txt_test_payload = QTextEdit()
        self.txt_test_payload.setPlaceholderText("Enter JSON Payload here...")
        self.txt_test_payload.setStyleSheet("font-family: Consolas; font-size: 12px;")
        
        payload_layout.addWidget(QLabel("Request Payload (JSON):"))
        payload_layout.addWidget(self.txt_test_payload)
        
        # Response 영역
        response_widget = QWidget()
        response_layout = QVBoxLayout(response_widget)
        response_layout.setContentsMargins(0,0,0,0)

        self.txt_test_response = QTextEdit()
        self.txt_test_response.setReadOnly(True)
        self.txt_test_response.setStyleSheet("font-family: Consolas; font-size: 12px; background-color: #11111b;")

        response_layout.addWidget(QLabel("Response Data:"))
        response_layout.addWidget(self.txt_test_response)

        splitter.addWidget(payload_widget)
        splitter.addWidget(response_widget)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 6)

        layout.addWidget(splitter)

    def set_api_template(self):
        """BXM 기본 페이로드 템플릿 입력"""
        template = {
            "header": {
                "application": "bxmAdmin",
                "service": "OnlineLogService",
                "operation": "getServiceLogList",
                "langCd": "ko"
            },
            "OnlineLogSearchConditionOMM": {
                "pageCount": "100",
                "pageNum": "1",
                "opOccurDttmStart": datetime.now().strftime("%Y-%m-%d 00:00"),
                "opOccurDttmEnd": datetime.now().strftime("%Y-%m-%d 23:59")
            }
        }
        self.txt_test_payload.setText(json.dumps(template, indent=4, ensure_ascii=False))

    def execute_api_test(self):
        """API 테스트 실행"""
        url = self.edt_test_url.text().strip()
        payload = self.txt_test_payload.toPlainText().strip()

        if not url:
            QMessageBox.warning(self, "Error", "URL is empty.")
            return
        
        # 메인 윈도우의 쿠키 사용
        cookies = self.main_window.cookies
        if not cookies:
            QMessageBox.warning(self, "Auth Error", "Please login first to get session cookies.")
            return

        # 메인 윈도우의 로그 함수 사용
        self.main_window.log_debug(f"Test API -> {url}")
        self.txt_test_response.setText("Sending request...")
        
        # API 호출
        success, response_text = self.api_service.send_raw_request(url, cookies, payload)
        
        self.txt_test_response.setText(response_text)
        if success:
            self.main_window.log_debug("API Test Success.")
        else:
            self.main_window.log_debug("API Test Failed.")