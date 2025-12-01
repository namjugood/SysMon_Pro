from PyQt6.QtWidgets import QMenuBar, QMessageBox
from PyQt6.QtGui import QAction
from ui.options_dialog import OptionsDialog  # [신규]

class AppMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        # 1. File Menu
        file_menu = self.addMenu('&File')
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.parent_window.close)
        file_menu.addAction(exit_action)

        # 2. View Menu
        view_menu = self.addMenu('&View')
        
        refresh_action = QAction('Refresh Data', self)
        refresh_action.setShortcut('F5')
        if self.parent_window and hasattr(self.parent_window, 'load_data'):
            refresh_action.triggered.connect(self.parent_window.load_data)
        view_menu.addAction(refresh_action)

        # 3. [신규] Tools Menu (Options)
        tools_menu = self.addMenu('&Tools')
        
        options_action = QAction('Options', self)
        options_action.setShortcut('Ctrl+O')
        options_action.triggered.connect(self.open_options)
        tools_menu.addAction(options_action)

        # 4. Help Menu
        help_menu = self.addMenu('&Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def open_options(self):
        """옵션 팝업 열기"""
        if self.parent_window:
            dlg = OptionsDialog(self.parent_window)
            dlg.exec()

    def show_about_dialog(self):
        QMessageBox.about(self, "About SysMon Pro", 
                          "SysMon Pro v2.0\n\nSystem Monitoring Dashboard\nDeveloped with PyQt6")