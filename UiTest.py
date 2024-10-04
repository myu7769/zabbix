import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from zabbixHost import *
from tkinter.simpledialog import askstring

ZABBIX_GLOBAL_URL = ''
COMMON = 'http://ncsma.ncsoft.net/zabbix/api_jsonrpc.php'
GAME = 'http://ncsma.ncsoft.net/zabbix-game/api_jsonrpc.php'

class CheckableTreeview(ttk.Treeview):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self['columns'] = ('호스트 이름', 'IP 주소')
        self.heading('#0', text='선택', anchor='w')
        self.column('#0', width=20, anchor='w')
        self.heading('호스트 이름', text='호스트 이름')
        self.heading('IP 주소', text='IP 주소')

        self.bind('<Button-1>', self.on_click)
        self.bind('<Double-1>', self.on_double_click)
        self.bind("<Button-3>", self.on_right_click)  # 마우스 오른쪽 클릭 이벤트 바인딩
        self.heading('#0', command=self.toggle_all_checks)

        self.right_click_menu = tk.Menu(self, tearoff=0)
        self.right_click_menu.add_command(label="호스트 추가", command=self.add_host)
        self.right_click_menu.add_command(label="선택된 항목 삭제", command=self.delete_selected_host)
  
        self.host_count_label = None

    def update_checked_count(self, event=None):
        # 체크된 항목의 수를 계산하고 라벨 업데이트
        checked_items = self.checked_items()
        self.checked_count_label.configure(text=f"체크된 항목 수: {len(checked_items)}")

    def on_click(self, event):
        region = self.identify("region", event.x, event.y)
        column = self.identify_column(event.x)
        if region == "tree" and column == "#0":
            item = self.identify_row(event.y)
            if self.item(item, 'text') == "✓":
                self.item(item, text=" ")
            else:
                self.item(item, text="✓")
            self.update_checked_count()  # 체크된 항목 수 업데이트 호출

    def set_host_count_label(self, label_widget):
        """호스트 수 카운터 라벨 위젯을 설정합니다."""
        self.host_count_label = label_widget
        self.update_host_count()  # 초기 호스트 수 업데이트

    def update_host_count(self):
        """트리뷰에 있는 호스트의 수를 업데이트합니다."""
        if self.host_count_label:
            host_count = len(self.get_children())
            self.host_count_label.configure(text=f"전체 호스트 수: {host_count}")

    def toggle_all_checks(self):
        children = self.get_children()
        if not children:
            return
        
        first_item_checked = self.item(children[0], 'text') == "✓"
        new_state = " " if first_item_checked else "✓"
        
        for item in children:
            self.item(item, text=new_state)
        self.update_checked_count()  # 체크된 항목 수 업데이트 호출

    def checked_items(self):
        return [item for item in self.get_children() if self.item(item, 'text') == "✓"]

    def on_double_click(self, event):
        region = self.identify_region(event.x, event.y)
        column = self.identify_column(event.x)
        item = self.identify_row(event.y)
        if region == 'cell' and column in ('#1', '#2'):
            self.entry_popup(item, column, event)

    def update_item_values(self, item, column, new_val):
        values = list(self.item(item, 'values'))
        col_index = int(column[1]) - 1
        values[col_index] = new_val
        return tuple(values)
    
    def entry_popup(self, item, column, event):
        # 현재 값 가져오기
        value = self.item(item, 'values')[int(column[1]) - 1]

        # Entry 위젯 생성 및 설정
        entry = tk.Entry(self)
        entry.insert(0, value)
        entry.select_range(0, tk.END)
        entry.focus()
        
        # 위치 조정
        entry_x = self.bbox(item, column)[0]
        entry_y = self.bbox(item, column)[1]
        entry.place(x=entry_x, y=entry_y, width=self.bbox(item, column)[2], height=self.bbox(item, column)[3])

        def save_edit(event=None):
            self.item(item, values=self.update_item_values(item, column, entry.get()))
            entry.destroy()

        def cancel_edit(event=None):
            entry.destroy()

        entry.bind('<Return>', save_edit)
        entry.bind('<Escape>', cancel_edit)
        entry.bind('<FocusOut>', save_edit)

    def update_host_ip(self, initial_hostname, actual_hostname, new_ip):
        """검색된 호스트 이름을 기준으로 특정 호스트의 IP 주소를 새로운 값으로 업데이트합니다."""
        found = False  # 호스트를 찾았는지 여부를 추적하는 플래그
        for item in tree.get_children():
            values = tree.item(item, 'values')
            # 검색된 actual_hostname을 사용하여 대소문자 구분 없이 비교
            if values[0] == initial_hostname:  
                # 새로운 IP 주소로 업데이트. 여기서는 검색된 호스트 이름(actual_hostname)의 대소문자 형태를 유지합니다.
                new_values = (actual_hostname, new_ip)  
                tree.item(item, values=new_values)
                found = True
                break
        if not found:
            output_window(f"\n{actual_hostname}을(를) 찾을 수 없습니다.")
        else:
            output_window(f"\n{actual_hostname} 정보를 업데이트하였습니다.")

    def on_right_click(self, event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()

    def add_host(self):
        hostname = askstring("호스트 추가", "호스트 이름을 입력하세요:")
        ip = askstring("호스트 추가", "IP 주소를 입력하세요:")
        if hostname and ip:
            self.insert('', tk.END, values=(hostname, ip))
        self.update_host_count()  # 호스트 수 업데이트
        self.update_checked_count() 



    def delete_selected_host(self):
        """트리뷰에서 현재 선택된 항목을 삭제합니다."""
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)
        print("선택된 항목이 삭제되었습니다.")
        self.update_host_count()  # 호스트 수 업데이트
        self.update_checked_count()

    def on_right_click(self, event):
        try:
            # 선택된 항목이 있을 때만 삭제 메뉴 활성화
            if self.selection():
                self.right_click_menu.entryconfig("선택된 항목 삭제", state="normal")
            else:
                self.right_click_menu.entryconfig("선택된 항목 삭제", state="disabled")
            self.right_click_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()

    def delete_selected_host(self):
        """트리뷰에서 현재 선택된 항목을 삭제합니다."""
        selected_items = self.selection()
        for item in selected_items:
            self.delete(item)
        print("선택된 항목이 삭제되었습니다.")
        self.update_host_count()  # 호스트 수 업데이트
        self.update_checked_count()

    def delete_all_hosts(self):
        """트리뷰의 모든 항목을 삭제합니다."""
        all_items = self.get_children()
        for item in all_items:
            self.delete(item)
        print("모든 호스트 정보가 삭제되었습니다.")
        self.update_host_count()  # 호스트 수 업데이트
        self.update_checked_count()
        

