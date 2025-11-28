import random
import datetime
import uuid

class MockApiService:
    @staticmethod
    def get_log_data(count=30):
        data = []
        apps = ["Application", "System", "Network", "Database"]
        services = ["ServiceMsme", "AuthService", "DataSync", "PaymentGateway"]
        operations = ["Runtime Layout", "Login", "Data Fetch", "Transaction", "Health Check"]
        
        current_time = datetime.datetime.now()

        for _ in range(count):
            is_error = random.choice([True, False, False, False]) # 25% 확률로 에러
            
            log_item = {
                "timestamp": (current_time - datetime.timedelta(minutes=random.randint(1, 1000))).strftime("%Y-%m-%d %H:%M:%S"),
                "guid": str(uuid.uuid4()),
                "user_ip": f"192.168.1.{random.randint(100, 200)}",
                "error": is_error,
                "application": random.choice(apps),
                "service": random.choice(services),
                "operation": random.choice(operations),
                "raw_input": '{\n  "guid": "...",\n  "action": "REQ",\n  "payload": "encrypted_data_packet"\n}',
                "raw_output": '{\n  "status": "200",\n  "message": "success"\n}' if not is_error else '{\n  "status": "500",\n  "error": "Critical Exception: NullPointer"\n}',
                "detail_log": (
                    f"[INFO] Transaction started by user.\n"
                    f"[DEBUG] Validating session token...\n"
                    f"{'[ERROR] Connection timeout to DB instance #3.' if is_error else '[INFO] Data successfully committed.'}\n"
                    f"[INFO] Process finished in {random.randint(10, 500)}ms."
                )
            }
            data.append(log_item)
            
        data.sort(key=lambda x: x['timestamp'], reverse=True)
        return data
