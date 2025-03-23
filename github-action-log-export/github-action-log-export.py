#!/usr/bin/env python3
"""
GitHub Actions 워크플로우 로그 다운로더
특정 기간 동안의 GitHub Actions 워크플로우 실행 로그를 다운로드하고 저장합니다.
"""

import argparse
import logging
import os
import sys
import zipfile
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitHubWorkflowLogger:
    def __init__(self, token: str, owner: str, repo: str, workflow_id: str, 
                timeout: int = 30, proxies: Optional[Dict[str, str]] = None):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.workflow_id = workflow_id
        self.timeout = timeout
        self.proxies = proxies
        self.headers = {
            "Authorization": f"token {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json"
        }

    def get_workflow_runs(self, start_time: datetime = None, end_time: datetime = None) -> List[Dict[str, Any]]:
        """워크플로우 실행 목록을 가져옵니다. 날짜 범위가 지정된 경우 API에서 직접 필터링합니다."""
        all_runs = []
        page = 1
        
        # 날짜 범위 매개변수 설정
        date_filter = None
        if start_time and end_time:
            # GitHub API 'created' 파라미터 포맷: YYYY-MM-DD
            start_date_str = start_time.strftime("%Y-%m-%d")
            end_date_str = end_time.strftime("%Y-%m-%d")
            date_filter = f"{start_date_str}..{end_date_str}"
            logger.info(f"날짜 필터 적용: {date_filter}")
        
        while True:
            runs_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/workflows/{self.workflow_id}/runs"
            params = {"per_page": 100, "page": page}
            
            # 날짜 필터 추가
            if date_filter:
                params["created"] = date_filter
            
            try:
                response = requests.get(
                    runs_url, 
                    headers=self.headers, 
                    params=params, 
                    timeout=self.timeout,
                    proxies=self.proxies
                )
                response.raise_for_status()
                runs_page = response.json().get("workflow_runs", [])
                
                if not runs_page:
                    break
                    
                all_runs.extend(runs_page)
                logger.info(f"페이지 {page}: {len(runs_page)}개의 실행")
                page += 1
                
            except requests.exceptions.RequestException as e:
                logger.error(f"워크플로우 실행 목록 조회 중 오류 발생: {e}")
                sys.exit(1)
        
        return all_runs

    def filter_runs_by_date(self, runs: List[Dict[str, Any]], 
                          start_time: datetime, 
                          end_time: datetime) -> List[Dict[str, Any]]:
        """날짜 범위에 해당하는 실행만 필터링합니다. API 필터링 후 추가 검증용으로 사용합니다."""
        target_runs = []
        for run in runs:
            run_time = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
            if start_time <= run_time <= end_time:
                logger.info(f"대상 실행: {run['id']} (생성 시각: {run['created_at']})")
                target_runs.append(run)
        return target_runs

    def download_and_save_logs(self, runs: List[Dict[str, Any]], base_dir: str) -> None:
        """선택된 실행의 로그를 다운로드하고 저장합니다."""
        # 기본 디렉토리를 Path 객체로 변환
        base_path = Path(base_dir)
        
        for run in runs:
            run_id = run["id"]
            created_at = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
            date_str = created_at.strftime("%Y-%m-%d")
            
            # 경로 생성을 Path 객체를 사용하여 수행
            date_dir = base_path / date_str
            run_dir = date_dir / f"run_{run_id}"
            # 디렉토리가 존재하지 않으면 생성
            run_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"다운로드 중: 실행 ID {run_id}")
            
            try:
                logs_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/runs/{run_id}/logs"
                logs_response = requests.get(
                    logs_url, 
                    headers=self.headers,
                    timeout=self.timeout,
                    proxies=self.proxies
                )
                logs_response.raise_for_status()
                
                # ZIP 파일 저장
                zip_filename = run_dir / "logs.zip"
                with open(zip_filename, "wb") as f:
                    f.write(logs_response.content)
                
                # ZIP 파일 압축 해제
                with zipfile.ZipFile(io.BytesIO(logs_response.content)) as z:
                    z.extractall(run_dir)
                    
                logger.info(f"로그 저장 완료: {run_dir}")
                
            except Exception as e:
                logger.error(f"실행 {run_id}의 로그 처리 중 오류 발생: {e}")

def main():
    parser = argparse.ArgumentParser(description='GitHub Actions 워크플로우 로그 다운로더')
    parser.add_argument('--owner', required=True, help='GitHub 리포지토리 소유자')
    parser.add_argument('--repo', required=True, help='GitHub 리포지토리 이름')
    parser.add_argument('--workflow', required=True, help='워크플로우 파일명 또는 ID')
    parser.add_argument('--start-date', required=True, help='시작 날짜 (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='종료 날짜 (YYYY-MM-DD)')
    parser.add_argument('--output-dir', default='logs', help='로그 저장 디렉토리')
    parser.add_argument('--timeout', type=int, default=30, help='HTTP 요청 타임아웃(초)')
    parser.add_argument('--proxy', help='프록시 URL (예: http://user:pass@proxy:port)')
    
    args = parser.parse_args()
    
    # 환경 변수에서 토큰 로드 (.env 파일 및 환경 변수)
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        logger.error("GITHUB_TOKEN 환경 변수가 설정되어 있지 않습니다.")
        sys.exit(1)
    
    # 프록시 설정
    proxies = None
    if args.proxy:
        proxies = {
            "http": args.proxy,
            "https": args.proxy
        }
    
    # 날짜 문자열을 datetime 객체로 변환
    start_time = datetime.strptime(args.start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end_time = datetime.strptime(args.end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end_time = end_time.replace(hour=23, minute=59, second=59)  # 종료일 마지막 시간으로 설정
    
    # 로거 초기화 및 실행
    workflow_logger = GitHubWorkflowLogger(
        token, 
        args.owner, 
        args.repo, 
        args.workflow,
        timeout=args.timeout,
        proxies=proxies
    )
    # API에서 날짜로 필터링된 워크플로우 실행 가져오기
    filtered_runs = workflow_logger.get_workflow_runs(start_time, end_time)
    logger.info(f"API 필터링으로 {len(filtered_runs)}개의 워크플로우 실행 조회됨")
    
    # 추가 검증 (시간까지 정확하게 필터링)
    target_runs = workflow_logger.filter_runs_by_date(filtered_runs, start_time, end_time)
    logger.info(f"시간 범위 필터링 후 {len(target_runs)}개의 워크플로우 실행 대상")
    
    # 로그 다운로드 및 저장
    workflow_logger.download_and_save_logs(target_runs, args.output_dir)

if __name__ == "__main__":
    main()