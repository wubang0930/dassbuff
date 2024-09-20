import tkinter as tk
from tkinter import ttk
import json
import Skin86BaseDataServer
import time

class TabbedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed Application")

        # 创建一个标签框架
        self.tabControl = ttk.Notebook(self.root)

        # 创建多个标签页
        self.create_tab1()
        self.create_tab2()

        # 将标签框架添加到窗口
        self.tabControl.pack(expand=1, fill="both")
        root.grid_rowconfigure(0, weight=1)  # 设置行权重为1，使得 Treeview 可以伸缩
    

    def create_tab1(self):
        tab1 = ttk.Frame(self.tabControl,width=1000,height=600)
        self.tabControl.add(tab1, text='国内数据')

        # 查询部分
        query_label = tk.Label(tab1, text="查询内容平台:")
        query_label.grid(row=0,columnspan=3,  column=0, padx=10, pady=5,sticky=tk.NSEW)

        query_entry = tk.Entry(tab1)
        query_entry.grid(row=1, column=0,ipadx=10,  padx=10, pady=5,sticky=tk.N)

        query_button = tk.Button(tab1, text="查询", command=lambda: self.display_data1(query_entry.get(), self.tree1))
        query_button.grid(row=1,  column=1, ipadx=10, padx=10, pady=5,sticky=tk.W)

        sync_button = tk.Button(tab1, text="同步数据", command=lambda: sync_data(sync_button))
        sync_button.grid(row=1, column=2, padx=10, pady=5,sticky=tk.N)

        
        # 列表展示部分
        self.tree1 = ttk.Treeview(tab1, columns=("en_name", "market_name","sell_min_price", "sell_max_num","price_alter_percentage_7d", "price_alter_value_7d","category_group_name"), show='headings')
        # 创建滚动条
        col_width = 120
        self.tree1.column("en_name", width=300, anchor='center')
        self.tree1.column("market_name", width=300, anchor='center')
        self.tree1.column("sell_min_price", width=col_width, anchor='center')
        self.tree1.column("sell_max_num", width=col_width, anchor='center')
        self.tree1.column("price_alter_percentage_7d", width=col_width, anchor='center')
        self.tree1.column("price_alter_value_7d", width=col_width, anchor='center')
        self.tree1.column("category_group_name", width=col_width, anchor='center')

        self.tree1.heading("en_name", text="英文名称")
        self.tree1.heading("market_name", text="名称")
        self.tree1.heading("sell_min_price", text="价格")
        self.tree1.heading("sell_max_num", text="数量")
        self.tree1.heading("price_alter_percentage_7d", text="7天变化率")
        self.tree1.heading("price_alter_value_7d", text="7天变化价格")
        self.tree1.heading("category_group_name", text="类型")
        # self.tree1.pack(side=tk.LEFT,pady=40,expand=1, fill="both")
        self.display_data1(None, self.tree1)

         # 创建水平滚动条
        x_scroll = ttk.Scrollbar(tab1, orient="horizontal", command=self.tree1.xview)
        y_scroll = ttk.Scrollbar(tab1, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(xscrollcommand=x_scroll.set)
        self.tree1.configure(yscrollcommand=y_scroll.set)

        # 布局
        self.tree1.grid(row=3,columnspan=3,rowspan =20, column=0,padx=30, pady=30,ipadx=10,ipady=10)



    def create_tab2(self):
        tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(tab2, text='查询页面 2')

        # # 查询部分
        # query_label = tk.Label(tab2, text="查询内容:")
        # query_label.pack(pady=10)

        # query_entry = tk.Entry(tab2)
        # query_entry.pack(pady=10)

        # query_button = tk.Button(tab2, text="查询", command=lambda: self.display_data1(query_entry.get(), self.tree2))
        # query_button.pack(pady=10)

        # # 列表展示部分
        # self.tree2 = ttk.Treeview(tab2, columns=("market_name", "sell_min_price"), show='headings')
        # self.tree2.heading("market_name", text="名称")
        # self.tree2.heading("sell_min_price", text="价格")
        # self.tree2.pack(pady=10)


    def display_data1(self, query, tree):
        # 假设从某个地方获取了一些 JSON 数据
        data = Skin86BaseDataServer.readBuffData()
        # 清空之前的数据
        for item in tree.get_children():
            tree.delete(item)

        # 将新的数据插入到表格中
        for entry in data:
            if query is None:
                tree.insert("", "end", values=(entry["en_name"],entry["market_name"], entry["sell_min_price"], entry["sell_max_num"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
            elif query in entry["en_name"] or query in entry["market_name"] or query in entry["category_group_name"]:  # 基于查询内容过滤数据
                tree.insert("", "end", values=(entry["en_name"],entry["market_name"], entry["sell_min_price"], entry["sell_max_num"], entry["price_alter_percentage_7d"], entry["price_alter_value_7d"], entry["category_group_name"]))
    

    



def sync_data(sync_button):
    # 修改按钮名称为同步中
    sync_button.config(state=tk.DISABLED,text="已同步")
    Skin86BaseDataServer.sync_data()


    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1300x700")
    app = TabbedApp(root)
    root.mainloop()