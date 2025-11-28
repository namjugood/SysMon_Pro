from PyQt6.QtGui import QColor

class AppStyle:
    # ---------------------------------------------------------
    # 1. 색상 상수
    # ---------------------------------------------------------
    COLOR_BG_MAIN = "#1e1e2e"
    COLOR_BG_PANEL = "#262638"
    COLOR_BORDER = "#383850"
    COLOR_TEXT = "#cdd6f4"
    COLOR_HEADER = "#313244"
    COLOR_ACCENT = "#89b4fa"
    COLOR_ERROR = "#f38ba8"
    COLOR_SUCCESS = "#a6e3a1"
    
    HIGHLIGHT_ERROR_BG = QColor(200, 30, 30, 80)
    HIGHLIGHT_SEARCH_TEXT = QColor("#FFFF00")
    HIGHLIGHT_FOCUS_BG = QColor("#FFFF00")
    HIGHLIGHT_FOCUS_TEXT = QColor("#000000")

    # ---------------------------------------------------------
    # 2. QSS 스타일시트
    # ---------------------------------------------------------
    DARK_THEME = f"""
    /* [Global] */
    QWidget {{
        background-color: {COLOR_BG_MAIN};
        color: {COLOR_TEXT};
        font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
        font-size: 13px;
    }}

    /* [Containers] */
    QFrame, QTableWidget, QTextEdit, QTabWidget::pane {{
        background-color: {COLOR_BG_PANEL};
        border: 1px solid {COLOR_BORDER};
        border-radius: 6px;
    }}

    /* [Header] */
    QFrame#panel_header {{
        background-color: {COLOR_HEADER};
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        border-bottom: 1px solid {COLOR_BORDER};
        border-left: none;
        border-right: none;
        border-top: none;
    }}
    QLabel#panel_title {{
        color: #cdd6f4;
        font-weight: bold;
        background: transparent;
        border: none;
    }}

    /* [Transparent] */
    QWidget#transparent_container {{
        background-color: transparent;
        border: none;
    }}
    QWidget#transparent_container > QLabel {{
        background-color: transparent;
        border: none;
        font-weight: bold;
        color: #a6adc8;
    }}

    /* [Buttons] */
    QPushButton, QToolButton {{
        background-color: #45475a;
        color: #ffffff;
        border: 1px solid #585b70;
        border-radius: 4px;
        font-weight: bold;
        padding: 0px 10px;
        min-height: 32px;
        max-height: 32px;
        font-size: 12px;
    }}
    QPushButton:hover, QToolButton:hover {{
        background-color: #585b70;
        border-color: #7f849c;
    }}
    QPushButton:pressed, QToolButton:pressed {{
        background-color: #313244;
        border-color: {COLOR_ACCENT};
    }}
    QPushButton:disabled, QToolButton:disabled {{
        background-color: #313244;
        color: #6c7086;
        border: 1px solid #45475a;
    }}

    /* [Inputs & ComboBox] */
    QLineEdit, QDateEdit, QComboBox {{
        background-color: #181825;
        border: 1px solid {COLOR_BORDER};
        padding: 0px 8px;
        color: {COLOR_TEXT};
        border-radius: 4px;
        min-height: 32px;
        max-height: 32px;
    }}
    QLineEdit:focus, QDateEdit:focus, QComboBox:focus {{
        border: 1px solid {COLOR_ACCENT};
    }}
    
    /* 콤보박스 드롭다운 스타일 */
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox::down-arrow {{
        width: 0; 
        height: 0; 
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #a6adc8;
        margin-right: 5px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLOR_BG_PANEL};
        border: 1px solid {COLOR_BORDER};
        selection-background-color: #585b70;
        color: {COLOR_TEXT};
    }}

    /* 특정 입력 필드 강조 */
    QLineEdit#input_highlight {{
        color: {COLOR_ACCENT};
        font-weight: bold;
    }}

    /* [TextEdit] */
    QTextEdit {{
        selection-background-color: #FFFF00;
        selection-color: #000000;
        line-height: 140%;
        font-family: Consolas, monospace;
        border: none;
    }}
    QTextEdit#detail_log_box {{
        background-color: #11111b;
        border: 1px solid {COLOR_BORDER};
        font-family: Consolas;
        font-size: 11px;
    }}

    /* [Table] */
    QTableWidget {{
        gridline-color: {COLOR_BORDER};
        selection-background-color: #45475a;
        selection-color: #ffffff;
        outline: none;
    }}
    QHeaderView::section {{
        background-color: {COLOR_HEADER};
        color: #a6adc8;
        padding: 4px;
        border: none;
        font-weight: bold;
        border-bottom: 1px solid {COLOR_BORDER};
        height: 32px;
    }}
    QTableCornerButton::section {{
        background-color: {COLOR_HEADER};
        border: none;
    }}

    /* [Tab] */
    QTabWidget::pane {{
        border: 1px solid {COLOR_BORDER};
        background: {COLOR_BG_MAIN};
    }}
    QTabBar::tab {{
        background: {COLOR_BG_PANEL};
        color: #a6adc8;
        padding: 8px 20px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        margin-right: 2px;
        font-weight: bold;
    }}
    QTabBar::tab:selected {{
        background: {COLOR_HEADER};
        color: {COLOR_TEXT};
        border-bottom: 2px solid {COLOR_ACCENT};
    }}

    /* [Labels] */
    QLabel#login_error_msg {{
        color: {COLOR_ERROR};
        font-size: 14px;
        padding: 20px;
        background: {COLOR_BG_MAIN};
    }}
    QLabel#user_offline {{ color: #6c7086; font-weight: bold; }}
    QLabel#user_online {{ color: {COLOR_SUCCESS}; font-weight: bold; }}
    QLabel#app_title {{ font-size: 18px; font-weight: bold; color: {COLOR_ACCENT}; }}

    /* [Scrollbar] */
    QScrollBar:vertical {{
        background: {COLOR_BG_MAIN};
        width: 12px;
        margin: 0px;
    }}
    QScrollBar::handle:vertical {{
        background: #585b70;
        min-height: 20px;
        border-radius: 6px;
        margin: 2px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    
    QSplitter::handle {{ background-color: {COLOR_BORDER}; }}
    """