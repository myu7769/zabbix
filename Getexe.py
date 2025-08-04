"""
PyInstaller를 사용한 EXE 파일 생성 스크립트
"""
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path


def create_exe_file():
    """EXE 파일 생성"""
    try:
        # 현재 날짜 가져오기 (예: 0805)
        current_date = datetime.now().strftime("%m%d")
        
        # 실행할 PyInstaller 명령어 설정
        command = [
            'pyinstaller',
            '--onefile',
            '--noconsole',
            '--name', f'ZabbixHost_{current_date}',
            'UiTest.py'
        ]
        
        print(f"EXE 파일 생성을 시작합니다...")
        print(f"명령어: {' '.join(command)}")
        
        # subprocess를 사용하여 명령어 실행
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("EXE 파일이 성공적으로 생성되었습니다!")
            print(f"생성된 파일: dist/ZabbixHost_{current_date}.exe")
        else:
            print("EXE 파일 생성에 실패했습니다.")
            print(f"오류: {result.stderr}")
            
    except Exception as e:
        print(f"EXE 파일 생성 중 오류가 발생했습니다: {e}")


def check_dependencies():
    """의존성 확인"""
    try:
        import tkinter
        import requests
        print("필수 의존성이 설치되어 있습니다.")
        return True
    except ImportError as e:
        print(f"필수 의존성이 설치되지 않았습니다: {e}")
        print("다음 명령어로 설치하세요:")
        print("pip install requests")
        return False


def check_pyinstaller():
    """PyInstaller 설치 확인"""
    try:
        import PyInstaller
        print("PyInstaller가 설치되어 있습니다.")
        return True
    except ImportError:
        print("PyInstaller가 설치되지 않았습니다.")
        print("다음 명령어로 설치하세요:")
        print("pip install pyinstaller")
        return False


def main():
    """메인 함수"""
    print("Zabbix 호스트 관리 도구 EXE 파일 생성기")
    print("=" * 50)
    
    # 의존성 확인
    if not check_dependencies():
        return
    
    if not check_pyinstaller():
        return
    
    # EXE 파일 생성
    create_exe_file()


if __name__ == "__main__":
    main()
