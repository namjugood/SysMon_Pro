from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from utils.styles import AppStyle

class ApiLoginDialog(QDialog):
    # 로그인 요청 신호 (url, id, pw, domain)
    login_requested = pyqtSignal(str, str, str, str)

    def __init__(self, target_url, user_id="", password="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Login")
        self.resize(400, 250)
        
        self.target_url = target_url
        
        self.initial_user_id = user_id
        self.initial_password = password
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 타이틀
        lbl_info = QLabel(f"Login to: {self.target_url}")
        lbl_info.setStyleSheet("color: #89b4fa; font-weight: bold;")
        layout.addWidget(lbl_info)

        # ID 입력
        self.edt_id = QLineEdit()
        self.edt_id.setPlaceholderText("User ID")
        self.edt_id.setText(self.initial_user_id)
        layout.addWidget(self.edt_id)

        # PW 입력
        self.edt_pw = QLineEdit()
        self.edt_pw.setPlaceholderText("Password")
        self.edt_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.edt_pw.setText(self.initial_password)
        layout.addWidget(self.edt_pw)

        # Domain ID 입력
        self.edt_domain = QLineEdit()
        self.edt_domain.setPlaceholderText("Domain ID")
        self.edt_domain.setText("OKC")
        layout.addWidget(self.edt_domain)

        # 버튼 영역
        btn_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_login = QPushButton("Login")
        self.btn_login.setStyleSheet(f"background-color: {AppStyle.COLOR_ACCENT}; color: #1e1e2e;")
        self.btn_login.clicked.connect(self.on_login_click)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_login)
        
        layout.addLayout(btn_layout)

    def on_login_click(self):
        user_id = self.edt_id.text().strip()
        password = self.edt_pw.text().strip()
        domain_id = self.edt_domain.text().strip()

        if not user_id or not password:
            QMessageBox.warning(self, "Input Error", "Please enter ID and Password.")
            return

        # [중요] 창을 닫지 않고 메인 윈도우에 로그인 요청 신호 발송
        self.set_controls_enabled(False)
        self.login_requested.emit(self.target_url, user_id, password, domain_id)

    def set_controls_enabled(self, enabled):
        """로딩 중 입력 방지"""
        self.edt_id.setEnabled(enabled)
        self.edt_pw.setEnabled(enabled)
        self.edt_domain.setEnabled(enabled)
        self.btn_login.setEnabled(enabled)
        self.btn_cancel.setEnabled(enabled)

    def resizeEvent(self, event):
        """창 크기 변경 시 오버레이(자식 위젯)도 같이 크기 조절"""
        for child in self.children():
            # LoadingOverlay 클래스인지 확인 (문자열 체크로 순환참조 방지)
            if "LoadingOverlay" in str(type(child)):
                child.resize(self.size())
        super().resizeEvent(event)