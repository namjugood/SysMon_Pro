from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QTextEdit, QLabel, QFrame, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                             QTabWidget, QDateEdit, QGridLayout, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QColor, QTextDocument, QTextCursor, QTextCharFormat, QFont
from datetime import datetime

from config.settings import APP_TITLE, LOGIN_URL
from utils.styles import AppStyle
from core.mock_api import MockApiService
from ui.widgets.custom_widgets import Panel, CollapsiblePanel
from ui.login_dialog import LoginDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(1600, 950)
        self.setStyleSheet(AppStyle.DARK_THEME)
        
        self.cookies = {} 
        self.api_service = MockApiService()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        main_layout.addWidget(self.create_top_bar())

        self.tabs = QTabWidget()
        
        self.tab_system = QWidget()
        self.setup_system_log_tab(self.tab_system)
        self.tabs.addTab(self.tab_system, "시스템로그")

        self.tab_batch = QWidget()
        self.tabs.addTab(self.tab_batch, "배치로그")
        
        main_layout.addWidget(self.tabs)

    def create_top_bar(self):
        container = QFrame()
        container.setFixedHeight(60)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        title = QLabel("SysMon Pro")
        title.setObjectName("app_title")
        
        self.edt_url = QLineEdit()
        self.edt_url.setText(LOGIN_URL) 
        self.edt_url.setPlaceholderText("접속할 시스템의 URL을 입력하세요")
        
        btn_go = QPushButton("Connect / Login")
        btn_go.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_go.setFixedWidth(130)
        btn_go.clicked.connect(self.open_login_dialog)

        self.lbl_user_info = QLabel("Guest | Offline")
        self.lbl_user_info.setObjectName("user_offline")

        layout.addWidget(title)
        layout.addWidget(self.edt_url, 1)
        layout.addWidget(btn_go)
        layout.addWidget(self.lbl_user_info)
        
        return container

    def open_login_dialog(self):
        target_url = self.edt_url.text().strip()
        if not target_url:
            QMessageBox.warning(self, "URL 오류", "접속할 URL을 입력해주세요.")
            return

        dlg = LoginDialog(url=target_url, parent=self)
        if dlg.exec():
            self.cookies = dlg.get_cookies()
            if self.cookies:
                self.lbl_user_info.setText("Admin | ✅ Online")
                self.lbl_user_info.setObjectName("user_online")
                self.lbl_user_info.style().unpolish(self.lbl_user_info)
                self.lbl_user_info.style().polish(self.lbl_user_info)
                QMessageBox.information(self, "연동 성공", "세션이 성공적으로 확보되었습니다.")
            else:
                self.lbl_user_info.setText("Guest | ⚠️ Cookie Not Found")
                self.lbl_user_info.setObjectName("user_offline")

    def setup_system_log_tab(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(self.create_filter_bar())

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.left_splitter = QSplitter(Qt.Orientation.Vertical)
        
        self.table = self.create_table()
        self.left_splitter.addWidget(Panel("System Log List", self.table))
        
        self.detail_panel = self.create_detail_layer()
        self.detail_panel.hide()
        self.left_splitter.addWidget(self.detail_panel)
        
        self.left_splitter.setStretchFactor(0, 7)
        self.left_splitter.setStretchFactor(1, 3)

        log_view_panel = self.create_log_view_panel()
        
        self.main_splitter.addWidget(self.left_splitter)
        self.main_splitter.addWidget(log_view_panel)
        
        self.main_splitter.setStretchFactor(0, 6)
        self.main_splitter.setStretchFactor(1, 4)

        layout.addWidget(self.main_splitter)

    def create_log_view_panel(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.edt_log_search = QLineEdit()
        self.edt_log_search.setPlaceholderText("Find string in log...")
        self.edt_log_search.textChanged.connect(self.update_highlights)
        self.edt_log_search.returnPressed.connect(lambda: self.find_text_in_log(forward=True))
        
        btn_prev = QPushButton("Prev")
        btn_prev.setFixedWidth(60)
        btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_prev.clicked.connect(lambda: self.find_text_in_log(forward=False))

        btn_next = QPushButton("Next")
        btn_next.setFixedWidth(60)
        btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_next.clicked.connect(lambda: self.find_text_in_log(forward=True))

        search_layout.addWidget(self.edt_log_search)
        search_layout.addWidget(btn_prev)
        search_layout.addWidget(btn_next)

        self.txt_full_log = QTextEdit()
        self.txt_full_log.setReadOnly(True)

        layout.addLayout(search_layout)
        layout.addWidget(self.txt_full_log)

        return Panel("Detailed Log View", container)

    def update_highlights(self):
        extra_selections = []
        doc = self.txt_full_log.document()
        
        # 1. 에러 라인
        error_keywords = ["error", "fatal", "exception"]
        
        block = doc.begin()
        while block.isValid():
            text = block.text().lower()
            if any(k in text for k in error_keywords):
                selection = QTextEdit.ExtraSelection()
                cursor = QTextCursor(doc)
                cursor.setPosition(block.position())
                cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
                selection.cursor = cursor
                
                fmt = QTextCharFormat()
                fmt.setBackground(AppStyle.HIGHLIGHT_ERROR_BG) 
                fmt.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
                selection.format = fmt
                extra_selections.append(selection)
            block = block.next()

        # 2. 검색어
        search_text = self.edt_log_search.text()
        if search_text:
            cursor = QTextCursor(doc)
            while not cursor.isNull() and not cursor.atEnd():
                cursor = doc.find(search_text, cursor)
                if not cursor.isNull():
                    selection = QTextEdit.ExtraSelection()
                    selection.cursor = cursor
                    
                    fmt = QTextCharFormat()
                    fmt.setForeground(AppStyle.HIGHLIGHT_SEARCH_TEXT)
                    fmt.setFontWeight(QFont.Weight.Bold)
                    selection.format = fmt
                    extra_selections.append(selection)

        self.txt_full_log.setExtraSelections(extra_selections)

    def find_text_in_log(self, forward=True):
        search_text = self.edt_log_search.text()
        if not search_text:
            return

        flags = QTextDocument.FindFlag(0)
        if not forward:
            flags |= QTextDocument.FindFlag.FindBackward
        
        found = self.txt_full_log.find(search_text, flags)
        
        if not found:
            cursor = self.txt_full_log.textCursor()
            if forward:
                cursor.movePosition(QTextCursor.MoveOperation.Start)
            else:
                cursor.movePosition(QTextCursor.MoveOperation.End)
            self.txt_full_log.setTextCursor(cursor)
            
            if not self.txt_full_log.find(search_text, flags):
                QMessageBox.information(self, "검색 결과", f"'{search_text}'을(를) 찾을 수 없습니다.")
                return

    def create_filter_bar(self):
        container = QWidget()
        container.setObjectName("transparent_container") 
        container.setFixedHeight(50) 
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 5, 10, 5)
        
        lbl_period = QLabel("조회기간:")
        
        times = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]

        self.date_start = QDateEdit()
        self.date_start.setDate(QDate.currentDate())
        self.date_start.setCalendarPopup(True)
        self.date_start.setDisplayFormat("yyyy-MM-dd")
        self.date_start.setFixedWidth(110)

        self.time_start = QComboBox()
        self.time_start.addItems(times)
        self.time_start.setEditable(True)
        self.time_start.setFixedWidth(80)
        self.time_start.setCurrentText("00:00")
        
        lbl_tilde = QLabel("~")
        
        self.date_end = QDateEdit()
        self.date_end.setDate(QDate.currentDate())
        self.date_end.setCalendarPopup(True)
        self.date_end.setDisplayFormat("yyyy-MM-dd")
        self.date_end.setFixedWidth(110)

        self.time_end = QComboBox()
        self.time_end.addItems(times)
        self.time_end.setEditable(True)
        self.time_end.setFixedWidth(80)
        self.time_end.setCurrentText("23:30")

        layout.addWidget(lbl_period)
        layout.addWidget(self.date_start)
        layout.addWidget(self.time_start)
        layout.addWidget(lbl_tilde)
        layout.addWidget(self.date_end)
        layout.addWidget(self.time_end)
        
        layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("GUID, IP, Service...")
        self.search_input.setFixedWidth(250)
        self.search_input.returnPressed.connect(self.load_data)
        
        btn_search = QPushButton("Search")
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setFixedWidth(80)
        btn_search.clicked.connect(self.load_data)
        
        layout.addWidget(self.search_input)
        layout.addWidget(btn_search)
        
        return container

    def create_detail_layer(self):
        content = QWidget()
        content.setObjectName("transparent_container")
        layout = QGridLayout(content)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.edt_guid = QLineEdit()
        self.edt_guid.setReadOnly(True)
        self.edt_guid.setObjectName("input_highlight") 
        self.edt_guid.setAlignment(Qt.AlignmentFlag.AlignLeft) 
        
        self.edt_app = QLineEdit()
        self.edt_app.setReadOnly(True)
        
        self.edt_service = QLineEdit()
        self.edt_service.setReadOnly(True)
        
        self.edt_op = QLineEdit()
        self.edt_op.setReadOnly(True)

        layout.addWidget(QLabel("GUID"), 0, 0)
        layout.addWidget(self.edt_guid, 0, 1)
        layout.addWidget(QLabel("어플리케이션"), 0, 2)
        layout.addWidget(self.edt_app, 0, 3)

        layout.addWidget(QLabel("서비스"), 1, 0)
        layout.addWidget(self.edt_service, 1, 1)
        layout.addWidget(QLabel("오퍼레이션"), 1, 2)
        layout.addWidget(self.edt_op, 1, 3)

        layout.addWidget(QLabel("입력전문 (RAW)"), 2, 0, 1, 2)
        layout.addWidget(QLabel("출력전문 (RAW)"), 2, 2, 1, 2)

        self.txt_raw_in = QTextEdit()
        self.txt_raw_in.setReadOnly(True)
        self.txt_raw_in.setObjectName("detail_log_box") 
        
        self.txt_raw_out = QTextEdit()
        self.txt_raw_out.setReadOnly(True)
        self.txt_raw_out.setObjectName("detail_log_box")

        layout.addWidget(self.txt_raw_in, 3, 0, 1, 2)
        layout.addWidget(self.txt_raw_out, 3, 2, 1, 2)
        
        layout.setRowStretch(3, 1)

        return CollapsiblePanel("이미지 로그 상세", content)

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
        table.setSortingEnabled(True)
        return table

    def reset_details(self):
        """[신규] 상세 정보 필드 초기화 및 패널 숨김 (검색 시 호출)"""
        # 1. 상세 로그 텍스트 초기화
        self.txt_full_log.clear()
        
        # 2. 이미지 로그 상세 필드 초기화
        self.edt_guid.clear()
        self.edt_app.clear()
        self.edt_service.clear()
        self.edt_op.clear()
        self.txt_raw_in.clear()
        self.txt_raw_out.clear()
        
        # 3. 패널 숨기기
        self.detail_panel.hide()

    def load_data(self):
        # [수정] 검색 시작 시 상세 정보 초기화
        self.reset_details()
        
        self.table.setSortingEnabled(False)
        
        all_data = self.api_service.get_log_data(count=100)
        self.data_list = []
        
        search_query = self.search_input.text().lower().strip()
        
        str_start = f"{self.date_start.date().toString('yyyy-MM-dd')} {self.time_start.currentText()}:00"
        str_end = f"{self.date_end.date().toString('yyyy-MM-dd')} {self.time_end.currentText()}:59"
        
        try:
            dt_start = datetime.strptime(str_start, "%Y-%m-%d %H:%M:%S")
            dt_end = datetime.strptime(str_end, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt_start = datetime.min
            dt_end = datetime.max

        self.table.setRowCount(0)
        
        for item in all_data:
            try:
                item_dt = datetime.strptime(item['timestamp'], "%Y-%m-%d %H:%M:%S")
                if not (dt_start <= item_dt <= dt_end):
                    continue
            except:
                pass

            if search_query:
                values = [
                    item['guid'].lower(),
                    item['user_ip'],
                    item['application'].lower(),
                    item['service'].lower(),
                    item['operation'].lower()
                ]
                if not any(search_query in v for v in values):
                    continue

            self.data_list.append(item)
            
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            
            mapping = [item['timestamp'], item['guid'], item['user_ip'], "", item['application'], item['service'], item['operation']]
            
            for col_idx, val in enumerate(mapping):
                if col_idx == 3:
                    status_text = "FAIL" if item['error'] else "OK"
                    cell = QTableWidgetItem(status_text)
                    cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    cell.setForeground(QColor(AppStyle.COLOR_ERROR if item['error'] else AppStyle.COLOR_SUCCESS))
                    self.table.setItem(row_idx, col_idx, cell)
                else:
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(val))
        
        self.table.setSortingEnabled(True)

    def on_row_clicked(self, item):
        row = item.row()
        target_guid = self.table.item(row, 1).text()
        
        data = next((d for d in self.data_list if d['guid'] == target_guid), None)
        
        if data:
            if self.detail_panel.isHidden():
                self.detail_panel.show()

            self.edt_guid.setText(data['guid'])
            self.edt_app.setText(data['application'])
            self.edt_service.setText(data['service'])
            self.edt_op.setText(data['operation'])
            self.txt_raw_in.setText(data['raw_input'])
            self.txt_raw_out.setText(data['raw_output'])
            
            self.txt_full_log.setText(data['detail_log'])
            self.update_highlights()