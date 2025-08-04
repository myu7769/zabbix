"""
로그인 다이얼로그 모듈
"""
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple
from zabbixAuth import zabbix_login


class LoginDialog:
    """로그인 다이얼로그 클래스"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        
    def show(self) -> Optional[Tuple[str, str, str]]:
        """
        로그인 다이얼로그를 표시합니다.
        
        Returns:
            (url, username, password) 튜플 또는 None
        """
        dialog = tk.Toplevel(self.parent)
        dialog.title("Zabbix 로그인")
        dialog.geometry("440x500")  # 창 크기 더 늘림
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 중앙 정렬
        dialog.resizable(False, False)
        
        # 메인 프레임
        main_frame = tk.Frame(dialog, padx=30, pady=40)
        main_frame.pack(fill="both", expand=True)
        
        # 제목
        title_label = tk.Label(main_frame, text="Zabbix 서버 로그인", font=("Arial", 15, "bold"))
        title_label.pack(pady=(0, 35))
        
        # 서버 선택
        server_frame = tk.Frame(main_frame)
        server_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(server_frame, text="서버 선택:", font=("Arial", 12)).pack(anchor="w")
        
        server_var = tk.StringVar(value="COMMON")
        server_radio_frame = tk.Frame(server_frame)
        server_radio_frame.pack(anchor="w", pady=(7, 0))
        
        tk.Radiobutton(server_radio_frame, text="COMMON", variable=server_var, 
                      value="COMMON", font=("Arial", 12)).pack(side="left", padx=(0, 18))
        tk.Radiobutton(server_radio_frame, text="GAME", variable=server_var, 
                      value="GAME", font=("Arial", 12)).pack(side="left")
        
        # 사용자명 입력
        username_frame = tk.Frame(main_frame)
        username_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(username_frame, text="사용자명:", font=("Arial", 12)).pack(anchor="w")
        username_entry = tk.Entry(username_frame, width=32, font=("Arial", 13))
        username_entry.pack(fill="x", pady=(7, 0))
        
        # 비밀번호 입력
        password_frame = tk.Frame(main_frame)
        password_frame.pack(fill="x", pady=(0, 40))
        
        tk.Label(password_frame, text="비밀번호:", font=("Arial", 12)).pack(anchor="w")
        password_entry = tk.Entry(password_frame, width=32, show="*", font=("Arial", 13))
        password_entry.pack(fill="x", pady=(7, 0))
        
        # # 테스트용 기본값 설정
        # username_entry.insert(0, "hi")
        # password_entry.insert(0, "hi")
        
        # 버튼 프레임 - 더 명확하게 배치
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side="bottom", pady=(40, 0), fill="x")
        
        def on_login():
            """로그인 버튼 클릭 처리"""
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("오류", "사용자명과 비밀번호를 모두 입력해주세요.")
                return
            
            # 서버 URL 결정
            if server_var.get() == "COMMON":
                from config import Config
                url = Config.COMMON_URL
            else:
                from config import Config
                url = Config.GAME_URL
            
            # 로그인 시도
            try:
                token = zabbix_login(url, username, password)
                if token:
                    messagebox.showinfo("성공", "로그인이 성공했습니다!")
                    self.result = (url, username, password)
                    dialog.destroy()
                else:
                    messagebox.showerror("실패", "로그인에 실패했습니다.\n사용자명과 비밀번호를 확인해주세요.")
            except Exception as e:
                messagebox.showerror("오류", f"로그인 중 오류가 발생했습니다:\n{str(e)}")
        
        def on_cancel():
            """취소 버튼 클릭 처리"""
            dialog.destroy()
        
        # 버튼들 - 더 명확하게 배치
        login_button = tk.Button(button_frame, text="로그인", command=on_login, 
                               width=15, height=2, bg="#4CAF50", fg="white", 
                               font=("Arial", 12, "bold"), relief="raised", bd=3)
        login_button.pack(side="left", padx=(0, 20))
        
        cancel_button = tk.Button(button_frame, text="취소", command=on_cancel, 
                                width=12, height=2, font=("Arial", 12))
        cancel_button.pack(side="left")
        
        # 초점 설정
        username_entry.focus()
        
        # 다이얼로그가 닫힐 때까지 대기
        dialog.wait_window()
        
        return self.result 