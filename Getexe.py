import subprocess
from datetime import datetime

# 현재 날짜 가져오기 (예: 0410)
current_date = datetime.now().strftime("%m%d")

# 실행할 PyInstaller 명령어 설정
command = f'pyinstaller --onefile --noconsole -n ZabbixHost_{current_date} UiTest.py'

# subprocess를 사용하여 명령어 실행
subprocess.run(command, shell=True)
