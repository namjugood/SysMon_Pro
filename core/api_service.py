import requests
import json
from datetime import datetime

class ApiService:
    def __init__(self):
        self.timeout = 10 

    def login(self, base_url, user_id, password, domain_id="OKC"):
        """
        로그인 API 호출하여 세션 쿠키 획득
        URL: [BaseURL]/bxmAdmin/json/login
        """
        # URL 보정 (끝에 슬래시 제거 후 경로 추가)
        api_url = f"{base_url.rstrip('/')}/bxmAdmin/json/login"

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json"
        }

        # 이미지의 Request Payload 구조 반영
        payload = {
            "header": {
                "application": "bxmAdmin",
                "langCd": "ko",
                "service": "AuthorityService",
                "operation": "loginOperation"
            },
            "LoginOMM": {
                "userId": user_id,
                "userPwd": password,
                "lang": "ko",
                "domainId": domain_id
            }
        }

        try:
            # 세션 객체를 사용하여 요청 (쿠키 자동 관리)
            session = requests.Session()
            response = session.post(api_url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            res_json = response.json()
            
            # 응답 코드 확인 (ResponseCode가 100이거나 header.returnCode가 0이면 성공으로 간주)
            # 이미지상 ResponseCode: {code: 100} 이 성공으로 보임
            is_success = False
            
            if "ResponseCode" in res_json and res_json["ResponseCode"].get("code") == 100:
                is_success = True
            elif "header" in res_json and res_json["header"].get("returnCode") == "0":
                is_success = True

            if is_success:
                # 성공 시 세션의 쿠키(CookieJar) 반환
                return True, session.cookies, "Login Success"
            else:
                msg = res_json.get("header", {}).get("returnMessage", "Unknown Error")
                return False, None, msg

        except Exception as e:
            return False, None, str(e)

    def get_system_logs(self, base_url, cookies, start_dt, end_dt, search_keyword=""):
        """시스템 로그 조회 (기존 로직 유지)"""
        api_url = f"{base_url.rstrip('/')}/bxmAdmin/json"

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json"
        }

        payload = {
            "header": {
                "application": "bxmAdmin",
                "service": "OnlineLogService",
                "operation": "getServiceLogList",
                "langCd": "ko"
            },
            "OnlineLogSearchConditionOMM": {
                "opOccurDttmStart": start_dt,
                "opOccurDttmEnd": end_dt,
                "pageCount": "100",
                "pageNum": "1",
                "guid": search_keyword if search_keyword else "",
                "svcNm": "", 
                "opNm": "",
                "bxmAppId": "",
                "nodeName": "",
                "sendUserIp": ""
            }
        }

        try:
            response = requests.post(
                api_url, 
                headers=headers, 
                cookies=cookies, 
                json=payload, 
                timeout=self.timeout
            )
            response.raise_for_status()

            res_json = response.json()
            
            if "ServiceLogListOMM" in res_json and "serviceLogList" in res_json["ServiceLogListOMM"]:
                raw_list = res_json["ServiceLogListOMM"]["serviceLogList"]
                return self._parse_logs(raw_list)
            else:
                return []

        except Exception as e:
            print(f"API Request Failed: {e}")
            return []

    def _parse_logs(self, raw_list):
        parsed_data = []
        for item in raw_list:
            is_error = item.get("opErrYn", "N") == "Y"
            
            log_item = {
                "timestamp": item.get("opOccurDttm", ""),
                "guid": item.get("guid", ""),
                "user_ip": item.get("sendUserIp", ""),
                "error": is_error,
                "application": item.get("bxmAppId", ""),
                "service": item.get("svcNm", ""),
                "operation": item.get("opNm", ""),
                "raw_input": json.dumps(item, indent=2, ensure_ascii=False), 
                "raw_output": "Detail API required", 
                "detail_log": (
                    f"[INFO] Node: {item.get('nodeName', 'N/A')}\n"
                    f"[INFO] Elapsed: {item.get('opElapsedMills', 0)}ms\n"
                    f"[INFO] Message: {item.get('msgType', '')}\n"
                    f"{'[ERROR] Transaction Failed' if is_error else '[INFO] Transaction Success'}"
                )
            }
            parsed_data.append(log_item)
        return parsed_data