import json
from datetime import datetime

import pandas as pd
import requests
from datetime import datetime
import time
import os
import shutil
from zipfile import ZipFile
import threading

import config

# change url to prod
rootApiUrl = "https://api.dmarket.com"
# exchange_rate=7.19   #实际汇率
recharge_rate=1.027   #充值手续费
bank_rate=0.985   #实际汇率*实际提现到手
steam_exchange_rate=0.79   #实际汇率*实际提现到手
searchNum="7"  #查询天数
searchUnit="D"  #查询单位

all_list=[]

data_path="E:/pythonFile/python/python_data/dassbuff/data"
skin_86_path="/analysis/skin_86_product_all.txt"

filter_num=30   #过滤平均销量大于30的数量
filter_list=[]   #过滤平均销量大于30的列表




# 实现追加
def get_my_buy_List_all(offset=0,limit=10,exchange_rate=7.14):
    file_name="E:/pythonFile/python/python_data/dassbuff/data/analysis/my_buy_list.txt"
    buff_file="E:/pythonFile/python/python_data/dassbuff/data/analysis/skin_86_product_all.txt"
    history_list=[]
    page=1

    product_name_list=[]
    with open("data/cs_product_all_name.txt", 'r', encoding='utf-8') as all_name_file:
        for line in all_name_file:
            product_name_list.append(line.strip())

    with open(file_name, 'r', encoding='utf-8') as my_buy_list_file:
        for cur_data in my_buy_list_file:
            json_item=json.loads(cur_data)
            history_list.append(json_item)

    
    buff_file_list=[]
    with open(buff_file, 'r', encoding='utf-8') as buff_file:
        for buff_data in buff_file:
            buff_data_item=json.loads(buff_data)
            buff_file_list.append(buff_data_item)


    with open(file_name, 'a+', encoding='utf-8') as my_buy_list_file:
        while True:
            print("获取第"+str(page)+"页数据"+"offset="+str(offset)+" limit="+str(limit))
            time.sleep(1)
            reponse_json=get_my_buy_List(page,offset,limit)

            if reponse_json is None:
                print("获取数据有误")
                break

            if reponse_json['objects'] is None or len(reponse_json['objects'])<1  :
                print("获取数据完成")
                break

            buy_data_list=[]
            offers=reponse_json['objects']
            total=reponse_json['total']
            print("总数据量："+str(total))
            
           
            for item in offers:
                try:
                    print(item['subject'])
                    buy_data={}
                    buy_data['id']=item['id']
                    buy_data['subject']=item['subject']
                    buy_data['price']=round(float(item['changes'][0]['money']['amount'])*recharge_rate*exchange_rate,2) 
                    buy_data['updatedAt']=datetime.fromtimestamp(int(item['updatedAt'])).strftime('%Y-%m-%d')
                    buy_data_list.append(buy_data)


                    # 匹配英文名称
                    buy_data['cn_name']="0"
                    for cur_name in product_name_list:
                        try:
                            cn_name_list=cur_name.split("----")
                            if cn_name_list[1] == buy_data['subject']:
                                buy_data['cn_name']=cn_name_list[0]
                                break
                        except Exception as e:  
                            continue
                    
                    old_flag=True
                    for history_item in history_list:
                        if history_item['id'] == buy_data['id']:
                            old_flag=False
                            break

                    
                    buy_data['buff_price']=0.01
                    buy_data['buff_price_divided']=0.01
                    buy_data['buff_price_divided_rate']=0.01
                    for buff_info in buff_file_list:
                        if buff_info['market_name'] == buy_data['cn_name']:
                                print(buy_data['cn_name'])
                                buy_data['buff_price']=buff_info['sell_min_price']
                                buy_data['buff_price_divided']=round(buff_info['sell_min_price']*trans_buff_service_change()-buy_data['price'],2)
                                buy_data['buff_price_divided_rate']=round((buff_info['sell_min_price']*trans_buff_service_change()-buy_data['price'])/buy_data['price'],2)



                    # 追加到最后一行
                    if old_flag:
                        my_buy_list_file.write(json.dumps(buy_data,ensure_ascii=False)+"\n")
                except Exception as e:
                    print(e)
                    print("当前行的数据解析有误")

            if total<offset:
                break
            offset=offset+limit
            page=page+1
                
  


# dm手续费 
def trans_dm_service_change(price):
    if price is None:
        return 1
    elif price >= 0 and price < 50:
        return 0.90
    elif price >= 50 and price < 100:
        return 0.95
    elif price >= 100:
        return 0.98
    else :    
        return 1
    

# 交易费用+提现手续费 
def trans_buff_service_change():
    return 0.975


