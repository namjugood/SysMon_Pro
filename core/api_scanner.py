import requests
from PyQt6.QtCore import QThread, pyqtSignal
from config.settings import TARGET_APIS, DEFAULT_HEADERS
from utils.logger import get_logger

log = get_logger("ApiScanner")

class ApiScannerThread(QThread):
    result_signal = pyqtSignal(str, str, int, str)
    finished_signal = pyqtSignal()

    def __init__(self, cookies):
        super().__init__()
        self.cookies = cookies

    def run(self):
        log.info("API 스캔 시작")
        session = requests.Session()
        session.headers.update(DEFAULT_HEADERS)
        
        for k, v in self.cookies.items():
            session.cookies.set(k, v)

        for api in TARGET_APIS:
            name = api['name']
            url = api['url']
            
            try:
                res = session.get(url, timeout=10)
                code = res.status_code
                status = "성공" if 200 <= code < 300 else "실패"
                
                log.debug(f"[{status}] {name} ({code})")
                self.result_signal.emit(name, url, code, status)
                
            except Exception as e:
                log.error(f"Error on {name}: {e}")
                self.result_signal.emit(name, url, 0, f"에러: {str(e)}")
        
        log.info("API 스캔 종료")
        self.finished_signal.emit()