# host에 대한 IP를 가져와 GUI에 작성 api 구현
def get_host_ips():
    if not ZABBIX_GLOBAL_URL:
        messagebox.showerror("URL 확인", "Zabbix common or game ?")
        return
    
    if not tree.checked_items():
        messagebox.showerror("오류", "호스트를 선택해주세요.")
        return

    token = zabbix_login(ZABBIX_GLOBAL_URL, username, password)
    get_hosts_count = 0
    try:
        for item in tree.checked_items():
            original_hostname, ip = tree.item(item, 'values')

            # 대소문자 변형을 시도하는 리스트
            hostname_variants = [
                {'hostname': original_hostname.lower(), 'case': 'lower'},
                {'hostname': original_hostname.upper(), 'case': 'upper'}
            ]

            found = False
            for variant in hostname_variants:
                hostname = variant['hostname']
                result = zabbix_host_get(ZABBIX_GLOBAL_URL, token, hostname)
                if result:
                    actual_hostname = result[0]['hostname']  # 실제 호스트 이름을 API 응답에서 가져옴
                    ip = result[0]['ip']
                    # 실제 호스트 이름을 사용하여 업데이트
                    tree.update_host_ip(original_hostname, actual_hostname, ip)  # 항상 실제 호스트 이름으로 업데이트
                    results = format_host_details_to_string(result)
                    output_window("\n")
                    # if results:
                    #     output_window(results)  # 결과를 별도의 윈도우에 출력
                    found = True
                    get_hosts_count += 1
                    break  # 정보를 찾으면 반복 중단
            
            if not found:
                # 대소문자 변형에도 불구하고 정보를 찾지 못한 경우
                output_window("\n")
                output_window(f"{original_hostname} : 해당하는 호스트 정보를 찾을 수 없습니다.\n")

            tree.checked_count_label.configure(text=f"정상 조회된 호스트 수: {get_hosts_count}")

        
        messagebox.showinfo("Host Infomations", "선택된 Host에 대한 IP를 가져옵니다.")

    except ValueError as e:
        messagebox.showerror("오류", "API 호출 중 오류가 발생했습니다.")

