# GitHub Actions Workflow Log Downloader

A tool to download and save GitHub Actions workflow run logs for a specific period.

*[한국어 버전](README.md)*

## Features

- Download GitHub Actions workflow run logs for a specific period
- Store logs in a structured format by date
- Save original ZIP files and extracted log files
- Provide detailed logging
- Support for Windows, macOS, Linux and all operating systems
- Proxy environment support
- Network timeout setting support

## Requirements

- Python 3.6 or higher
- GitHub Personal Access Token (with repo scope)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/github-workflow-logger.git
cd github-workflow-logger
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
Create a `.env` file and set your GitHub token:
```
GITHUB_TOKEN=your_github_token_here
```

## Usage

Basic usage:
```bash
python github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

### Command Line Arguments

- `--owner`: GitHub repository owner (required)
- `--repo`: GitHub repository name (required)
- `--workflow`: Workflow file name or ID (required)
- `--start-date`: Start date (YYYY-MM-DD format, required)
- `--end-date`: End date (YYYY-MM-DD format, required)
- `--output-dir`: Log save directory (default: 'logs')
- `--timeout`: HTTP request timeout in seconds (default: 30)
- `--proxy`: Proxy URL (e.g., http://user:pass@proxy:port)

## Operating System-Specific Usage

### Windows

On Windows, you can run it as follows:

```
python github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

Setting environment variables in Windows (PowerShell):
```
$env:GITHUB_TOKEN = "your_github_token_here"
```

### macOS / Linux

On macOS and Linux, you can run it as follows:

```
python3 github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

Setting environment variables in macOS/Linux:
```
export GITHUB_TOKEN=your_github_token_here
```

## Using Proxy Environments

If you need to use a proxy in a corporate network or similar environment, you can use the `--proxy` option:

```
python github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD --proxy http://proxy.company.com:8080
```

For proxies requiring authentication:

```
python github-action-log-export.py --owner OWNER --repo REPO --workflow WORKFLOW_ID --start-date YYYY-MM-DD --end-date YYYY-MM-DD --proxy http://username:password@proxy.company.com:8080
```

## Output Structure

Downloaded logs are stored in the following structure:
```
logs/
└── YYYY-MM-DD/
    └── run_RUN_ID/
        ├── logs.zip
        └── [extracted log files]
```

## License

MIT License

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 