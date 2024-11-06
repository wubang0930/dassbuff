import tkinter as tk
from tkinter import ttk
import json
import bastPricetSellSkin86
import time
import os
import config
from datetime import datetime
import threading
import offer_sell_product
import pyperclip  # 用于复制到剪贴板
import bastPricetMyBuy


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



class ScheduledTask:
    def __init__(self, interval):
        self.interval = int(interval)*60*60  # 任务执行间隔（小时）
        self.stop_event = threading.Event()  # 用于停止任务的事件
        self.thread = None

    def start(self,search_content,sync_button,public_key,secret_key):
        now = datetime.now()
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()  # 清除停止事件
            self.thread = threading.Thread(target=self.run, args=(search_content,sync_button,public_key,secret_key))
            self.thread.daemon = True
            self.thread.start()
            print(str(now)+f"任务已开始，每 {self.interval/3600} 小时执行一次。")

    def run(self,search_content,sync_button,public_key,secret_key):
        while not self.stop_event.is_set():
            self.execute_task(search_content,sync_button,public_key,secret_key)  # 执行任务
            time.sleep(self.interval)  # 等待指定时间

    def execute_task(self,search_content,sync_button,public_key,secret_key):
        now = datetime.now()
        print(str(now)+"：执行定时任务..."+search_content)  # 这里可以替换为实际的任务逻辑
        timer_task_buy_min_data( search_content,sync_button,public_key,secret_key)


    def stop(self,sync_button):
        sync_button.config(state=tk.NORMAL)
        self.stop_event.set()  # 设置停止事件
        print("任务已停止。")

 


class TabbedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed Application")

        # 创建一个标签框架
        self.tabControl = ttk.Notebook(self.root)
        # 创建多个标签页
        self.create_tab1()
        self.create_tab1_2()
        self.create_tab2_1()
        self.create_tab2_2()
        self.create_tab3()

        # 将标签框架添加到窗口
        self.tabControl.pack(expand=1, fill="both")
        root.grid_rowconfigure(0, weight=1)  # 设置行权重为1，使得 Treeview 可以伸缩
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
        

    def on_closing(self):
        self.task_min.stop(self.sync_button_one)
        self.root.destroy()
        
    

    def create_tab1(self):
        tab1 = ttk.Frame(self.tabControl,width=1200,height=800)
        self.tabControl.add(tab1, text='DM购买后BUFF出售-账号1')

        # 查询部分
        query_label = tk.Label(tab1, text="查询内容平台:")
        query_label.grid(row=0,columnspan=3, column=0)

        defualt_query = "300,1,100,1,15,200,YP"
        sync_query_one = tk.Entry(tab1,width=30)
        sync_query_one.insert(0, "8")
        sync_query_one.grid(row=1, column=0,sticky=tk.E,padx=30)
        sync_query = tk.Entry(tab1,width=30)
        sync_query.insert(0, defualt_query)
        sync_query.grid(row=1, column=1,sticky=tk.W,padx=30)
        sync_button = tk.Button(tab1, text="同步数据",width=15, command=lambda: sync_data(sync_query.get(), sync_button))
        sync_button.grid(row=1,  column=2,sticky=tk.W)
        self.sync_button_one=sync_button

        self.task_min = ScheduledTask(interval=sync_query_one.get())
        


        sync_query_time = tk.Entry(tab1,width=30,state=tk.DISABLED)
        sync_query_time.insert(0, defualt_query)
        sync_query_time.grid(row=2, column=0,sticky=tk.E,padx=30)
        start_button_time = tk.Button(tab1, text="定时采购最低价",width=15, command=lambda: start_data_timer(sync_query.get(),stop_button_time,start_button_time,self.task_min,sync_button,config.dmarket_public_key,config.dmarket_secret_key))
        start_button_time.grid(row=2,  column=1,sticky=tk.W,padx=30)
        stop_button_time = tk.Button(tab1, text="暂停采购最低价",width=15, command=lambda: stop_data_timer(sync_query.get(), stop_button_time,start_button_time,self.task_min,sync_button,config.dmarket_public_key,config.dmarket_secret_key))
        stop_button_time.grid(row=2,  column=2,sticky=tk.W)
        stop_button_time.config(state=tk.DISABLED)


        search_min_button_query = tk.Entry(tab1,width=30)
        search_min_button_query.insert(0, "")
        search_min_button_query.grid(row=3, column=0,sticky=tk.E,padx=30)
        search_min_button = tk.Button(tab1, text="查询采购最低价",width=15, command=lambda: search_min_data(search_min_button_query.get(),self.tree1))
        search_min_button.grid(row=3,  column=1,sticky=tk.W,padx=30)
        buy_min_button = tk.Button(tab1, text="采购最低价",width=15, command=lambda: buy_min_data(search_min_button_query.get(),config.dmarket_public_key,config.dmarket_secret_key))
        buy_min_button.grid(row=3,  column=2,sticky=tk.W)


        search_avg_query = tk.Entry(tab1,width=30)
        search_avg_query.insert(0, "")
        search_avg_query.grid(row=4, column=0,sticky=tk.E,padx=30)
        search_avg_button = tk.Button(tab1, text="查询采购平均价",width=15, command=lambda: search_avg_data(search_avg_query.get(),self.tree1))
        search_avg_button.grid(row=4, column=1,sticky=tk.W,padx=30)
        buy_avg_button = tk.Button(tab1, text="采购平均价",width=15, command=lambda: buy_avg_data(search_avg_query.get(),self.tree1,config.dmarket_public_key,config.dmarket_secret_key))
        buy_avg_button.grid(row=4, column=2,sticky=tk.W)

        




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
        self.tree1.grid(row=5,columnspan=3,sticky=tk.NS,padx=30,pady=30)

    def create_tab1_2(self):
        tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(tab2, text='悠悠购买DM出售-账号1')

        # 查询部分
        query_label_inve = tk.Label(tab2, text="库存平台:")
        query_label_inve.grid(row=0,columnspan=4, column=0)



        sync_query_time_add_1_2 = tk.Entry(tab2,width=30)
        sync_query_time_add_1_2.grid(row=1, column=0,sticky=tk.E,padx=30)
        sync_query_time_add_1_2_limit = tk.Entry(tab2,width=30)
        sync_query_time_add_1_2_limit.insert(0, "100")
        sync_query_time_add_1_2_limit.grid(row=1, column=1,sticky=tk.E,padx=30)
        start_button_time_add_1_2 = tk.Button(tab2, text="查询提现购物车",width=15, command=lambda: add_task_to_steam_cart(sync_query_time_add_1_2.get(),sync_query_time_add_1_2_limit.get(),self.tree_1_2,"itemLocation[]=true,tradeLockTo[]=0",count_label_1_2_value,count_label_1_2_value_all,config.authorization))
        start_button_time_add_1_2.grid(row=1,  column=2,sticky=tk.W,padx=30)
        stop_button_time_add_1_2 = tk.Button(tab2, text="确认提现",width=15, command=lambda: confirm_task_to_steam_cart(config.authorization))
        stop_button_time_add_1_2.grid(row=1,  column=3,sticky=tk.W)


        sync_query_time_sale_1_2 = tk.Entry(tab2,width=30)
        sync_query_time_sale_1_2.grid(row=2, column=0,sticky=tk.E,padx=30)
        sync_query_time_sale_1_2_limit = tk.Entry(tab2,width=30)
        sync_query_time_sale_1_2_limit.insert(0, "100")
        sync_query_time_sale_1_2_limit.grid(row=2, column=1,sticky=tk.E,padx=30)
        start_button_time_sale_1_2 = tk.Button(tab2, text="查询出售购物车",width=15, command=lambda: add_task_to_steam_cart(sync_query_time_sale_1_2.get(),sync_query_time_sale_1_2_limit.get(),self.tree_1_2,"itemLocation[]=false,tradeLockTo[]=0",count_label_1_2_value,count_label_1_2_value_all,config.authorization))
        start_button_time_sale_1_2.grid(row=2,  column=2,sticky=tk.W,padx=30)
        stop_button_time_sale_1_2 = tk.Button(tab2, text="确认出售购物车",width=15, command=lambda: confirm_task_to_sale_cart(config.authorization))
        stop_button_time_sale_1_2.grid(row=2,  column=3,sticky=tk.W)
        

        sync_query_time_change_1_2 = tk.Entry(tab2,width=30)
        sync_query_time_change_1_2.grid(row=3, column=0,sticky=tk.E,padx=30)
        sync_query_time_change_1_2_limit = tk.Entry(tab2,width=30)
        sync_query_time_change_1_2_limit.insert(0, "100")
        sync_query_time_change_1_2_limit.grid(row=3, column=1,sticky=tk.E,padx=30)
        start_button_time_change_1_2 = tk.Button(tab2, text="查询出售中数据",width=15, command=lambda: add_task_to_change_cart(sync_query_time_change_1_2.get(),sync_query_time_change_1_2_limit.get(),self.tree_1_2,count_label_1_2_value,count_label_1_2_value_all,config.authorization))
        start_button_time_change_1_2.grid(row=3,  column=2,sticky=tk.W,padx=30)
        stop_button_time_change_1_2 = tk.Button(tab2, text="确认出售中数据",width=15, command=lambda: confirm_task_to_change_cart(config.authorization))
        stop_button_time_change_1_2.grid(row=3,  column=3,sticky=tk.W)
        

        count_label_1_2 = tk.Label(tab2, text="当前条数:")
        count_label_1_2.grid(row=4,column=0,sticky=tk.E,padx=30,pady=30)
        count_label_1_2_value = tk.Entry(tab2,width=30)
        count_label_1_2_value.grid(row=4, column=1,sticky=tk.E,padx=30,pady=30)
        count_label_1_2_all = tk.Label(tab2, text="总条数:")
        count_label_1_2_all.grid(row=4,column=2,sticky=tk.W,padx=30,pady=30)
        count_label_1_2_value_all = tk.Entry(tab2,width=30)
        count_label_1_2_value_all.grid(row=4, column=3,sticky=tk.W,pady=30)
        
        # 列表展示部分
        self.tree_1_2 = ttk.Treeview(tab2, height=25, selectmode="browse",columns=("id", "title", "gameType", "price", "instantPrice"), show='headings')
        # 创建滚动条
        self.tree_1_2.column("id", width=300, anchor='center')
        self.tree_1_2.column("title", width=300, anchor='center')
        self.tree_1_2.column("gameType", width=150, anchor='center')
        self.tree_1_2.column("price", width=150, anchor='center')
        self.tree_1_2.column("instantPrice", width=150, anchor='center')

        self.tree_1_2.heading("id", text="英文名称")
        self.tree_1_2.heading("title", text="名称")
        self.tree_1_2.heading("gameType", text="饰品类型")
        self.tree_1_2.heading("price", text="价格")
        self.tree_1_2.heading("instantPrice", text="即时销售价格")
        self.display_data1(None, self.tree_1_2)

        # 布局
        self.tree_1_2.grid(row=6,columnspan=4,sticky=tk.NS,padx=30,pady=10)
        # 绑定行选择事件
        self.tree_1_2.bind("<<TreeviewSelect>>", self.on_row_select_1)

        # 绑定键盘事件（Ctrl+C 复制选中行）
        self.tree_1_2.bind("<Control-c>", self.copy_selection_1)


    def create_tab2_1(self):
        tab1 = ttk.Frame(self.tabControl,width=1200,height=800)
        self.tabControl.add(tab1, text='DM购买后BUFF出售-账号2')

        # 查询部分
        query_label = tk.Label(tab1, text="查询内容平台:")
        query_label.grid(row=0,columnspan=3, column=0)

        defualt_query = "300,1,100,1,15,200,YP"
        sync_query_2_1_one_2_1 = tk.Entry(tab1,width=30)
        sync_query_2_1_one_2_1.insert(0, "8")
        sync_query_2_1_one_2_1.grid(row=1, column=0,sticky=tk.E,padx=30)
        sync_query_2_1 = tk.Entry(tab1,width=30)
        sync_query_2_1.insert(0, defualt_query)
        sync_query_2_1.grid(row=1, column=1,sticky=tk.W,padx=30)
        sync_button_2_1 = tk.Button(tab1, text="同步数据",width=15, command=lambda: sync_data(sync_query_2_1.get(), sync_button_2_1))
        sync_button_2_1.grid(row=1,  column=2,sticky=tk.W)
        self.sync_button_2_1_one=sync_button_2_1

        self.task_min_2_1 = ScheduledTask(interval=sync_query_2_1_one_2_1.get())
        


        sync_query_2_1_time = tk.Entry(tab1,width=30,state=tk.DISABLED)
        sync_query_2_1_time.insert(0, defualt_query)
        sync_query_2_1_time.grid(row=2, column=0,sticky=tk.E,padx=30)
        start_button_time_2_1 = tk.Button(tab1, text="定时采购最低价",width=15, command=lambda: start_data_timer(sync_query_2_1.get(),stop_button_time_2_1,start_button_time_2_1,self.task_min_2_1,sync_button_2_1,config.dmarket_public_key_two,config.dmarket_secret_key_two))
        start_button_time_2_1.grid(row=2,  column=1,sticky=tk.W,padx=30)
        stop_button_time_2_1 = tk.Button(tab1, text="暂停采购最低价",width=15, command=lambda: stop_data_timer(sync_query_2_1.get(), stop_button_time_2_1,start_button_time_2_1,self.task_min_2_1,sync_button_2_1,config.dmarket_public_key_two,config.dmarket_secret_key_two))
        stop_button_time_2_1.grid(row=2,  column=2,sticky=tk.W)
        stop_button_time_2_1.config(state=tk.DISABLED)


        search_min_button_2_1_query_2_1 = tk.Entry(tab1,width=30)
        search_min_button_2_1_query_2_1.insert(0, "")
        search_min_button_2_1_query_2_1.grid(row=3, column=0,sticky=tk.E,padx=30)
        search_min_button_2_1 = tk.Button(tab1, text="查询采购最低价",width=15, command=lambda: search_min_data(search_min_button_2_1_query_2_1.get(),self.tree_2_1))
        search_min_button_2_1.grid(row=3,  column=1,sticky=tk.W,padx=30)
        buy_min_button_2_1 = tk.Button(tab1, text="采购最低价",width=15, command=lambda: buy_min_data(search_min_button_2_1_query_2_1.get(),config.dmarket_public_key_two,config.dmarket_secret_key_two))
        buy_min_button_2_1.grid(row=3,  column=2,sticky=tk.W)


        search_avg_query_2_1 = tk.Entry(tab1,width=30)
        search_avg_query_2_1.insert(0, "")
        search_avg_query_2_1.grid(row=4, column=0,sticky=tk.E,padx=30)
        search_avg_button_2_1 = tk.Button(tab1, text="查询采购平均价",width=15, command=lambda: search_avg_data(search_avg_query_2_1.get(),self.tree_2_1))
        search_avg_button_2_1.grid(row=4, column=1,sticky=tk.W,padx=30)
        buy_avg_button_2_1 = tk.Button(tab1, text="采购平均价",width=15, command=lambda: buy_avg_data(search_avg_query_2_1.get(),self.tree_2_1,config.dmarket_public_key_two,config.dmarket_secret_key_two))
        buy_avg_button_2_1.grid(row=4, column=2,sticky=tk.W)

        




        # 列表展示部分
        self.tree_2_1 = ttk.Treeview(tab1, height=25, selectmode="browse",columns=("drtitle", "title","totalSales", "date","offer_price", "target_price","buff_avg_price","dm_buy_buff_sale_avg","dm_buy_buff_sale_avg_rate","dm_buy_buff_sale_min","dm_buy_buff_sale_min_rate","price_alter_percentage_7d","price_alter_value_7d","category_group_name"), show='headings')
        # 创建滚动条
        col_width = 75
        self.tree_2_1.column("drtitle", width=60, anchor='center')
        self.tree_2_1.column("title", width=120, anchor='center')
        self.tree_2_1.column("totalSales", width=40, anchor='center')
        self.tree_2_1.column("date", width=col_width, anchor='center')
        self.tree_2_1.column("offer_price", width=col_width, anchor='center')
        self.tree_2_1.column("target_price", width=col_width, anchor='center')
        self.tree_2_1.column("buff_avg_price", width=col_width, anchor='center')
        self.tree_2_1.column("dm_buy_buff_sale_avg", width=col_width, anchor='center')
        self.tree_2_1.column("dm_buy_buff_sale_avg_rate", width=col_width, anchor='center')
        self.tree_2_1.column("dm_buy_buff_sale_min", width=col_width, anchor='center')
        self.tree_2_1.column("dm_buy_buff_sale_min_rate", width=col_width, anchor='center')
        self.tree_2_1.column("price_alter_percentage_7d", width=col_width, anchor='center')
        self.tree_2_1.column("price_alter_value_7d", width=col_width, anchor='center')
        self.tree_2_1.column("category_group_name", width=col_width, anchor='center')

        self.tree_2_1.heading("drtitle", text="英文名称")
        self.tree_2_1.heading("title", text="名称")
        self.tree_2_1.heading("totalSales", text="销售数量")
        self.tree_2_1.heading("date", text="日期")
        self.tree_2_1.heading("offer_price", text="平均购买价")
        self.tree_2_1.heading("target_price", text="当前出售价")
        self.tree_2_1.heading("buff_avg_price", text="buff在售价")
        self.tree_2_1.heading("dm_buy_buff_sale_avg", text="dm购买buff出售-平均价")
        self.tree_2_1.heading("dm_buy_buff_sale_avg_rate", text="dm购买buff出售-平均价率")
        self.tree_2_1.heading("dm_buy_buff_sale_min", text="dm购买buff出售-当前价")
        self.tree_2_1.heading("dm_buy_buff_sale_min_rate", text="dm购买buff出售-当前价率")
        self.tree_2_1.heading("price_alter_percentage_7d", text="7天变化率")
        self.tree_2_1.heading("price_alter_value_7d", text="7天变化价格")
        self.tree_2_1.heading("category_group_name", text="饰品类型")
        # self.tree_2_1.pack(side=tk.LEFT,pady=40,expand=1, fill="both")
        self.display_data1(None, self.tree_2_1)

         # 创建水平滚动条
        x_scroll = ttk.Scrollbar(tab1, orient="horizontal", command=self.tree_2_1.xview)
        y_scroll = ttk.Scrollbar(tab1, orient="vertical", command=self.tree_2_1.yview)
        self.tree_2_1.configure(xscrollcommand=x_scroll.set)
        self.tree_2_1.configure(yscrollcommand=y_scroll.set)

        # 布局
        self.tree_2_1.grid(row=5,columnspan=3,sticky=tk.NS,padx=30,pady=30)


    def create_tab2_2(self):
        tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(tab2, text='悠悠购买DM出售-账号2')

        # 查询部分
        query_label_inve = tk.Label(tab2, text="库存平台:")
        query_label_inve.grid(row=0,columnspan=4, column=0)



        sync_query_time_add = tk.Entry(tab2,width=30)
        sync_query_time_add.grid(row=1, column=0,sticky=tk.E,padx=30)
        sync_query_time_add_limit = tk.Entry(tab2,width=30)
        sync_query_time_add_limit.insert(0, "100")
        sync_query_time_add_limit.grid(row=1, column=1,sticky=tk.E,padx=30)
        start_button_time_add = tk.Button(tab2, text="查询提现购物车",width=15, command=lambda: add_task_to_steam_cart(sync_query_time_add.get(),sync_query_time_add_limit.get(),self.tree2,"itemLocation[]=true,tradeLockTo[]=0",count_label_value,count_label_value_all,config.authorization_two))
        start_button_time_add.grid(row=1,  column=2,sticky=tk.W,padx=30)
        stop_button_time_add = tk.Button(tab2, text="确认提现",width=15, command=lambda: confirm_task_to_steam_cart())
        stop_button_time_add.grid(row=1,  column=3,sticky=tk.W)


        sync_query_time_sale = tk.Entry(tab2,width=30)
        sync_query_time_sale.grid(row=2, column=0,sticky=tk.E,padx=30)
        sync_query_time_sale_limit = tk.Entry(tab2,width=30)
        sync_query_time_sale_limit.insert(0, "100")
        sync_query_time_sale_limit.grid(row=2, column=1,sticky=tk.E,padx=30)
        start_button_time_sale = tk.Button(tab2, text="查询出售购物车",width=15, command=lambda: add_task_to_steam_cart(sync_query_time_sale.get(),sync_query_time_sale_limit.get(),self.tree2,"itemLocation[]=false,tradeLockTo[]=0",count_label_value,count_label_value_all,config.authorization_two))
        start_button_time_sale.grid(row=2,  column=2,sticky=tk.W,padx=30)
        stop_button_time_sale = tk.Button(tab2, text="确认出售购物车",width=15, command=lambda: confirm_task_to_sale_cart())
        stop_button_time_sale.grid(row=2,  column=3,sticky=tk.W)
        

        sync_query_time_change = tk.Entry(tab2,width=30)
        sync_query_time_change.grid(row=3, column=0,sticky=tk.E,padx=30)
        sync_query_time_change_limit = tk.Entry(tab2,width=30)
        sync_query_time_change_limit.insert(0, "100")
        sync_query_time_change_limit.grid(row=3, column=1,sticky=tk.E,padx=30)
        start_button_time_change = tk.Button(tab2, text="查询出售中数据",width=15, command=lambda: add_task_to_change_cart(sync_query_time_change.get(),sync_query_time_change_limit.get(),self.tree2,count_label_value,count_label_value_all,config.authorization_two))
        start_button_time_change.grid(row=3,  column=2,sticky=tk.W,padx=30)
        stop_button_time_change = tk.Button(tab2, text="确认出售中数据",width=15, command=lambda: confirm_task_to_change_cart(config.authorization_two))
        stop_button_time_change.grid(row=3,  column=3,sticky=tk.W)
        

        count_label = tk.Label(tab2, text="当前条数:")
        count_label.grid(row=4,column=0,sticky=tk.E,padx=30,pady=30)
        count_label_value = tk.Entry(tab2,width=30)
        count_label_value.grid(row=4, column=1,sticky=tk.E,padx=30,pady=30)
        count_label_all = tk.Label(tab2, text="总条数:")
        count_label_all.grid(row=4,column=2,sticky=tk.W,padx=30,pady=30)
        count_label_value_all = tk.Entry(tab2,width=30)
        count_label_value_all.grid(row=4, column=3,sticky=tk.W,pady=30)
        
        # 列表展示部分
        self.tree2 = ttk.Treeview(tab2, height=25, selectmode="browse",columns=("id", "title", "gameType", "price", "instantPrice"), show='headings')
        # 创建滚动条
        self.tree2.column("id", width=300, anchor='center')
        self.tree2.column("title", width=300, anchor='center')
        self.tree2.column("gameType", width=150, anchor='center')
        self.tree2.column("price", width=150, anchor='center')
        self.tree2.column("instantPrice", width=150, anchor='center')

        self.tree2.heading("id", text="英文名称")
        self.tree2.heading("title", text="名称")
        self.tree2.heading("gameType", text="饰品类型")
        self.tree2.heading("price", text="价格")
        self.tree2.heading("instantPrice", text="即时销售价格")
        self.display_data1(None, self.tree2)

        # 布局
        self.tree2.grid(row=6,columnspan=4,sticky=tk.NS,padx=30,pady=10)
        # 绑定行选择事件
        self.tree2.bind("<<TreeviewSelect>>", self.on_row_select_2)

        # 绑定键盘事件（Ctrl+C 复制选中行）
        self.root.bind("<Control-c>", self.copy_selection_2)

    def create_tab3(self):
        tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(tab2, text='查询出售购买记录')

        # 查询部分
        query_label_inve = tk.Label(tab2, text="出售购买记录")
        query_label_inve.grid(row=0,columnspan=5, column=0)


        default_query="1,100,7.10,1"

        sync_query_type = tk.Entry(tab2,width=10)
        sync_query_type.grid(row=1, column=0,sticky=tk.E,padx=10)
        sync_query_type.insert(0, "Sell")

        sync_query_time_sale_buy = tk.Entry(tab2,width=30)
        sync_query_time_sale_buy.grid(row=1, column=1,sticky=tk.W,padx=10)
        
        sync_query_time_sale_buy_limit = tk.Entry(tab2,width=30)
        sync_query_time_sale_buy_limit.insert(0, default_query)
        sync_query_time_sale_buy_limit.grid(row=1, column=2,sticky=tk.E,padx=10)
        start_button_time_sale_buy = tk.Button(tab2, text="查询-账号1",width=15, command=lambda: query_my_sale_buy_record(sync_query_time_sale_buy.get(),sync_query_type.get(),self.tree3,config.my_buy_current_file,count_label_value_three,count_label_value_all_three))
        start_button_time_sale_buy.grid(row=1,  column=3,sticky=tk.W,padx=10)
        stop_button_time_sale_buy = tk.Button(tab2, text="同步历史-账号1",width=15, command=lambda: update_my_sale_buy_record(sync_query_time_sale_buy_limit.get(),config.authorization,config.my_buy_current_file))
        stop_button_time_sale_buy.grid(row=1,  column=4,sticky=tk.W)


        sync_query_type_two = tk.Entry(tab2,width=10)
        sync_query_type_two.grid(row=2, column=0,sticky=tk.E,padx=10)
        sync_query_type_two.insert(0, "Sell")

        sync_query_time_sale_buy_two = tk.Entry(tab2,width=30)
        sync_query_time_sale_buy_two.grid(row=2, column=1,sticky=tk.W,padx=10)

        sync_query_time_sale_buy_two_limit = tk.Entry(tab2,width=30)
        sync_query_time_sale_buy_two_limit.insert(0, default_query)
        sync_query_time_sale_buy_two_limit.grid(row=2, column=2,sticky=tk.E,padx=10)
        start_button_time_sale_buy_two = tk.Button(tab2, text="查询-账号2",width=15, command=lambda: query_my_sale_buy_record(sync_query_time_sale_buy_two.get(),sync_query_type_two.get(),self.tree3,config.my_buy_current_file_two,count_label_value_three,count_label_value_all_three))
        start_button_time_sale_buy_two.grid(row=2,  column=3,sticky=tk.W,padx=10)
        stop_button_time_sale_buy_two = tk.Button(tab2, text="同步历史-账号2",width=15, command=lambda: update_my_sale_buy_record(sync_query_time_sale_buy_two_limit.get(),config.authorization_two,config.my_buy_current_file_two))
        stop_button_time_sale_buy_two.grid(row=2,  column=4,sticky=tk.W)

        count_label_three = tk.Label(tab2, text="当前条数:")
        count_label_three.grid(row=4,column=0,sticky=tk.E,padx=30,pady=30)
        count_label_value_three = tk.Entry(tab2,width=30)
        count_label_value_three.grid(row=4, column=1,sticky=tk.E,padx=30,pady=30)
        count_label_all_three = tk.Label(tab2, text="总条数:")
        count_label_all_three.grid(row=4,column=2,sticky=tk.W,padx=30,pady=30)
        count_label_value_all_three = tk.Entry(tab2,width=30)
        count_label_value_all_three.grid(row=4, column=3,sticky=tk.W,pady=30)
   
        
        
        # 列表展示部分
        self.tree3 = ttk.Treeview(tab2, height=25, selectmode="browse",columns=("action", "subject", "cn_name", "price_us", "price", "buff_price", "buff_price_divided", "buff_price_divided_rate", "category_group_name", "updatedAt"), show='headings')
        # 创建滚动条
        width_avg = 80
        self.tree3.column("action", width=width_avg, anchor='center')
        self.tree3.column("subject", width=200, anchor='center')
        self.tree3.column("cn_name", width=200, anchor='center')
        self.tree3.column("price_us", width=width_avg, anchor='center')
        self.tree3.column("price", width=width_avg, anchor='center')
        self.tree3.column("buff_price", width=width_avg, anchor='center')
        self.tree3.column("buff_price_divided", width=width_avg, anchor='center')
        self.tree3.column("buff_price_divided_rate", width=width_avg, anchor='center')
        self.tree3.column("category_group_name", width=width_avg, anchor='center')
        self.tree3.column("updatedAt", width=120, anchor='center')

        self.tree3.heading("action", text="销售类型")
        self.tree3.heading("subject", text="名称")
        self.tree3.heading("cn_name", text="英文名")
        self.tree3.heading("price_us", text="美元价")
        self.tree3.heading("price", text="当前价")
        self.tree3.heading("buff_price", text="buff价格")
        self.tree3.heading("buff_price_divided", text="盈利价")
        self.tree3.heading("buff_price_divided_rate", text="盈利率")
        self.tree3.heading("category_group_name", text="类型")
        self.tree3.heading("updatedAt", text="时间")
        self.display_data1(None, self.tree3)

        # 布局
        self.tree3.grid(row=6,columnspan=5,sticky=tk.NS,padx=30,pady=10)
        # 绑定行选择事件
        self.tree3.bind("<<TreeviewSelect>>", self.on_row_select_3)

        # 绑定键盘事件（Ctrl+C 复制选中行）
        self.root.bind("<Control-c>", self.copy_selection_3)



    def on_row_select_1(self, event):
        # 获取选中行的内容（可选）
        print("")
        selected_item = self.tree_1_2.selection()
        if selected_item:
            item_values = self.tree_1_2.item(selected_item)['values']
            print("选中的行内容:", item_values)

    def copy_selection_1(self, event):
        selected_item = self.tree_1_2.selection()
        if selected_item:
            item_values = self.tree_1_2.item(selected_item)['values'][1]
            # 将选中行的数据拼接成字符串
            pyperclip.copy(item_values)  # 复制到剪贴板
            print("已复制到剪贴板:", item_values)

    def on_row_select_2(self, event):
        # 获取选中行的内容（可选）
        print("")
        selected_item = self.tree2.selection()
        if selected_item:
            item_values = self.tree2.item(selected_item)['values']
            print("选中的行内容:", item_values)

    def copy_selection_2(self, event):
        selected_item = self.tree2.selection()
        if selected_item:
            item_values = self.tree2.item(selected_item)['values'][1]
            # 将选中行的数据拼接成字符串
            pyperclip.copy(item_values)  # 复制到剪贴板
            print("已复制到剪贴板:", item_values)



    def on_row_select_3(self, event):
        # 获取选中行的内容（可选）
        print("")
        selected_item = self.tree3.selection()
        if selected_item:
            item_values = self.tree3.item(selected_item)['values']
            print("选中的行内容:", item_values)

    def copy_selection_3(self, event):
        selected_item = self.tree3.selection()
        if selected_item:
            item_values = self.tree3.item(selected_item)['values'][1]
            # 将选中行的数据拼接成字符串
            pyperclip.copy(item_values)  # 复制到剪贴板
            print("已复制到剪贴板:", item_values)




    def display_data1(self, query, tree):
        print("显示数据")
      