# 활성화 버튼의 동작 구현
def activate_selected_hosts():

    if not ZABBIX_GLOBAL_URL:
        messagebox.showerror("URL 확인", "Zabbix common or game ?")
        return
    
    if not tree.checked_items():
        messagebox.showerror("오류", "호스트를 선택해주세요.")
        return
    
    # 성공과 실패를 추적하기 위한 딕셔너리 초기화
    results_summary = {'success': [], 'fail': [] , 'msg' : []}
    token = zabbix_login(ZABBIX_GLOBAL_URL, username, password)

    try:
        for item in tree.checked_items():
            hostname, ip = tree.item(item, 'values')
            print(hostname)

            host_info = [[hostname, ip]]
            result = enable_hosts_if_ip_matches(ZABBIX_GLOBAL_URL, token, host_info)

            # 결과를 요약 정보에 추가
            if result.get('success'):
                results_summary['success'].extend(result['success'])
            if result.get('fail'):
                results_summary['fail'].extend(result['fail'])
            if result.get('msg'):
                results_summary['msg'].extend(result['msg'])


        messagebox.showinfo("비활성화", "선택된 호스트를 활성화합니다.")  
        output_window("\n")

        # for문이 종료된 후, 결과 요약 정보 출력
        if results_summary['success']:
            output_window("활성화 성공한 호스트: " + ", ".join(results_summary['success']) + "\n")
        if results_summary['fail']:
            output_window("활성화 실패한 호스트: " + ", ".join(results_summary['fail']) + "\n")
        if results_summary['msg']:
            output_window("".join(results_summary['msg']) + "\n")

    except ValueError as e:
        messagebox.showerror("오류", "API 호출 중 오류가 발생했습니다.")
        output_window(str(e) + "\n")

# 비활성화 버튼의 동작 구현
def deactivate_selected_hosts():
    if not ZABBIX_GLOBAL_URL:
        messagebox.showerror("URL 확인", "Zabbix common or game ?")
        return
    
    if not tree.checked_items():
        messagebox.showerror("오류", "호스트를 선택해주세요.")
        return
    
    # 성공과 실패를 추적하기 위한 딕셔너리 초기화
    results_summary = {'success': [], 'fail': [] , 'msg' : []}
    token = zabbix_login(ZABBIX_GLOBAL_URL, username, password)

    try:
        for item in tree.checked_items():
            hostname, ip = tree.item(item, 'values')
            print(hostname)

            host_info = [[hostname, ip]]
            result = disable_hosts_if_ip_matches(ZABBIX_GLOBAL_URL, token, host_info)

            # 결과를 요약 정보에 추가
            if result.get('success'):
                results_summary['success'].extend(result['success'])
            if result.get('fail'):
                results_summary['fail'].extend(result['fail'])
            if result.get('msg'):
                results_summary['msg'].extend(result['msg'])

        messagebox.showinfo("비활성화", "선택된 호스트를 비활성화합니다.")
        output_window("\n")

        output_window("  " "\n")
        # for문이 종료된 후, 결과 요약 정보 출력
        if results_summary['success']:
            output_window("비활성화 성공한 호스트: " + ", ".join(results_summary['success']) + "\n")
        if results_summary['fail']:
            output_window("비활성화 실패한 호스트: " + ", ".join(results_summary['fail']) + "\n")
        if results_summary['msg']:
            output_window("".join(results_summary['msg']) + "\n")

    except ValueError as e:
        messagebox.showerror("오류", "API 호출 중 오류가 발생했습니다.")
        output_window(str(e) + "\n")

    # 여기에 실제 비활성화 작업 코드를 추가합니다.

