from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QUrl, Qt

# 웹 엔진 확인
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineProfile
    WEB_ENGINE_AVAILABLE = True
except ImportError:
    WEB_ENGINE_AVAILABLE = False

from config.settings import LOGIN_URL

class LoginDialog(QDialog):
    def __init__(self, url=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로그인 (Web Browser)")
        self.resize(1024, 768)
        self.cookies = {}
        self.target_url = url if url else LOGIN_URL
        
        # 다이얼로그도 다크 테마 적용을 위해 스타일시트가 필요할 수 있음
        # 하지만 main.py에서 QApplication에 적용했으므로 자동 상속됨.
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if not WEB_ENGINE_AVAILABLE:
            lbl_err = QLabel("⚠️ PyQt6-WebEngine이 설치되지 않았습니다.")
            lbl_err.setStyleSheet("color: #f38ba8; font-size: 14px; padding: 20px; background: #1e1e2e;")
            layout.addWidget(lbl_err)
            self.setLayout(layout)
            return

        self.webview = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        self.cookie_store = profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.on_cookie_added)
        
        if not self.target_url.startswith("http"):
            self.target_url = "https://" + self.target_url
        self.webview.setUrl(QUrl(self.target_url))
        
        layout.addWidget(self.webview)

        # 하단 버튼 영역
        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(10, 10, 10, 10)
        
        # [수정] 인라인 스타일 제거하여 전역 스타일 적용
        btn = QPushButton("로그인 완료 및 닫기 (세션 저장)")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(45) # 높이만 살짝 키움 (터치/클릭 용이성)
        
        btn.clicked.connect(self.accept)
        btn_layout.addWidget(btn)
        
        # 하단 바 배경색 맞춤
        bottom_frame = QDialog() # 더미 컨테이너 대신 스타일 상속
        # 여기서는 그냥 layout에 추가
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def on_cookie_added(self, cookie):
        name = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')
        self.cookies[name] = value

    def get_cookies(self):
        return self.cookies