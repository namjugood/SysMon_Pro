# SysMon Pro (System Monitoring Dashboard)

**SysMon Pro**는 사내 시스템(BXM Admin)의 로그와 트랜잭션을 실시간으로 모니터링하기 위한 데스크톱 애플리케이션입니다.
현재 버전(v2.0)은 실제 API와 연동되어 시스템 로그를 조회하고 분석할 수 있는 기능을 제공합니다.

## 📸 주요 기능
1. **Dark Theme Dashboard**
   - 장시간 모니터링에 최적화된 어두운 테마(Dracula tone) 적용
   - 직관적인 상태 표시 (성공 ✅ / 실패 ❌)

2. **3-Pane Layout (3분할 화면)**
   - **Main List**: 타임스탬프, GUID, 서비스명, 에러 여부를 리스트로 확인
   - **Transaction Detail**: 선택한 트랜잭션의 입/출력 값(RAW Data) 및 상세 정보 조회 (접기/펼치기 가능)
   - **Full Log View**: 상세 텍스트 로그 및 디버깅 정보 확인 (검색어/에러 라인 하이라이팅 지원)

3. **Real API Integration**
   - **BXM Admin API 연동**: 실제 운영 시스템의 로그 조회 API(`getServiceLogList`)와 연동
   - **Multi-Login Support**: 여러 운영 서버의 URL과 계정 정보를 `Tools > Options` 메뉴에서 관리하고 간편하게 로그인

4. **Enhanced Search & Filter**
   - **Time Range**: 30분 단위의 정밀한 날짜/시간 조회 조건 설정
   - **Keyword Filter**: GUID, IP, 서비스명, 오퍼레이션명 등에 대한 통합 검색 지원

5. **Improved UX**
   - **Loading Overlay**: API 통신 중 화면을 Dim 처리하여 작업 진행 상태 시각화
   - **Log Highlighting**: 검색어(노란색), 에러 라인(붉은색 배경) 자동 강조

## 🛠 기술 스택 (Tech Stack)
- **Language**: Python 3.9+
- **GUI Framework**: PyQt6
- **Network**: Requests (Session & Cookie handling)
- **Architecture**:
  - **Config**: 시스템 설정 및 URL 데이터 관리 (`utils/config_manager.py`)
  - **Core**: API 통신(`api_service.py`) 및 비동기 처리
  - **UI**: 메인 윈도우, 다이얼로그, 커스텀 위젯 분리 구조
  - **Utils**: 공통 스타일(QSS) 및 로깅

## 📂 프로젝트 구조
```text
bxm_monitoring/
├── config/              # 시스템 설정
│   └── settings.py      # 앱 상수 정의
├── core/                # 핵심 로직
│   ├── api_service.py   # (New) 실제 API 통신 모듈
│   └── mock_api.py      # (Legacy) 테스트용 가상 데이터 생성기
├── ui/                  # UI 컴포넌트
│   ├── widgets/         # 재사용 위젯
│   │   ├── custom_widgets.py # Panel, LoadingOverlay 등
│   │   └── menu_bar.py       # (New) 메뉴바 관리
│   ├── main_window.py   # 메인 대시보드 로직
│   ├── api_login_dialog.py # (New) API 로그인 입력창
│   └── options_dialog.py   # (New) URL/계정 관리 팝업
├── utils/               # 유틸리티
│   ├── config_manager.py # (New) 설정 파일(JSON) 입출력
│   ├── styles.py        # 통합 스타일시트 (QSS)
│   └── logger.py        # 로깅 설정
├── main.py              # 프로그램 진입점
├── requirements.txt     # 의존성 목록
└── README.md            # 프로젝트 문서
````

## 🚀 설치 및 실행 방법

### 1\. 환경 설정

필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

### 2\. 프로그램 실행

메인 스크립트를 실행하여 대시보드를 띄웁니다.

```bash
python main.py
```

### 3\. 사용 가이드

1.  상단 메뉴의 **Tools \> Options**를 클릭합니다.
2.  접속할 BXM Admin 시스템의 **이름, URL, ID, Password**를 추가하고 저장합니다.
3.  메인 화면 상단에 생성된 **바로가기 버튼**을 클릭하여 로그인합니다.
4.  조회를 원하는 **날짜와 시간**을 설정하고 **Search** 버튼을 누릅니다.

## 🗓 완료된 작업 (Completed)

  - [x] **실제 API 연동**: BXM Admin 로그인 및 로그 조회 구현 완료
  - [x] **검색 및 필터**: 날짜/시간 범위 및 키워드 필터링 적용
  - [x] **URL 관리자**: 접속 정보 저장/관리 기능(Options) 구현
  - [x] **UI/UX 개선**: 로딩 오버레이, 다크 테마, 로그 하이라이팅 적용

## 🗓 향후 계획 (Roadmap)

  - [ ] **자동 새로고침**: 주기적인 데이터 폴링(Polling) 기능 추가
  - [ ] **배포**: PyInstaller를 이용한 실행 파일(.exe) 패키징
  - [ ] **상세 로그 파싱**: `raw_input` 등 JSON 데이터의 Tree View 시각화