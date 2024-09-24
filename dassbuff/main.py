import tkinter as tk
from tkinter import ttk
import json
import bastPricetSellSkin86
import time
import os
import config
from datetime import datetime
import threading


exchange_rate=7.10

def initFile():
    print("文件初始化")
    if not os.path.exists(config.data_local):
        os.makedirs(config.data_local)

    if not os.path.exists(config.data_local_excel):
        os.makedirs(config.data_local_excel)

    if not os.path.exists(config.data_local_analysis):
        os.makedirs(config.data_local_analysis)

    exchange_rate=bastPricetSellSkin86.find_us_exchange()
    print("当前的美元汇率是："+str(exchange_rate))



    


class TabbedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed Application")

        # 创建一个标签框架
        self.tabControl = ttk.Notebook(self.root)
        self.task = ScheduledTask(interval=5)

        # 创建多个标签页
        self.create_tab1()
        self.create_tab2()

        # 将标签框架添加到窗口
        self.tabControl.pack(expand=1, fill="both")
        root.grid_rowconfigure(0, weight=1)  # 设置行权重为1，使得 Treeview 可以伸缩
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.task.stop()
        self.root.destroy()
        
    

    def create_tab1(self):
        tab1 = ttk.Frame(self.tabControl,width=1200,height=800)
        self.tabControl.add(tab1, text='国内数据')

        # 查询部分
        query_label = tk.Label(tab1, text="查询内容平台:")
        query_label.grid(row=0,columnspan=2, column=0)

        sync_query = tk.Entry(tab1,width=30)
        sync_query.insert(0, "1,1,10,0.5,200,100")
        sync_query.grid(row=1, column=0,sticky=tk.E,padx=30)
        sync_button = tk.Button(tab1, text="同步数据",width=15, command=lambda: sync_data(sync_query.get(), sync_button))
        sync_button.grid(row=1,  column=1,sticky=tk.W)

        sync_query_time = tk.Entry(tab1,width=30)
        sync_query_time.insert(0, "1")
        sync_query_time.grid(row=2, column=0,sticky=tk.E,padx=30)
        start_button_time = tk.Button(tab1, text="定时同步",width=15, command=lambda: start_data_timer(sync_query.get(),sync_query_time.get(), stop_button_time,start_button_time,self.task))
        start_button_time.grid(row=2,  column=1,sticky=tk.W)

        stop_query_time = tk.Entry(tab1,width=30)
        stop_query_time.insert(0, "1")
        stop_query_time.grid(row=3, column=0,sticky=tk.E,padx=30)
        stop_button_time = tk.Button(tab1, text="暂停同步",width=15, command=lambda: stop_data_timer(sync_query.get(),sync_query_time.get(), stop_button_time,start_button_time,self.task))
        stop_button_time.grid(row=3,  column=1,sticky=tk.W)


        search_min_button = tk.Button(tab1, text="查询采购最低价",width=15, command=lambda: search_min_data(None,self.tree1))
        search_min_button.grid(row=4,  column=0,sticky=tk.E,padx=30)
        buy_min_button = tk.Button(tab1, text="采购最低价",width=15, command=lambda: buy_min_data(None,self.tree1))
        buy_min_button.grid(row=4,  column=1,sticky=tk.W)


        search_avg_button = tk.Button(tab1, text="查询采购平均价",width=15, command=lambda: search_avg_data(None,self.tree1))
        search_avg_button.grid(row=5, column=0,sticky=tk.E,padx=30)
        buy_avg_button = tk.Button(tab1, text="采购平均价",width=15, command=lambda: buy_avg_data(None,self.tree1))
        buy_avg_button.grid(row=5, column=1,sticky=tk.W)

        




        # 列表展示部分
        self.tree1 = ttk.Treeview(tab1, height=25, selectmode="browse",columns=("drtitle", "title","totalSales", "date","offer_price", "target_price","buff_avg_price","dm_buy_buff_sale_avg","dm_buy_buff_sale_avg_rate","dm_buy_buff_sale_min","dm_buy_buff_sale_min_rate","price_alter_percentage_7d","price_alter_value_7d","category_group_name"), show='headings')
        # 创建滚动条
        col_width = 75
        self.tree1.column("drtitle", width=60, anchor='center')
        self.tree1.column("title", width=120, anchor='center')
        self.tree1.column("totalSales", width=40, anchor='center')
        self.tree1.column("date", width=col_width, anchor='center')
        self.tree1.column("offer_price", width=col_width, anchor='center')
        self.tree1.column("target_price", width=col_width, anchor='center')
        self.tree1.column("buff_avg_price", width=col_width, anchor='center')
        self.tree1.column("dm_buy_buff_sale_avg", width=col_width, anchor='center')
        self.tree1.column("dm_buy_buff_sale_avg_rate", width=col_width, anchor='center')
        self.tree1.column("dm_buy_buff_sale_min", width=col_width, anchor='center')
        self.tree1.column("dm_buy_buff_sale_min_rate", width=col_width, anchor='center')
        self.tree1.column("price_alter_percentage_7d", width=col_width, anchor='center')
        self.tree1.column("price_alter_value_7d", width=col_width, anchor='center')
        self.tree1.column("category_group_name", width=col_width, anchor='center')

        self.tree1.heading("drtitle", text="英文名称")
        self.tree1.heading("title", text="名称")
        self.tree1.heading("totalSales", text="销售数量")
        self.tree1.heading("date", text="日期")
        self.tree1.heading("offer_price", text="平均购买价")
        self.tree1.heading("target_price", text="当前出售价")
        self.tree1.heading("buff_avg_price", text="buff在售价")
        self.tree1.heading("dm_buy_buff_sale_avg", text="dm购买buff出售-平均价")
        self.tree1.heading("dm_buy_buff_sale_avg_rate", text="dm购买buff出售-平均价率")
        self.tree1.heading("dm_buy_buff_sale_min", text="dm购买buff出售-当前价")
        self.tree1.heading("dm_buy_buff_sale_min_rate", text="dm购买buff出售-当前价率")
        self.tree1.heading("price_alter_percentage_7d", text="7天变化率")
        self.tree1.heading("price_alter_value_7d", text="7天变化价格")
        self.tree1.heading("category_group_name", text="饰品类型")
        # self.tree1.pack(side=tk.LEFT,pady=40,expand=1, fill="both")
        self.display_data1(None, self.tree1)

         # 创建水平滚动条
        x_scroll = ttk.Scrollbar(tab1, orient="horizontal", command=self.tree1.xview)
        y_scroll = ttk.Scrollbar(tab1, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(xscrollcommand=x_scroll.set)
        self.tree1.configure(yscrollcommand=y_scroll.set)

        # 布局
        self.tree1.grid(row=6,columnspan=2,sticky=tk.NS,padx=30,pady=30)



    def create_tab2(self):
        tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(tab2, text='查询页面 2')

       


    def display_data1(self, query, tree):
        print("显示数据")
      

    

def search_min_data(query, tree):
    print("采购最低价")
    create_target_list=bastPricetSellSkin86.create_avg_target_min(exchange_rate)
    if create_target_list is None or len(create_target_list)==0 :
        print("没有数据")
        return
    
    # 清空之前的数据
    for item in tree.get_children():
        tree.delete(item)
            # 将新的数据插入到表格中

    for entry in create_target_list:
        if query is None:
            tree.insert("", "end", values=(entry["drtitle"],entry["title"], entry["totalSales"], entry["date"], entry["offer_price"], entry["target_price"], entry["buff_avg_price"], entry["dm_buy_buff_sale_avg"], entry["dm_buy_buff_sale_avg_rate"], entry["dm_buy_buff_sale_min"], entry["dm_buy_buff_sale_min_rate"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
        elif query in entry["drtitle"] or query in entry["title"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
            tree.insert("", "end", values=(entry["drtitle"],entry["title"], entry["totalSales"], entry["date"], entry["offer_price"], entry["target_price"], entry["buff_avg_price"], entry["dm_buy_buff_sale_avg"], entry["dm_buy_buff_sale_avg_rate"], entry["dm_buy_buff_sale_min"], entry["dm_buy_buff_sale_min_rate"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
    
    

def buy_min_data( query,tree):
    print("开始采购")
    create_target_list=bastPricetSellSkin86.create_avg_target_min(exchange_rate)
    filename=config.data_local_excel+"/creat_target_min_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    bastPricetSellSkin86.creat_now(create_target_list,filename,100,"min")


def search_avg_data( query,tree):
    print("查询平均价")
    create_avg_target_list=bastPricetSellSkin86.create_avg_target_avg(exchange_rate)
    if create_avg_target_list is None or len(create_avg_target_list)==0 :
        print("没有数据")
        return
    # 清空之前的数据
    for item in tree.get_children():
        tree.delete(item)
            # 将新的数据插入到表格中

    for entry in create_avg_target_list:
        if query is None:
            tree.insert("", "end", values=(entry["drtitle"],entry["title"], entry["totalSales"], entry["date"], entry["offer_price"], entry["target_price"], entry["buff_avg_price"], entry["dm_buy_buff_sale_avg"], entry["dm_buy_buff_sale_avg_rate"], entry["dm_buy_buff_sale_min"], entry["dm_buy_buff_sale_min_rate"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
        elif query in entry["drtitle"] or query in entry["title"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
            tree.insert("", "end", values=(entry["drtitle"],entry["title"], entry["totalSales"], entry["date"], entry["offer_price"], entry["target_price"], entry["buff_avg_price"], entry["dm_buy_buff_sale_avg"], entry["dm_buy_buff_sale_avg_rate"], entry["dm_buy_buff_sale_min"], entry["dm_buy_buff_sale_min_rate"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
    


def buy_avg_data( query,tree):
    print("购买平均价")
    create_avg_target_list=bastPricetSellSkin86.create_avg_target_avg(exchange_rate)
    filename=config.data_local_excel+"/creat_target_avg_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    bastPricetSellSkin86.creat_now(create_avg_target_list,filename,50,"avg")



def start_data_timer(search_content, timer,stop_button_time,start_button_time,task):
      # 每 5 秒执行一次任务
    start_button_time.config(state=tk.DISABLED)
    task.start()
    stop_button_time.config(state=tk.NORMAL)


def stop_data_timer(search_content, timer,stop_button_time,start_button_time,task):
    stop_button_time.config(state=tk.DISABLED)
    task.stop()
    start_button_time.config(state=tk.NORMAL)
    


def testTimer(search_content):
    print("开始同步")
    while True:
        time.sleep(1)
        print("定时同步中："+search_content)


class ScheduledTask:
    def __init__(self, interval):
        self.interval = interval  # 任务执行间隔（秒）
        self.stop_event = threading.Event()  # 用于停止任务的事件
        self.thread = None

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()  # 清除停止事件
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
            print(f"任务已开始，每 {self.interval} 秒执行一次。")

    def run(self):
        while not self.stop_event.is_set():
            self.execute_task()  # 执行任务
            time.sleep(self.interval)  # 等待指定时间

    def execute_task(self):
        print("执行任务...")  # 这里可以替换为实际的任务逻辑

    def stop(self):
        self.stop_event.set()  # 设置停止事件
        if self.thread is not None:
            self.thread.join()  # 等待线程结束
        print("任务已停止。")


def sync_data(search_content, sync_button):    
    # 修改按钮名称为同步中 
    # 500,1,100,0.5,200,100
    sync_button.config(state=tk.DISABLED)
    query_content = search_content.split(",")
    limit_page=int(query_content[0])
    page=int(query_content[1])
    page_size=int(query_content[2])
    price_start=float(query_content[3])
    price_end=float(query_content[4])
    selling_num_start=int(query_content[5])

    bastPricetSellSkin86.sync_data(limit_page,page,page_size,price_start,price_end,selling_num_start)
    sync_button.config(state=tk.NORMAL,text="同步")
    print("同步结束")

    
if __name__ == "__main__":
    initFile()
    root = tk.Tk()
    root.geometry("1200x800")
    app = TabbedApp(root)
    root.mainloop()