# 提现手续费 
def trans_buff_bank_change():
    return 0.99



# 获取最采购高价和出售最低价
# 获取当前的采购饰品情况
def get_my_buy_List(exchange_rate=7.14,offset=0,limit=10):
    
    try:
        # 设置请求的URL
        url = 'https://api.dmarket.com/exchange/v1/history'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmNjk0NjQzNy0wN2ZlLTRhMWYtOTMxYi1jN2JiZmYzMzdlMWEiLCJleHAiOjE3MjYwNTU4MTQsImlhdCI6MTcyMzQ2MzgxNCwic2lkIjoiNDM1ZTEzMTMtNjEyOC00OGY4LWEyNmEtMTA3YmVlMTRiMWIzIiwidHlwIjoiYWNjZXNzIiwiaWQiOiI0MWU0Y2RlZC1hMDcxLTRiMDUtODRjYS1lYzM2OWEzZjYyZjUiLCJwdmQiOiJyZWd1bGFyIiwicHJ0IjoiMjQwOCIsImF0dHJpYnV0ZXMiOnsid2FsbGV0X2lkIjoiZjg1MTM4Yjc0NWFiNGIyY2FjNTY3ZTFmMDVmN2VmNGZlNDJjMTUzYzJkMTg0NDM1Yjg2OTk3ODNkMDljOTgxNSIsInNhZ2Ffd2FsbGV0X2FkZHJlc3MiOiIweEM3OWZlMzhjM0I4MzJkODU2ZDJGMUVmQTBGYzAwRUUzMThBOTM2NjQiLCJhY2NvdW50X2lkIjoiODZhZmQxZmYtMDVlOC00NzM5LTkzNmQtN2I2NWUwOWQ3ODVlIn19.Bnig8ltKoIqd8XHScE5RlDjBC3yRh5DYMdabUJibWD1In5MQTrnTngYBUbioXrRsHzxDZWThoEOpKqQhd5_-mQ',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'jkkat': '4e55ab9f',
            'language': 'ZH',
            'origin': 'https://dmarket.com',
            'payment-session-id': '77af0392-9f37-40c8-9e68-4bbaf9f5cf00',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
        # 设置请求的数据
        params = {
            "version": "V3",
            "offset": offset,
            "limit": limit,
            "activities": 'purchase',
            "statuses": 'success',
        }

        # 发送POST请求
        response = requests.get(url, params=params,headers=headers)
        reponse_json = json.loads(response.text)
        return reponse_json
    except Exception as e:
        print(e)
        return None



# 一行一行的读取json数组，并写入到excel中
def export_json_to_excel():
    print("开始导出数据")
    filename=data_path+"/excel/"+"my_buy_list_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"

    all_data=[]

        # 定义中文名和字段样式
    chinese_columns = {
        "id":'id',
        "cn_name":'饰品名称',
        "subject":'饰品名称-英文',
        "price":'购买',
        "updatedAt":'日期',
        "buff_price":'当前buff售价',
        "buff_price_divided":'盈利价',
        "buff_price_divided_rate":'盈利价率',
    
    }
    column_order = ['id', 'cn_name', 'subject','price','updatedAt','buff_price','buff_price_divided','buff_price_divided_rate']

    # 打开文件准备读取
    file_name="E:/pythonFile/python/python_data/dassbuff/data/analysis/my_buy_list.txt"
    with open(file_name, 'r', encoding='utf-8') as file:
       for line in file:
           json_data=json.loads(line.replace("\\b",""))
           all_data.append(json_data)


    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(all_data)
    
    df = df[column_order]
 
    # 写入Excel文件
    # 注意：如果你需要写入.xlsx文件，需要指定引擎为openpyxl
    # df.to_excel(filename, index=False, engine='openpyxl')

    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        # 获取工作簿和工作表对象
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # 定义加粗和颜色格式
        yellow_format = workbook.add_format({'bold': True, 'bg_color': '#ffff00'})  # 黄色背景色代码

        

        # 设置列标题的中文名和样式
        for col_num, value in enumerate(df.columns.values):
            
            # 设置列宽
            column_width = 9  # 你可以根据需要调整这个值
            worksheet.set_column(col_num, col_num, column_width)
            worksheet.write(0, col_num, chinese_columns[value], yellow_format)


    # 完成后关闭文件
    # workbook.close()





if __name__ == '__main__':
    start_time=int(time.time())

    # 初始化数据
    get_my_buy_List_all(40,10,7.14)
    export_json_to_excel()


    end_time=int(time.time())
    print("运行时间："+str(end_time-start_time))
