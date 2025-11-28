# SysMon Pro (System Monitoring Dashboard)

**SysMon Pro**는 사내 시스템의 로그와 트랜잭션을 실시간으로 모니터링하기 위한 데스크톱 애플리케이션입니다.
현재 버전(v2.0)은 UI/UX 프로토타입 단계로, **Mock API**를 통해 생성된 가상의 로그 데이터를 사용하여 대시보드 기능을 시연합니다.

## 📸 주요 기능
1. **Dark Theme Dashboard**
   - 장시간 모니터링에 최적화된 어두운 테마(Dracula tone) 적용
   - 직관적인 상태 표시 (성공 ✅ / 실패 ❌)

2. **3-Pane Layout (3분할 화면)**
   - **Main List**: 타임스탬프, GUID, 서비스명, 에러 여부를 리스트로 확인
   - **Transaction Detail**: 선택한 트랜잭션의 입/출력 값(JSON) 상세 조회
   - **Full Log View**: 상세 텍스트 로그 및 디버깅 정보 확인

3. **Mock Data Generation**
   - 실제 서버 연동 전, 다양한 에러 상황과 트랜잭션을 시뮬레이션하는 가상 데이터 생성기 탑재

## 🛠 기술 스택 (Tech Stack)
- **Language**: Python 3.9+
- **GUI Framework**: PyQt6
- **Network**: Requests (추후 실제 API 연동 시 사용)
- **Architecture**:
  - **Config**: 설정 및 상수 관리
  - **Core**: 비즈니스 로직 및 데이터 처리
  - **UI**: 화면 레이아웃 및 위젯 (Splitter 기반)
  - **Utils**: 공통 스타일(CSS) 및 로깅

## 📂 프로젝트 구조
```text
bxm_monitoring/
├── config/              # 시스템 설정
│   └── settings.py      # 앱 타이틀, 버전, 상수 정의
├── core/                # 핵심 로직
│   └── mock_api.py      # 테스트용 가상 데이터 생성기
├── ui/                  # UI 컴포넌트
│   ├── widgets/         # 재사용 가능한 커스텀 위젯 (Panel 등)
│   └── main_window.py   # 메인 대시보드 및 레이아웃 조립
├── utils/               # 유틸리티
│   ├── styles.py        # 다크 테마(QSS) 스타일시트 정의
│   └── logger.py        # 로깅 설정
├── main.py              # 프로그램 진입점 (Entry Point)
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

## 🗓 향후 계획 (Roadmap)

  - [ ] **실제 API 연동**: MockApiService를 실제 서버 API 클라이언트로 교체
  - [ ] **검색 및 필터**: GUID, 서비스명, 날짜별 검색 기능 구현
  - [ ] **자동 새로고침**: 주기적인 데이터 폴링(Polling) 기능 추가
  - [ ] **배포**: PyInstaller를 이용한 실행 파일(.exe) 패키징