def delete_selected_hosts_api():
    
    if not ZABBIX_GLOBAL_URL:
        messagebox.showerror("URL 확인", "Zabbix common or game ?")
        return
    
    if not tree.checked_items():
        messagebox.showerror("오류", "호스트를 선택해주세요.")
        return
    
    results_summary = {'success': [], 'fail': [] , 'msg' : []}
    messagebox.showinfo("삭제", "선택된 호스트를 삭제합니다.")
    # 사용자에게 확인을 요청하는 대화상자를 띄웁니다.
    response = messagebox.askokcancel("확인 요청", "계속 진행하시겠습니까?")
    if response:  # 사용자가 '확인'을 선택한 경우
        print("사용자가 확인을 선택했습니다.")
        token = zabbix_login(ZABBIX_GLOBAL_URL, username, password)        
        try:
            for item in tree.checked_items():
                hostname, ip = tree.item(item, 'values')
                print(hostname)

                host_info = [[hostname, ip]]
                result = zabbix_delete_api(ZABBIX_GLOBAL_URL, token, host_info)

                # 결과를 요약 정보에 추가
                if result.get('success'):
                    results_summary['success'].extend(result['success'])
                if result.get('fail'):
                    results_summary['fail'].extend(result['fail'])
                if result.get('msg'):
                    results_summary['msg'].extend(result['msg'])

            messagebox.showinfo("삭제", "선택된 호스트를 삭제합니다.")
            output_window("\n")

            output_window("  " "\n")
            # for문이 종료된 후, 결과 요약 정보 출력
            if results_summary['success']:
                output_window("삭제 성공한 호스트: " + ", ".join(results_summary['success']) + "\n")
            if results_summary['fail']:
                output_window("삭제 실패한 호스트: " + ", ".join(results_summary['fail']) + "\n")
            if results_summary['msg']:
                output_window("".join(results_summary['msg']) + "\n")

        except ValueError as e:
            messagebox.showerror("오류", "API 호출 중 오류가 발생했습니다.")
            output_window(str(e) + "\n")
    else:  # 사용자가 '취소'를 선택한 경우
        print("사용자가 취소를 선택했습니다.")
        
