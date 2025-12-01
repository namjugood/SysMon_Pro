import PyInstaller.__main__
import os
import shutil
import sys
import subprocess

# 프로젝트 설정 파일에서 버전 정보 가져오기
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from config.settings import APP_VERSION

# 7z 압축 방법 결정
USE_PY7ZR = False
try:
    import py7zr
    USE_PY7ZR = True
except ImportError:
    pass

def find_7z_exe():
    """시스템에서 7z.exe 경로를 찾습니다."""
    # 1. PATH에 있는 경우
    if shutil.which("7z"):
        return "7z"
    
    # 2. 일반적인 설치 경로 확인
    paths = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe"
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def build_exe():
    app_name = "SysMonPro"
    version_tag = f"v{APP_VERSION}"  # 예: v2.0
    
    # 최종 결과물 이름 (예: SysMonPro_v2.0)
    final_name = f"{app_name}_{version_tag}"
    dist_path = "release"
    
    print(f"🚀 배포 파일 생성 시작 (버전: {version_tag})")

    # 1. 기존 빌드 폴더 정리
    if os.path.exists(dist_path):
        try:
            shutil.rmtree(dist_path)
            print(f" - 기존 '{dist_path}' 폴더 삭제 완료")
        except Exception as e:
            print(f" - [경고] 폴더 삭제 실패: {e}")

    # 2. PyInstaller 실행 (폴더 방식 --onedir 권장)
    options = [
        'main.py',
        f'--name={app_name}',               # 기본 이름으로 빌드 후 나중에 변경
        '--noconsole',
        '--onedir',                         # 폴더 방식 (권장)
        '--clean',
        f'--distpath={dist_path}',
        '--workpath=build/temp',
        '--specpath=build/spec',
        
        # 필수 라이브러리 포함
        '--hidden-import=PyQt6.QtWebEngineWidgets',
        '--hidden-import=PyQt6.QtWebEngineCore',
        '--collect-all=requests',
    ]

    try:
        print(" - PyInstaller 빌드 중...")
        PyInstaller.__main__.run(options)
        
        # 3. 폴더 이름 변경 (SysMonPro -> SysMonPro_v2.0)
        original_folder = os.path.join(dist_path, app_name)
        target_folder = os.path.join(dist_path, final_name)
        
        if os.path.exists(original_folder):
            if os.path.exists(target_folder):
                shutil.rmtree(target_folder)
            os.rename(original_folder, target_folder)
            print(f" - 폴더명 변경 완료: {target_folder}")
        
        # 4. .7z 압축 생성
        archive_name = os.path.join(dist_path, f"{final_name}.7z")
        print(f" - 압축 파일 생성 중 (.7z)...")
        
        success_compression = False
        
        if USE_PY7ZR:
            print("   [Info] py7zr 라이브러리를 사용합니다.")
            with py7zr.SevenZipFile(archive_name, 'w') as archive:
                archive.writeall(target_folder, arcname=final_name)
            success_compression = True
        else:
            # py7zr이 없으면 외부 명령어(7z.exe) 사용
            seven_zip_exe = find_7z_exe()
            if seven_zip_exe:
                print(f"   [Info] 외부 프로그램 사용: {seven_zip_exe}")
                # 7z a "archive.7z" "target_folder"
                cmd = [seven_zip_exe, "a", archive_name, target_folder]
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.returncode == 0:
                    success_compression = True
                else:
                    print(f"   [Error] 7-Zip 실행 실패:\n{result.stderr}")
            else:
                print("   [Warning] 'py7zr' 라이브러리가 없고 '7-Zip' 프로그램도 찾을 수 없습니다.")
                print("   -> .7z 파일을 생성하지 못했습니다.")
                print("   -> 해결법: 'pip install py7zr' 또는 7-Zip 프로그램 설치 (https://www.7-zip.org/)")

        if success_compression:
            print("\n🎉 빌드 및 패키징 성공!")
            print(f"   📂 폴더: {target_folder}")
            print(f"   📦 압축: {archive_name}")
        else:
            print("\n⚠️  빌드는 성공했으나 압축 파일 생성에 실패했습니다.")
            print(f"   📂 폴더: {target_folder}")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    build_exe()
