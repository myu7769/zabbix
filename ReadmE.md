# Zabbix 호스트 관리 도구

> **📝 수정 정보**: 2025년 8월 5일 커서로 수정

Zabbix 서버의 호스트를 효율적으로 관리하는 Python GUI 애플리케이션입니다.

## 🚀 주요 기능

- **🔐 안전한 로그인**: 서버별 인증 및 로그인 상태 확인
- **📊 호스트 조회**: Zabbix 서버에서 호스트 정보를 상세히 조회
- **⚡ 호스트 제어**: 선택된 호스트의 활성화/비활성화
- **🗑️ 호스트 삭제**: 안전한 호스트 삭제 기능
- **🔧 유지보수 관리**: 선택된 호스트에 대한 유지보수 생성
- **📁 파일 로드**: 텍스트 파일에서 호스트 목록을 일괄 로드
- **✅ 실시간 상태**: 작업 결과를 실시간으로 확인

## 📋 시스템 요구사항

- **Python**: 3.8 이상
- **운영체제**: Windows, macOS, Linux
- **네트워크**: Zabbix 서버 접근 가능

## 🛠️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/myu7769/zabbix.git
cd zabbix
```

### 2. 가상환경 생성 및 활성화
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install requests
```

### 4. 설정 구성
`config.py` 파일에서 Zabbix 서버 정보를 설정하세요:

```python
# 환경 변수로 설정 (권장)
export ZABBIX_USERNAME="your_username"
export ZABBIX_PASSWORD="your_password"

# 또는 config.py에서 직접 설정
USERNAME = "your_username"
PASSWORD = "your_password"
```

### 5. 애플리케이션 실행
```bash
python UiTest.py
```

## 📦 EXE 파일 생성

### 자동 생성
```bash
python Getexe.py
```

### 수동 생성
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole UiTest.py
```

## 📁 프로젝트 구조

```
zabbix/
├── config.py              # 설정 관리
├── zabbixAuth.py          # 인증 모듈
├── zabbixHost.py          # 호스트 관리 모듈
├── login_dialog.py        # 로그인 다이얼로그
├── UiTest.py              # 메인 GUI 애플리케이션
├── Getexe.py              # EXE 생성 스크립트
├── README.md              # 프로젝트 문서
└── .gitignore             # Git 무시 파일
```

## 🎯 사용법

### 1. 서버 선택
- **COMMON**: 일반 서버
- **GAME**: 게임 서버

### 2. 로그인
- 서버 선택 후 사용자명과 비밀번호 입력
- 로그인 성공/실패 상태 확인

### 3. 호스트 관리
1. **파일 로드**: 호스트 목록 파일 선택
   - 형식: `호스트명,IP주소` (한 줄에 하나씩)
2. **호스트 선택**: 체크박스로 작업할 호스트 선택
3. **작업 실행**: 원하는 작업 버튼 클릭

### 4. 작업 종류
- **호스트 정보 확인**: 선택된 호스트의 상세 정보 조회
- **호스트 활성화**: 선택된 호스트를 활성화
- **호스트 비활성화**: 선택된 호스트를 비활성화
- **호스트 삭제**: 선택된 호스트를 삭제 (확인 필요)
- **유지보수 생성**: 선택된 호스트에 유지보수 설정

## 🔧 주요 개선사항

### 코드 구조 개선
- ✅ 모듈화된 구조로 변경
- ✅ 클래스 기반 설계 적용
- ✅ 타입 힌트 추가로 코드 가독성 향상
- ✅ 에러 처리 강화

### 중복 코드 제거
- ✅ 공통 API 클라이언트 생성
- ✅ 설정 중앙화
- ✅ 메시지 상수화

### UI/UX 개선
- ✅ 로그인 다이얼로그 추가
- ✅ 실시간 상태 표시
- ✅ 사용자 친화적 메시지
- ✅ 반응형 레이아웃

### 보안 강화
- ✅ 환경 변수를 통한 인증 정보 관리
- ✅ 안전한 로그인 검증
- ✅ 작업 확인 다이얼로그

## 🚨 주의사항

### 보안
- 인증 정보는 환경 변수로 관리하는 것을 권장합니다
- 프로덕션 환경에서는 안전한 인증 방식을 사용하세요

### 네트워크
- Zabbix 서버에 대한 네트워크 접근이 필요합니다
- 방화벽 설정을 확인하세요

### 작업 주의
- 호스트 삭제는 되돌릴 수 없으므로 신중하게 진행하세요
- 대량 작업 전에 테스트 환경에서 검증하세요

## 🐛 문제 해결

### 로그인 실패
1. 사용자명과 비밀번호 확인
2. 서버 URL 접근 가능 여부 확인
3. 네트워크 연결 상태 확인

### EXE 파일 실행 오류
1. Windows Defender 예외 설정
2. 관리자 권한으로 실행
3. .NET Framework 설치 확인

### 네트워크 오류
1. Zabbix 서버 URL 확인
2. 방화벽 설정 확인
3. 프록시 설정 확인

## 📈 버전 히스토리

| 버전 | 날짜 | 주요 변경사항 |
|------|------|---------------|
| v1.0 | 2024-08-05 | 완전한 리팩토링 및 로그인 다이얼로그 추가 |
| v0.3 | 2024-04-01 | 유지보수 기능 구현 완료 |
| v0.2 | 2024-03-28 | GUI 개선, 카운터 추가 |
| v0.1 | 2024-03-26 | 기본 기능 구현 |

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 내부 사용을 위한 도구입니다.

## 📞 지원

문제가 발생하거나 기능 요청이 있으시면 이슈를 등록해주세요.

---

**개발자**: 김명종  
**최종 업데이트**: 2025년 8월 5일