def create_zabbix_maintenance():
    if not ZABBIX_GLOBAL_URL:
        messagebox.showerror("URL 확인", "Zabbix common or game ?")
        return
    
    maintenance_subject = e3.get()
    if not maintenance_subject:
        messagebox.showerror("제목 확인", "제목을 입력해주세요")
        return

    try:
        start_time = string_to_unix_time(e4.get())
    except ValueError:
        messagebox.showerror("잘못된 날짜 형식입니다.", "Start time 올바른 형식으로 입력해주세요.")
        return

    try:
        end_time = string_to_unix_time(e5.get())
    except ValueError:
        messagebox.showerror("잘못된 날짜 형식입니다.", "End time 올바른 형식으로 입력해주세요.")
        return
    
    main_hostnames = [ ]
    main_hostgroups = [ ]

    try:
        token = zabbix_login(ZABBIX_GLOBAL_URL, username, password)
        hostGroups = e6.get().split()
        hostGroup = readGroupId(ZABBIX_GLOBAL_URL, token, hostGroups)
        hostGroupIds = [groupIds[1] for groupIds in hostGroup]
        main_hostgroups = [groupIds[0] for groupIds in hostGroup]
        hostnames = [tree.item(item, 'values')[0] for item in tree.checked_items()]

        hosts_Info = getHostId(url=ZABBIX_GLOBAL_URL, token=token, hostnames=hostnames)
        hostIds = [hostInfo['hostid'] for hostInfo in hosts_Info ]
        main_hostnames = [hostInfo['hostname'] for hostInfo in hosts_Info ]

        print(hostIds)

        result = create_maintenance(ZABBIX_GLOBAL_URL, token, maintenance_subject, hostIds, hostGroupIds, start_time, end_time)
    except Exception as e:
        messagebox.showerror("오류", f"API 호출 중 오류가 발생했습니다: {e}")
        return
    # 에러 정보 추출
    if "error" in result:
        error_message = result["error"]["data"]
        messagebox.showerror("오류", error_message)
        return
    else:
        print(main_hostnames)
        output_window("Maintenance 설정된 호스트: " + ", ".join(main_hostnames) + "\n")
        output_window("Maintenance 설정된 그룹: " + ", ".join(main_hostgroups) + "\n" )
        output_window("--------------------------------------------------------------" + "\n")
        # output_window(main_hostnames)
        messagebox.showinfo("성공", "Maintenance 가 성공적으로 생성되었습니다.")
        return

def output_window(text):
    # 윈도우가 이미 존재하는지 확인하고, 존재하지 않으면 새로 만든다.
    if not hasattr(output_window, "win") or output_window.win is None:
        output_window.win = tk.Toplevel(root)
        output_window.win.title("API 호출 결과")
        output_window.win.geometry("700x300")

        # 윈도우가 닫힐 때 실행될 함수를 정의한다.
        def on_close():
            # 윈도우 참조를 None으로 초기화하여 윈도우가 닫혔음을 표시한다.
            output_window.win.destroy()
            output_window.win = None

        # 윈도우 닫기 버튼을 누르면 on_close 함수가 호출되도록 한다.
        output_window.win.protocol("WM_DELETE_WINDOW", on_close)

        # 스크롤 가능한 텍스트 위젯을 생성하고 윈도우에 추가한다.
        output_window.text_widget = scrolledtext.ScrolledText(output_window.win, wrap=tk.WORD)
        output_window.text_widget.pack(expand=True, fill='both')
    else:
        # 윈도우가 이미 존재하면, 기존 윈도우를 맨 앞으로 가져온다.
        output_window.win.lift()

    # 텍스트 위젯에 텍스트를 추가하고, 스크롤을 가장 아래로 내린다.
    output_window.text_widget.insert(tk.END, text)
    output_window.text_widget.see(tk.END)

# 파일 로드 함수 정의
def load_file():
    filename = filedialog.askopenfilename(initialdir="/", title="파일 선택",
                                          filetypes=(("텍스트 파일", "*.txt"), ("모든 파일", "*.*")))
    if not filename:
        return

    tree.delete(*tree.get_children())
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) < 2:
                    parts = line.strip().split()  # 빈칸으로 분할 시도
                hostname = parts[0]
                ip = parts[1] if len(parts) > 1 else ""  # IP가 없는 경우 빈 문자열 사용
                tree.insert('', tk.END, values=(hostname, ip), text=" ")
        tree.update_host_count()


