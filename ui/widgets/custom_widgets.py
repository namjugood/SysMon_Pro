from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QToolButton, QWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPainter

class Panel(QFrame):
    """기본 패널 (헤더 + 컨텐츠)"""
    def __init__(self, title, content_widget, parent=None):
        super().__init__(parent)
        self.init_ui(title, content_widget)

    def init_ui(self, title, content_widget):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        header_frame = QFrame()
        header_frame.setObjectName("panel_header")
        header_frame.setFixedHeight(35)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 0, 0, 0)
        
        lbl_title = QLabel(title)
        lbl_title.setObjectName("panel_title")
        
        header_layout.addWidget(lbl_title)
        
        layout.addWidget(header_frame)
        layout.addWidget(content_widget)

class CollapsiblePanel(QWidget):
    """접이식 패널"""
    HEADER_HEIGHT = 46 

    def __init__(self, title, content_widget, parent=None):
        super().__init__(parent)
        self.setObjectName("transparent_container") 
        
        self.is_collapsed = False
        self.content_widget = content_widget
        self.init_ui(title)

    def init_ui(self, title):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.header = QFrame()
        self.header.setObjectName("panel_header")
        self.header.setFixedHeight(self.HEADER_HEIGHT)
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 0, 10, 0)

        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("panel_title")
        
        self.btn_toggle = QToolButton()
        self.btn_toggle.setText("▼") 
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setFixedWidth(40)
        self.btn_toggle.clicked.connect(self.toggle_content)

        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_toggle)

        self.content_wrapper = QWidget()
        wrapper_layout = QVBoxLayout(self.content_wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(self.content_widget)

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.content_wrapper)
        
        self.setMinimumHeight(self.HEADER_HEIGHT)

    def toggle_content(self):
        self.is_collapsed = not self.is_collapsed
        
        if self.is_collapsed:
            self.content_wrapper.setVisible(False)
            self.btn_toggle.setText("▲")
            self.setFixedHeight(self.HEADER_HEIGHT)
        else:
            self.content_wrapper.setVisible(True)
            self.btn_toggle.setText("▼")
            self.setMinimumHeight(self.HEADER_HEIGHT)
            self.setMaximumHeight(16777215)

class LoadingOverlay(QWidget):
    """화면을 덮는 반투명 로딩 오버레이 (최상위 창 모드)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # [핵심] 부모 창에 종속되지 않고 독립적인 최상위 창으로 설정
        # Frameless: 테두리 없음 / Tool: 작업표시줄 안 뜸 / WindowStaysOnTopHint: 항상 위
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_msg = QLabel("Processing...")
        self.lbl_msg.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-weight: bold;
                font-size: 24px;
                background-color: transparent;
                border: none;
            }
        """)
        layout.addWidget(self.lbl_msg)

    def paintEvent(self, event):
        """반투명 검은색 배경 그리기"""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 180)) # 조금 더 진하게 (180)

    def show_loading(self, msg="Loading..."):
        self.lbl_msg.setText(msg)
        
        # 부모(메인윈도우)의 위치와 크기를 그대로 따라감
        if self.parent():
            geo = self.parent().geometry() # 화면상 절대 좌표 및 크기
            self.setGeometry(geo)
            
        self.show()
        self.raise_() # 최상단 보장

    def hide_loading(self):
        self.hide()