from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QToolButton, QWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QSize

class Panel(QFrame):
    """기본 패널 (헤더 + 컨텐츠)"""
    def __init__(self, title, content_widget, parent=None):
        super().__init__(parent)
        self.init_ui(title, content_widget)

    def init_ui(self, title, content_widget):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 헤더 컨테이너 (스타일: styles.py -> #panel_header)
        header_frame = QFrame()
        header_frame.setObjectName("panel_header")
        header_frame.setFixedHeight(35)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 0, 0, 0)
        
        # 제목 라벨 (스타일: styles.py -> #panel_title)
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
        # 투명 컨테이너 설정 (스타일: styles.py -> #transparent_container)
        self.setObjectName("transparent_container") 
        
        self.is_collapsed = False
        self.content_widget = content_widget
        self.init_ui(title)

    def init_ui(self, title):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 헤더 (스타일: styles.py -> #panel_header)
        self.header = QFrame()
        self.header.setObjectName("panel_header")
        self.header.setFixedHeight(self.HEADER_HEIGHT)
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 0, 10, 0)

        # 제목 (스타일: styles.py -> #panel_title)
        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("panel_title")
        
        # 최소화 버튼 (스타일: styles.py -> QToolButton)
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