# API 호출 확인 함수 정의
def confirm_and_call_api():

    if not ZABBIX_GLOBAL_URL:
        messagebox.showerror("URL 확인", "Zabbix common or game ?")
        return
    token = zabbix_login(ZABBIX_GLOBAL_URL, username, password)
    
    if not tree.checked_items():
        messagebox.showerror("오류", "호스트를 선택해주세요.")
        return

    print(tree.checked_items())

    try:
        for item in tree.checked_items():
            hostname, ip = tree.item(item, 'values')

            # 소문자로 시도
            lowercase_hostname = hostname.lower()
            result = format_host_details_to_string(zabbix_host_get(ZABBIX_GLOBAL_URL, token, lowercase_hostname))

            if result:
                # 소문자로 성공한 경우
                success_hostname = lowercase_hostname
            else:
                # 대문자로 시도
                uppercase_hostname = hostname.upper()
                result = format_host_details_to_string(zabbix_host_get(ZABBIX_GLOBAL_URL, token, uppercase_hostname))
                if result:
                    # 대문자로 성공한 경우
                    success_hostname = uppercase_hostname
                else:
                    # 두 경우 모두 실패한 경우
                    success_hostname = None

            # 결과 출력
            output_window("\n")
            if success_hostname:
                # 성공한 경우, 변경된 hostname 상태를 출력
                output_window(f"{success_hostname} : 성공적으로 정보를 가져왔습니다.\n")
                output_window(result)  # 결과를 별도의 윈도우에 출력
            else:
                # 두 경우 모두 실패한 경우, 원래의 hostname 상태를 출력
                output_window(f"{hostname} : 해당하는 호스트 정보를 찾을 수 없습니다.\n")

        messagebox.showinfo("완료", "선택된 호스트에 대한 API 호출이 완료되었습니다.")
    except ValueError as e:
        messagebox.showerror("오류", "API 호출 중 오류가 발생했습니다.")

def radio_changed(*args):
    # radio_var의 값에 따라 원하는 동작을 수행합니다.
    global ZABBIX_GLOBAL_URL
    if radio_var.get() == 1:
        ZABBIX_GLOBAL_URL = COMMON

    if radio_var.get() == 2:
        ZABBIX_GLOBAL_URL = GAME

# 초기에는 두 번째 윈도우가 없으므로 None으로 초기화
second_window = None
# 두 번째 윈도우를 띄우는 함수
def zabbix_group_maintenance_window():
    global e3, e4, e5, e6, second_window
    
    if second_window is None or not second_window.winfo_exists():
        second_window = tk.Toplevel()  # 새로운 창 열기
        # 새로운 창에 대한 설정 및 내용 추가
    else:
        second_window.lift()  # 이미 열려 있는 창을 활성화
    second_window.title("Zabbix Maintenance 설정")

    L3 = ttk.Label(second_window, text = "Maintenance 제목 :")
    L3.grid(row =0, column = 0)

    e3 = ttk.Entry(second_window, width = 30)
    e3.grid(row = 0, column = 1)

    TitleLabel = ttk.Label(second_window, text = " ex) 2022-01-01 15:00 ")     # %Y-%m-%d %H:%M 
    TitleLabel.grid(row = 1, column = 1)

    L4 = ttk.Label(second_window, text = "Maintenance 시작 시간 :")
    L4.grid(row =2, column = 0)

    e4 = ttk.Entry(second_window, width = 30)
    e4.grid(row = 2, column = 1)

    L5 = ttk.Label(second_window, text = "Maintenance 종료 시간 :")
    L5.grid(row = 3, column = 0)

    e5 = ttk.Entry(second_window, width = 30)
    e5.grid(row = 3, column = 1)

    
    hostLabel = ttk.Label(second_window, text = "ex) CDB_NP CDB_MINIBUS ")     # space 구분 
    hostLabel.grid(row = 4, column = 1)

    L6 = ttk.Label(second_window, text = "Host Group Name :")
    L6.grid(row = 5, column = 0)

    e6 = ttk.Entry(second_window, width = 30)
    e6.grid(row = 5, column = 1)

    btn = ttk.Button(second_window, text = "Submit Answers", command = create_zabbix_maintenance)
    btn.grid(row = 6, column = 1)

    second_window.mainloop()

