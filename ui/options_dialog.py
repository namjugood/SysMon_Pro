from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHeaderView, QLineEdit, 
                             QMessageBox, QWidget)
from PyQt6.QtCore import Qt
from utils.styles import AppStyle
from utils.config_manager import ConfigManager

class OptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("Login Page Options")
        self.resize(800, 400) # 너비 확장 (컬럼 추가됨)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 1. 입력 폼 (페이지명, URL, ID, PW, 추가 버튼)
        form_layout = QHBoxLayout()
        
        self.edt_name = QLineEdit()
        self.edt_name.setPlaceholderText("Name")
        self.edt_name.setFixedWidth(100)
        
        self.edt_url = QLineEdit()
        self.edt_url.setPlaceholderText("URL (https://...)")
        
        # [신규] ID/PW 입력 필드
        self.edt_id = QLineEdit()
        self.edt_id.setPlaceholderText("ID")
        self.edt_id.setFixedWidth(100)

        self.edt_pw = QLineEdit()
        self.edt_pw.setPlaceholderText("Password")
        self.edt_pw.setFixedWidth(100)
        self.edt_pw.setEchoMode(QLineEdit.EchoMode.Password) # 비밀번호 가림
        
        btn_add = QPushButton("Add")
        btn_add.setFixedWidth(60)
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self.add_row)
        
        form_layout.addWidget(self.edt_name)
        form_layout.addWidget(self.edt_url)
        form_layout.addWidget(self.edt_id)
        form_layout.addWidget(self.edt_pw)
        form_layout.addWidget(btn_add)
        
        layout.addLayout(form_layout)

        # 2. 테이블 (목록 표시)
        self.table = QTableWidget()
        # 컬럼 5개로 증가 (Name, URL, ID, PW, Action)
        self.table.setColumnCount(5) 
        self.table.setHorizontalHeaderLabels(["Name", "URL", "ID", "Password", "Action"])
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 70)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)

        # 3. 하단 저장 버튼
        btn_save = QPushButton("Save & Apply")
        btn_save.setFixedHeight(40)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self.save_options)
        btn_save.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyle.COLOR_ACCENT};
                color: #1e1e2e;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: #b4befe; }}
        """)
        
        layout.addWidget(btn_save)

    def load_data(self):
        """저장된 데이터 불러와서 테이블에 표시"""
        data = ConfigManager.load_urls()
        self.table.setRowCount(0)
        for item in data:
            self.insert_table_row(
                item.get('name', ''), 
                item.get('url', ''),
                item.get('id', ''),      # ID 로드
                item.get('password', '') # PW 로드
            )

    def add_row(self):
        """UI에서 행 추가"""
        name = self.edt_name.text().strip()
        url = self.edt_url.text().strip()
        user_id = self.edt_id.text().strip()
        password = self.edt_pw.text().strip()
        
        if not name or not url:
            QMessageBox.warning(self, "Input Error", "Page Name and URL are required.")
            return
            
        self.insert_table_row(name, url, user_id, password)
        
        # 입력창 초기화
        self.edt_name.clear()
        self.edt_url.clear()
        self.edt_id.clear()
        self.edt_pw.clear()

    def insert_table_row(self, name, url, user_id, password):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(url))
        self.table.setItem(row, 2, QTableWidgetItem(user_id))
        self.table.setItem(row, 3, QTableWidgetItem(password)) # 실제 비밀번호 텍스트 (보이게 할지 선택 가능)
        
        # 삭제 버튼
        btn_del = QPushButton("Delete")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.setStyleSheet(f"color: {AppStyle.COLOR_ERROR}; border: 1px solid {AppStyle.COLOR_ERROR};")
        # 클로저 문제 방지를 위해 indexAt 사용
        btn_del.clicked.connect(lambda: self.delete_row_at(btn_del))
        
        self.table.setCellWidget(row, 4, btn_del)

    def delete_row_at(self, widget):
        """버튼 위치를 기반으로 행 삭제"""
        pos = widget.pos()
        index = self.table.indexAt(pos)
        if index.isValid():
            self.table.removeRow(index.row())

    def save_options(self):
        """데이터 저장 및 메인 윈도우 갱신"""
        data = []
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text()
            url = self.table.item(row, 1).text()
            user_id = self.table.item(row, 2).text()
            password = self.table.item(row, 3).text()
            
            data.append({
                "name": name, 
                "url": url,
                "id": user_id,
                "password": password
            })
            
        ConfigManager.save_urls(data)
        
        if self.parent_window and hasattr(self.parent_window, 'refresh_login_buttons'):
            self.parent_window.refresh_login_buttons()
            
        QMessageBox.information(self, "Saved", "Options saved successfully!")
        self.accept()