import os
import sys

def check_project_structure():
    current_dir = os.getcwd()
    print(f"📂 현재 작업 디렉토리: {current_dir}")
    print(f"🐍 Python 실행 경로 (sys.path): {sys.path[0]}")
    print("-" * 40)

    # 1. core 폴더 확인
    core_path = os.path.join(current_dir, "core")
    if not os.path.exists(core_path):
        print("❌ [Error] 'core' 폴더를 찾을 수 없습니다.")
        return

    # 2. 파일 존재 확인
    files = os.listdir(core_path)
    print(f"📄 'core' 폴더 내 파일 목록: {files}")

    target_file = "api_service.py"
    if target_file in files:
        print(f"✅ '{target_file}' 파일이 존재합니다.")
    else:
        print(f"❌ [Error] '{target_file}' 파일이 없습니다! (파일명 오타 확인 필요)")
        # 혹시 모를 유사 파일명 추천
        for f in files:
            if "api" in f and f.endswith(".py"):
                print(f"   -> 혹시 '{f}' 파일을 의도하셨나요?")

    # 3. __init__.py 확인
    if "__init__.py" not in files:
        print("⚠️ [Warning] 'core/__init__.py' 파일이 없습니다. (패키지 인식 실패 가능성)")
        try:
            with open(os.path.join(core_path, "__init__.py"), "w") as f:
                pass
            print("   -> 🔧 빈 '__init__.py' 파일을 자동으로 생성했습니다.")
        except Exception as e:
            print(f"   -> 생성 실패: {e}")
    else:
        print("✅ 'core/__init__.py' 파일이 존재합니다.")

    print("-" * 40)

    # 4. 임포트 테스트
    print("🚀 모듈 임포트 테스트 중...")
    try:
        from core.api_service import ApiService
        print("✅ 성공! 'core.api_service' 모듈을 정상적으로 불러왔습니다.")
    except ImportError as e:
        print(f"❌ [ImportError] 임포트 실패: {e}")
    except Exception as e:
        print(f"❌ [Error] 기타 오류: {e}")

if __name__ == "__main__":
    check_project_structure()