def main():
    global tree, radio_var, root
    # 메인 애플리케이션 GUI 설정
    root = tk.Tk()
    root.title("Zabbix 호스트 관리")
    root.geometry("800x400")  # 기존보다 너비를 늘려서 버튼을 수용합니다.

    frame_top = tk.Frame(root)
    # frame_top.pack(expand=True, fill='both')  
    frame_top.pack(expand=False, fill='x', side='top', padx=10, pady=10)

    # 라디오 버튼을 위한 프레임 생성 및 배치
    radio_frame = tk.Frame(frame_top)
    radio_frame.grid(row=4, column=1)  # columnspan을 사용하여 라디오 버튼들이 차지하는 공간을 조정합니다.

    # 라디오 버튼을 위한 변수
    radio_var = tk.IntVar()
    radio_var.trace_add("write", radio_changed)

    # 라디오 버튼 1
    radio_button1 = tk.Radiobutton(radio_frame, text="Zabbix Common", variable=radio_var, value=1)
    radio_button1.pack(side='left', padx=5)  # radio_frame 내부에서는 pack 사용

    # 라디오 버튼 2
    radio_button2 = tk.Radiobutton(radio_frame, text="Zabbix Game", variable=radio_var, value=2)
    radio_button2.pack(side='left', padx=5)  # radio_frame 내부에서는 pack 사용

    # 파일 열기 버튼
    open_file_button = tk.Button(frame_top, text="파일 열기", command=load_file, width=15)
    open_file_button.grid(row=4, column=2)

    # 선택된 호스트 삭제 버튼
    delete_button = tk.Button(frame_top, text="선택된 호스트 삭제", command=lambda: tree.delete_selected_host(), width=15)
    delete_button.grid(row=4, column=3)

    # reset 버튼
    reset_button = tk.Button(frame_top, text="초기화", command=lambda: tree.delete_all_hosts(), width=15)
    reset_button.grid(row=4, column=4)

    # Label = tk.Label(frame_top, "12312")
    # Label.grid(row=4, column=5)

    # Middle 프레임
    frame_middle = tk.Frame(root)
    frame_middle.pack(expand=True, fill='both')

    tree = CheckableTreeview(frame_middle, show='tree headings')
    tree.pack(expand=True, fill='both')  

    
    # 하단 프레임 (Grid 사용)
    frame_bot = tk.Frame(root)
    frame_bot.pack(side="bottom")

    # 체크된 항목 수를 표시할 라벨 생성 및 배치
    tree.checked_count_label = tk.Label(frame_bot, text="체크된 항목 수: 0")
    # 로드된 호스트 수를 표시할 라벨
    host_count_label = tk.Label(frame_bot, text="")
    tree.set_host_count_label(host_count_label)


    # 확인 및 API 호출 버튼
    confirm_button = tk.Button(frame_bot, text="Host 정보 확인", command=confirm_and_call_api, width=15)
    # confirm_button.pack(pady=10)
    get_hosts_Info_button = tk.Button(frame_bot, text="Host 정보 가져오기", command=get_host_ips, width=15)

    # 활성화 및 비활성화 버튼 추가
    activate_button = tk.Button(frame_bot, text="Zabbix Host 활성화", command=activate_selected_hosts,width=20)
    # activate_button.pack(side=tk.LEFT, padx=10, pady=5)

    deactivate_button = tk.Button(frame_bot, text="Zabbix Host 비활성화", command=deactivate_selected_hosts, width=20)
    # deactivate_button.pack(side=tk.RIGHT, padx=10, pady=5)

    delete_button = tk.Button(frame_bot, text="Zabbix Host 삭제", command=delete_selected_hosts_api, width=15)

    
    second_window_button = tk.Button(frame_bot, text="Zabbix maintenance ", command=zabbix_group_maintenance_window, width=20)



    host_count_label.grid(row=3, column=2) 
    tree.checked_count_label.grid(row=3, column=4)

    confirm_button.grid(row=4, column=1)
    get_hosts_Info_button.grid(row=4, column=2)
    activate_button.grid(row=4, column=3)
    deactivate_button.grid(row=4, column=4)
    delete_button.grid(row=4, column=5)
    second_window_button.grid(row=4, column=6)

    root.mainloop()

if __name__ == "__main__":
    main()


