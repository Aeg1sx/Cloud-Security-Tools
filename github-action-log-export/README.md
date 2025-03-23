# GitHub Actions 워크플로우 로그 다운로더

*[English version](README_EN.md)*

GitHub Actions의 특정 기간 동안의 워크플로우 실행 로그를 다운로드하고 저장하는 도구입니다.

## 기능

- 특정 기간 동안의 GitHub Actions 워크플로우 실행 로그 다운로드
- 날짜별로 구조화된 로그 저장
- 원본 ZIP 파일 및 압축 해제된 로그 파일 저장
- 상세한 로깅 제공
- Windows, macOS, Linux 등 모든 운영체제 지원
- 프록시 환경 지원
- 네트워크 타임아웃 설정 지원

## 요구사항

- Python 3.6 이상
- GitHub Personal Access Token (repo 스코프 필요)

## 설치

1. 저장소를 클론합니다:
```bash
git clone https://github.com/yourusername/github-workflow-logger.git
cd github-workflow-logger
```

2. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정:
`.env` 파일을 생성하고 GitHub 토큰을 설정합니다:
```
GITHUB_TOKEN=your_github_token_here
```

## 사용법

기본 사용법:
```bash
python github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

### 명령줄 인자

- `--owner`: GitHub 리포지토리 소유자 (필수)
- `--repo`: GitHub 리포지토리 이름 (필수)
- `--workflow`: 워크플로우 파일명 또는 ID (필수)
- `--start-date`: 시작 날짜 (YYYY-MM-DD 형식, 필수)
- `--end-date`: 종료 날짜 (YYYY-MM-DD 형식, 필수)
- `--output-dir`: 로그 저장 디렉토리 (기본값: 'logs')
- `--timeout`: HTTP 요청 타임아웃(초) (기본값: 30)
- `--proxy`: 프록시 URL (예: http://user:pass@proxy:port)

## 운영체제별 사용 방법

### Windows

Windows에서는 다음과 같이 실행할 수 있습니다:

```
python github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

Windows에서 환경 변수 설정 (PowerShell):
```
$env:GITHUB_TOKEN = "your_github_token_here"
```

### macOS / Linux

macOS와 Linux에서는 다음과 같이 실행할 수 있습니다:

```
python3 github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

macOS/Linux에서 환경 변수 설정:
```
export GITHUB_TOKEN=your_github_token_here
```

## 프록시 환경 사용하기

회사 네트워크 등에서 프록시를 사용해야 하는 경우 `--proxy` 옵션을 사용할 수 있습니다:

```
python github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD --proxy http://proxy.company.com:8080
```

인증이 필요한 프록시의 경우:

```
python github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD --proxy http://username:password@proxy.company.com:8080
```

## 출력 구조

다운로드된 로그는 다음과 같은 구조로 저장됩니다:
```
logs/
└── YYYY-MM-DD/
    └── run_RUN_ID/
        ├── logs.zip
        └── [압축 해제된 로그 파일들]
```

## 라이선스

MIT License

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 