add_list=[]
change_list=[]




def query_my_sale_buy_record(query,query_type,tree,file_path,count_label_value,count_label_value_all):
    print("查询列表"+query+",路径："+file_path)
    add_list.clear()
    change_list.clear()

    count_label_value.delete(0,tk.END)
    count_label_value_all.delete(0,tk.END)

    for item in tree.get_children():
        tree.delete(item)
            # 将新的数据插入到表格中
    file_all_data=bastPricetMyBuy.find_buy_price(file_path)

    # 打开文件准备读取
    current_size=0
    all_size=0
    for entry in file_all_data:
        all_size+=1

        if query_type is None:
            if query is None:
                tree.insert("", "end", values=(entry["action"],entry["subject"],entry["cn_name"],entry["price_us"],entry["price"],entry["buff_price"],entry["buff_price_divided"],entry["buff_price_divided_rate"],entry["category_group_name"],entry["updatedAt"]))
            elif query in entry["action"] or query in entry["subject"] or query in entry["cn_name"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
                current_size+=1
                tree.insert("", "end", values=(entry["action"],entry["subject"],entry["cn_name"],entry["price_us"],entry["price"],entry["buff_price"],entry["buff_price_divided"],entry["buff_price_divided_rate"],entry["category_group_name"],entry["updatedAt"]))
        elif query_type in entry["action"]:
            if query is None:
                tree.insert("", "end", values=(entry["action"],entry["subject"],entry["cn_name"],entry["price_us"],entry["price"],entry["buff_price"],entry["buff_price_divided"],entry["buff_price_divided_rate"],entry["category_group_name"],entry["updatedAt"]))
            elif query in entry["action"] or query in entry["subject"] or query in entry["cn_name"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
                current_size+=1
                tree.insert("", "end", values=(entry["action"],entry["subject"],entry["cn_name"],entry["price_us"],entry["price"],entry["buff_price"],entry["buff_price_divided"],entry["buff_price_divided_rate"],entry["category_group_name"],entry["updatedAt"]))
        


    count_label_value.insert(0,str(current_size))
    count_label_value_all.insert(0,str(all_size))

def update_my_sale_buy_record(limit,authorization,file_path):
    print("同步列表"+limit+",路径："+file_path)
    limit_list=limit.split(",")
    offset=int(limit_list[0])
    limit=int(limit_list[1])
    exchange_rate=float(limit_list[2])
    seartch_page=int(limit_list[3])

    ## 同步最新数据
    bastPricetMyBuy.create_my_buy_List_all(offset,limit,exchange_rate,seartch_page,authorization,file_path)
    


    print("查询列表成功")


def add_task_to_steam_cart(content,limit,tree,treeFilters,count_label_value,count_label_value_all,authorization):
    add_list.clear()
    change_list.clear()
    count_label_value.delete(0,tk.END)
    count_label_value_all.delete(0,tk.END)

    print("添加任务到steam购物车"+content+limit)
    if content is None:
        title=""
    else:
        title=content

    reponse_json=offer_sell_product.get_my_invert_List(title=title,limit=limit,treeFilters=treeFilters,authorization=authorization)
    my_invert_list=reponse_json['objects']

    if my_invert_list is None or len(my_invert_list) == 0: 
        print("获取当前的采购饰品情况失败")
        return
    

    count_label_value.insert(0,str(len(my_invert_list)))
    count_label_value_all.insert(0,reponse_json['total']['  '])

    for item in tree.get_children():
        tree.delete(item)
            # 将新的数据插入到表格中

    for entry in my_invert_list:
        print(entry)
        if entry["price"]['USD'] is not None or entry["price"]['USD']!="":
            price=round(int(entry["price"]['USD'])/100*exchange_rate,2)
        
        if entry["recommendedPrice"]['offerPrice']['USD'] is not None or entry["recommendedPrice"]['offerPrice']['USD']!="":
            instantPrice=round(int(entry["recommendedPrice"]['offerPrice']['USD'])/100*exchange_rate,2)

        tree.insert("", "end", values=(entry["itemId"],entry["title"],entry["gameType"],price,instantPrice))
    
    
    for item in my_invert_list:
        print(item['itemId'])
        add_list.append(item['itemId'])
    
    print(add_list)
    # offer_sell_product.add_my_invert_List(items=add_list)


    print("查询列表成功")


def confirm_task_to_steam_cart(authorization):
    offer_sell_product.add_my_invert_List(items=add_list,authorization=authorization)
    add_list.clear()
    change_list.clear()
    print("添加任务到steam购物车")


def confirm_task_to_sale_cart():
    offer_sell_product.add_my_invert_List(items=add_list)
    add_list.clear()
    change_list.clear()
    print("添加任务到出售购物车")



def add_task_to_change_cart(content,limit,tree,count_label_value,count_label_value_all,authorization):
    add_list.clear()
    change_list.clear()
    count_label_value.delete(0,tk.END)
    count_label_value_all.delete(0,tk.END)

    print("添加任务到出售单购物车"+content+limit)
    if content is None:
        title=""
    else:
        title=content

    for item in tree.get_children():
        tree.delete(item)
            # 将新的数据插入到表格中

    reponse_json=offer_sell_product.get_my_offer_List(title=title,limit=limit,authorization=authorization)
    my_invert_list=reponse_json['objects']

    if my_invert_list is None or len(my_invert_list) == 0: 
        print("获取当前的出售饰品情况失败")
        return

    count_label_value.insert(0,str(len(my_invert_list)))
    count_label_value_all.insert(0,reponse_json['total']['offers'])

    for entry in my_invert_list:
        print(entry)
        if entry["price"]['USD'] is not None or entry["price"]['USD']!="":
            price=round(int(entry["price"]['USD'])/100*exchange_rate,2)
        
        if entry["recommendedPrice"]['offerPrice']['USD'] is not None or entry["recommendedPrice"]['offerPrice']['USD']!="":
            instantPrice=round(int(entry["recommendedPrice"]['offerPrice']['USD'])/100*exchange_rate,2)
        tree.insert("", "end", values=(entry["itemId"],entry["title"],entry["gameType"],price,instantPrice))
    
    
    for item in my_invert_list:
        print(item['itemId'])
        change_list.append(item['itemId'])
    

def confirm_task_to_change_cart(authorization):
    offer_sell_product.add_my_sell_List(items=change_list,authorization=authorization)
    add_list.clear()
    change_list.clear()
    print("添加出售中成功")





def search_min_data(query, tree):
    print("查询采购最低价")
        # 清空之前的数据
    for item in tree.get_children():
        tree.delete(item)
            # 将新的数据插入到表格中

    create_target_list=bastPricetSellSkin86.create_avg_target_min(exchange_rate)
    if create_target_list is None or len(create_target_list)==0 :
        print("没有数据")
        return

    create_target_list.sort(key=lambda x:x['dm_buy_buff_sale_min_rate'],reverse=True)

    for entry in create_target_list:
        if query is None:
            tree.insert("", "end", values=(entry["drtitle"],entry["title"], entry["totalSales"], entry["date"], entry["offer_price"], entry["target_price"], entry["buff_avg_price"], entry["dm_buy_buff_sale_avg"], entry["dm_buy_buff_sale_avg_rate"], entry["dm_buy_buff_sale_min"], entry["dm_buy_buff_sale_min_rate"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
        elif query in entry["drtitle"] or query in entry["title"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
            tree.insert("", "end", values=(entry["drtitle"],entry["title"], entry["totalSales"], entry["date"], entry["offer_price"], entry["target_price"], entry["buff_avg_price"], entry["dm_buy_buff_sale_avg"], entry["dm_buy_buff_sale_avg_rate"], entry["dm_buy_buff_sale_min"], entry["dm_buy_buff_sale_min_rate"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
    

def timer_task_buy_min_data( query,sync_button,public_key,secret_key):
    sync_data(query, sync_button)
    buy_min_data( None,public_key,secret_key)


def buy_min_data( query,public_key,secret_key):
    print("开始采购")
    create_target_list=bastPricetSellSkin86.create_avg_target_min(exchange_rate)

    filter_list=[]
    for entry in create_target_list:
        if query is None:
            filter_list=create_target_list
        elif query in entry["drtitle"] or query in entry["title"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
            filter_list.append(entry)

    filename=config.data_local_excel+"/creat_target_min_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    bastPricetSellSkin86.creat_now(filter_list,filename,100,"min",public_key,secret_key)


def search_avg_data( query,tree):
    print("查询平均价")
        # 清空之前的数据
    for item in tree.get_children():
        tree.delete(item)
            # 将新的数据插入到表格中
            
    create_avg_target_list=bastPricetSellSkin86.create_avg_target_avg(exchange_rate)
    if create_avg_target_list is None or len(create_avg_target_list)==0 :
        print("没有数据")
        return


    create_avg_target_list.sort(key=lambda x:x['dm_buy_buff_sale_avg_rate'],reverse=True)
    for entry in create_avg_target_list:
        if query is None:
            tree.insert("", "end", values=(entry["drtitle"],entry["title"], entry["totalSales"], entry["date"], entry["offer_price"], entry["target_price"], entry["buff_avg_price"], entry["dm_buy_buff_sale_avg"], entry["dm_buy_buff_sale_avg_rate"], entry["dm_buy_buff_sale_min"], entry["dm_buy_buff_sale_min_rate"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
        elif query in entry["drtitle"] or query in entry["title"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
            tree.insert("", "end", values=(entry["drtitle"],entry["title"], entry["totalSales"], entry["date"], entry["offer_price"], entry["target_price"], entry["buff_avg_price"], entry["dm_buy_buff_sale_avg"], entry["dm_buy_buff_sale_avg_rate"], entry["dm_buy_buff_sale_min"], entry["dm_buy_buff_sale_min_rate"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
    


def buy_avg_data( query,tree,public_key,secret_key):
    print("购买平均价")
    create_avg_target_list=bastPricetSellSkin86.create_avg_target_avg(exchange_rate)
    filename=config.data_local_excel+"/creat_target_avg_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"

    filter_list=[]
    for entry in create_avg_target_list:
        if query is None:
            filter_list=create_avg_target_list
        elif query in entry["drtitle"] or query in entry["title"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
            filter_list.append(entry)


    bastPricetSellSkin86.creat_now(filter_list,filename,50,"avg",public_key,secret_key)



def start_data_timer(search_content, stop_button_time,start_button_time,task,sync_button,public_key,secret_key):
      # 每 5 秒执行一次任务
    start_button_time.config(state=tk.DISABLED)
    task.start(search_content,sync_button,public_key,secret_key)
    stop_button_time.config(state=tk.NORMAL)


def stop_data_timer(search_content, stop_button_time,start_button_time,task,sync_button,public_key,secret_key):
    stop_button_time.config(state=tk.DISABLED)
    task.stop(sync_button,public_key,secret_key)
    start_button_time.config(state=tk.NORMAL)
    


# def start_avg_data_timer(search_content, timer,stop_button_time,start_button_time,task):
#       # 每 5 秒执行一次任务
#     start_button_time.config(state=tk.DISABLED)
#     task.start()
#     stop_button_time.config(state=tk.NORMAL)


# def stop_avg_data_timer(search_content, timer,stop_button_time,start_button_time,task):
#     stop_button_time.config(state=tk.DISABLED)
#     task.stop()
#     start_button_time.config(state=tk.NORMAL)
    



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
    platform=str(query_content[6])

    bastPricetSellSkin86.sync_data(limit_page,page,page_size,price_start,price_end,selling_num_start)
    sync_button.config(state=tk.NORMAL,text="同步")
    print("同步结束")

    
if __name__ == "__main__":
    initFile()
    root = tk.Tk()
    root.geometry("1200x800")
    app = TabbedApp(root)
    root.mainloop()