from math import e
from re import L
import tkinter as tk
from tkinter import ttk
import bastPricetSellSkin86
import os
import config
from datetime import datetime
import soccerbenefit
import log_utils
import httpUtils
import soccerBet
import log_utils
import time


exchange_rate=7.10

def initFile():
    print("文件初始化")
    if not os.path.exists(config.data_local):
        os.makedirs(config.data_local)

    if not os.path.exists(config.data_local_excel):
        os.makedirs(config.data_local_excel)

    if not os.path.exists(config.data_local_analysis):
        os.makedirs(config.data_local_analysis)

    # if os.path.exists(config.log_file):
    #     os.remove(config.log_file)
    #     os.makedirs(config.log_file)

    global  exchange_rate
    exchange_rate=bastPricetSellSkin86.find_us_exchange()
    print("当前的美元汇率是："+str(exchange_rate))


 


class TabbedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed Application")

        # 创建一个标签框架
        self.tabControl = ttk.Notebook(self.root)
        # 创建多个标签页
        self.create_tab0()
       

        # 将标签框架添加到窗口
        self.tabControl.pack(expand=1, fill="both")
        root.grid_rowconfigure(0, weight=1)  # 设置行权重为1，使得 Treeview 可以伸缩
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
        

    def on_closing(self):
        import threading
        import sys

        print("正在关闭程序，尝试关闭所有线程...")

        # 获取当前所有活动线程
        threads = threading.enumerate()
        main_thread = threading.current_thread()

        # 通知所有非主线程退出（如果有自定义线程可加退出标志）
        for t in threads:
            if t is not main_thread:
                try:
                    # 如果线程有自定义的stop/exit方法，可以调用
                    if hasattr(t, "stop"):
                        t.stop()
                    elif hasattr(t, "terminate"):
                        t.terminate()
                except Exception as e:
                    print(f"关闭线程{t.name}时出错: {e}")

        # 强制退出程序
        self.root.destroy()
        sys.exit(0)
     
        
        
    def create_tab0(self):
        tab0 = ttk.Frame(self.tabControl, width=1200, height=800)
        self.tabControl.add(tab0, text='首页-其他汇总')
        # 展示3行，每行有1个按钮、1个文本框和1个上下滑动的大文本框，按钮用来触发某个功能，文本框用来输入参数，大文本框用来展示执行过程中的日志信息
        self.tab0_scroll_boxes = []  # 保存每行的日志框，便于后续访问

        # 设置grid列权重，使日志框只占1/3且靠右
        tab0.grid_columnconfigure(0, weight=1)
        tab0.grid_columnconfigure(1, weight=1)
        tab0.grid_columnconfigure(2, weight=1)  # 日志框所在列
        tab0.grid_rowconfigure(0, weight=1)
        tab0.grid_rowconfigure(1, weight=1)
        tab0.grid_rowconfigure(2, weight=1)

        # 创建日志框，只创建一次，宽度设置小一些以适应1/3页面
        scroll_box = tk.Text(tab0, width=40, height=45, wrap="word")
        scroll_box.grid(row=0, column=3, rowspan=3, sticky=tk.NSEW, padx=30, pady=10)
        scroll_box.configure(state=tk.DISABLED)
        scroll_box.insert(tk.END, "日志信息\n")
        self.tab0_scroll_boxes.append(scroll_box)

        import threading

        def update_log_box():
            import os
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_file_name = f"main-{datetime.now().strftime('%Y%m%d')}.log"
            log_file_path = os.path.join(base_dir, "log/"+log_file_name)

            try:
                # 如果日志文件不存在，则创建该文件
                if not os.path.exists(log_file_path):
                    # 确保目录存在
                    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
                    with open(log_file_path, "w", encoding="utf-8") as f_create:
                        f_create.write("日志文件已创建。\n")
                with open(log_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    last_100_lines = lines[-100:] if len(lines) > 100 else lines
                    log_text = "".join(last_100_lines)
            except Exception as e:
                log_text = f"日志读取失败: {e}\n"
            scroll_box.configure(state=tk.NORMAL)
            scroll_box.delete(1.0, tk.END)
            scroll_box.insert(tk.END, log_text)
            scroll_box.see(tk.END)
            scroll_box.configure(state=tk.DISABLED)
            # 每隔1秒刷新一次
            scroll_box.after(1000, update_log_box)

        # 启动日志自动刷新
        update_log_box()

        # 创建三行，每行一个按钮和一个可自定义长宽高的文本框
        # 先创建一个列表保存每个text_box的引用
        self.tab0_text_boxes = []
        for i in range(3):
            # 创建按钮，并绑定事件处理方法
            button_title = "开始bet"

            # 这里将Entry替换为Text，并允许自定义宽高
            text_box = tk.Text(tab0, width=60, height=15)
            text_box.grid(row=i, column=2, sticky=tk.W, padx=30)
            self.tab0_text_boxes.append(text_box)

            if i == 2:
                button_title = "同步历史"
                # 填充text_box的默认值
                text_box.insert(tk.END, "3,1,10")

            button = tk.Button(tab0, text=button_title+str(i+1), width=15, command=lambda idx=i: tab0_button_command(idx))
            button.grid(row=i, column=0, sticky=tk.W, padx=30)

            button = tk.Button(tab0, text=button_title+"停止"+str(i+1), width=15, command=lambda idx=i: tab0_button_stop(idx))
            button.grid(row=i, column=1, sticky=tk.W, padx=30)

        
            
# 单独定义按钮点击事件方法
        def tab0_button_command(idx):
            # 获取对应text_box的内容
            text_box_value = self.tab0_text_boxes[idx].get("1.0", tk.END).strip()
            log_msg = f"按钮{idx+1}被点击，输入框内容为：{text_box_value}\n"
            print(log_msg)


            if idx == 0:
                domain_cookie = httpUtils.parse_curl_to_params(text_box_value)
                print(domain_cookie)
                threading.Thread(target=soccerbenefit.receive_all_bonus_action, args=(domain_cookie,)).start()
                print("按钮执行结束11")
            if idx == 1:
                domain_cookie2 = httpUtils.parse_curl_to_params_bet(text_box_value)
                print(domain_cookie2)
                threading.Thread(target=soccerBet.startBetSoccer, args=(domain_cookie2,)).start()
                print("按钮执行结束2")
            if idx == 2:
                text_box_value2 = self.tab0_text_boxes[1].get("1.0", tk.END).strip()
                domain_cookie2 = httpUtils.parse_curl_to_params_bet(text_box_value2)

                limit_page = text_box_value.split(",")[0]
                page = text_box_value.split(",")[1]
                page_size = text_box_value.split(",")[2]
                soccerBet.updateMyBetHistoryList(domain_cookie2,int(limit_page),int(page),int(page_size))
                print("按钮执行结束3")
        
        def tab0_button_stop(idx):
            # 获取当前主线程
            main_thread = threading.main_thread()
            # 遍历所有活动线程
            for t in threading.enumerate():
                # 跳过主线程
                if t is main_thread:
                    continue
                try:
                    # 线程对象没有直接的终止方法，这里采用强制退出进程的方式
                    # 只要有非主线程存在就强制退出整个进程
                    print(f"中断线程: {t.name}")
                    os._exit(0)
                except Exception as e:
                    print(f"中断线程失败: {e}")


if __name__ == "__main__":
    initFile()
    start_time=int(time.time())
    log_file_name = f"main-{datetime.now().strftime('%Y%m%d')}"
    print("开始运行",log_file_name)
    log_utils.init_logger(log_file_name)
    root = tk.Tk()
    root.geometry("1200x800")
    app = TabbedApp(root)
    root.mainloop()