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
import Skin86BaseData
import bastPricetSellSkin86

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


filter_num=30   #过滤平均销量大于30的数量
filter_list=[]   #过滤平均销量大于30的列表


data_path=config.data_local
file_name=config.data_local_analysis+"/my_buy_list.txt"
buff_file=config.skin_86_product_all_buy
my_buy_current_file=config.data_local_analysis+"/my_buy_current_list.txt"
my_target_current_file=config.data_local_analysis+"/my_target_current_list.txt"

def create_my_buy_List_all(offset=0,limit=10,exchange_rate=7.14,seartch_page=10):
    history_list=[]
    product_name_list=[]

    with open(config.cs_product_all_name, 'r', encoding='utf-8') as all_name_file:
        for line in all_name_file:
            product_name_list.append(line.strip())

    if not os.path.exists(file_name):
        open(file_name,'w',encoding='utf-8')
    else:
        with open(file_name, 'r', encoding='utf-8') as my_buy_list_file:
            for cur_data in my_buy_list_file:
                json_item=json.loads(cur_data)
                history_list.append(json_item)

    page=1
    with open(file_name, 'a+', encoding='utf-8') as my_buy_list_file:
        while True:
            print("获取第"+str(page)+"页数据"+"offset="+str(offset)+" limit="+str(limit))
            if page>seartch_page:
                print("获取数据达到要求")
                break

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
                    buy_data['action']=item['action']
                    buy_data['subject']=item['subject']
                    if item['changes'] is None or len(item['changes'])>0:
                        if item['action'] == "Sell" or item['action'] == "Deposit":
                            buy_data['price']=round(float(item['changes'][0]['money']['amount'])*recharge_rate*exchange_rate,2) 
                            buy_data['price_us']=float(item['changes'][0]['money']['amount'])
                        else:
                            buy_data['price']=round(float(item['changes'][0]['money']['amount'])*recharge_rate*exchange_rate,2) 
                            buy_data['price_us']=float(item['changes'][0]['money']['amount'])
                    else:
                        buy_data['price']= 0
                        buy_data['price_us']= 0

                    buy_data['updatedAt']=datetime.fromtimestamp(int(item['updatedAt'])).strftime('%Y-%m-%d %H:%M:%S')
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


def find_buy_price():
    buff_file_list=[]
    with open(buff_file, 'r', encoding='utf-8') as buff_file_read:
        for buff_data in buff_file_read:
            buff_data_item=json.loads(buff_data)
            buff_file_list.append(buff_data_item)


    second_list=[]
    with open(file_name, 'r', encoding='utf-8') as second_read_file:
        for second in second_read_file:
            if '印花' not in second:
                second_item=json.loads(second)
                second_list.append(second_item) 
    
    # 按照时间排序second_list
    
    second_list.sort(key=lambda x:x['updatedAt'],reverse=True)

    with open(my_buy_current_file, 'w', encoding='utf-8') as my_buy_current_file_write:
        for send_data in second_list:

            for buff_info in buff_file_list:
                send_data['buff_price']=0.01
                send_data['buff_price_divided']=0.01
                send_data['buff_price_divided_rate']=0.01
                send_data['category_group_name']=buff_info['category_group_name']
                if buff_info['market_name'] == send_data['cn_name']:
                    print(send_data['cn_name'])
                    if send_data['price'] is not None and send_data['price']!=0:
                        send_data['buff_price']=buff_info['sell_min_price']
                        send_data['buff_price_divided']=round(buff_info['sell_min_price']*trans_buff_service_change()-send_data['price'],2)
                        send_data['buff_price_divided_rate']=round((buff_info['sell_min_price']*trans_buff_service_change()-send_data['price'])/send_data['price'],2)
                        break
                        

            my_buy_current_file_write.write(json.dumps(send_data,ensure_ascii=False)+"\n")


def tranStrToDatetime(str_time):

    # 指定日期格式
    date_format = "%Y-%m-%d %H:%M:%S"

    # 使用strptime方法将日期字符串转换为datetime对象
    date_obj = datetime.strptime(str_time, date_format)

    # 使用timestamp()方法将datetime对象转换为以秒为单位的时间戳
    timestamp = int(date_obj.timestamp())
    return timestamp

                
            
def find_target_price(target_list):
    buff_file_list=[]
    with open(buff_file, 'r', encoding='utf-8') as buff_file_read:
        for buff_data in buff_file_read:
            buff_data_item=json.loads(buff_data)
            buff_file_list.append(buff_data_item)


    # 获取所有的已购买的数据 安装名称
    second_list=[]
    with open(file_name, 'r', encoding='utf-8') as second_read_file:
        for second in second_read_file:
            second_item=json.loads(second)
            second_list.append(second_item) 


    # 使用字典来存储每个产品名称的最大购买时间
    max_purchase_times = {}
    for second_line in second_list:
        if second_line['subject'] not in max_purchase_times or tranStrToDatetime(second_line['updatedAt']) > tranStrToDatetime(max_purchase_times[second_line['subject']]['updatedAt']):
            max_purchase_times[second_line['subject']] = second_line



    with open(my_target_current_file, 'w', encoding='utf-8') as my_target_current_write:
        for target_data in target_list:
            print(target_data['title'])
            for buff_info in buff_file_list:
                target_data['buff_price']=0.01
                target_data['buff_price_divided']=0.01
                target_data['buff_price_divided_rate']=0.01
                target_data['cn_name']=""

                if buff_info['en_name'] == target_data['title']:
                    target_data['cn_name']=buff_info['market_name']
                    target_data['buff_price']=buff_info['sell_min_price']
                    target_data['buff_price_divided']=round(buff_info['sell_min_price']*trans_buff_service_change()-target_data['price'],2)
                    target_data['buff_price_divided_rate']=round((buff_info['sell_min_price']*trans_buff_service_change()-target_data['price'])/target_data['price'],2)
                    break

            

            if target_data['title'] in max_purchase_times:
                max_purchase=max_purchase_times[target_data['title']]
                target_data['recent_purchase_time']=max_purchase['updatedAt']
                target_data['recent_purchase_price']=max_purchase['price']
                target_data['recent_purchase_price_divided']=round(target_data['recent_purchase_price']-target_data['price'],2)
                  
            else:
                target_data['recent_purchase_time']="" 
                target_data['recent_purchase_price']=0
                target_data['recent_purchase_price_divided']=0
                

            
            my_target_current_write.write(json.dumps(target_data,ensure_ascii=False)+"\n")

                        
            
  


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
            'authorization': config.authorization,
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
            "statuses": 'success',
            # "activities": 'exchange,sell,purchase,instant_sell,charging_fee,target_closed,withdraw,deposit,cash_deposit,cashback',
            "activities": 'exchange,sell,purchase,instant_sell,charging_fee,target_closed,deposit,cash_deposit,cashback',
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
        "action":'类型',
        "cn_name":'饰品名称',
        "subject":'饰品名称-英文',
        "price_us":'购买-美元价格',
        "price":'购买',
        "updatedAt":'日期',
        "buff_price":'当前buff售价',
        "buff_price_divided":'盈利价',
        "buff_price_divided_rate":'盈利价率',
        "category_group_name":'类型',
    
    }
    column_order = ['id', 'action', 'cn_name', 'subject','price_us','price','updatedAt','buff_price','buff_price_divided','buff_price_divided_rate','category_group_name']

    # 打开文件准备读取
    with open(my_buy_current_file, 'r', encoding='utf-8') as file:
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




# 一行一行的读取json数组，并写入到excel中
def export_target_to_excel():
    print("开始导出数据")
    filename=data_path+"/excel/"+"my_target_list_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"

    all_data=[]

        # 定义中文名和字段样式
    chinese_columns = {
        "cn_name":'饰品名称',
        "title":'饰品名称-英文',
        "amount":'数量',
        "price":'价格',
        "createdAt":'日期',
        "buff_price":'当前buff售价',
        "buff_price_divided":'盈利价',
        "buff_price_divided_rate":'盈利价率',
        "recent_purchase_time":'最近购买时间',
        "recent_purchase_price":'最近购买价格',
        "recent_purchase_price_divided":'最近购买和当前购买价差额',
    
    }
    column_order = ['cn_name', 'title', 'amount','price','createdAt','buff_price','buff_price_divided','buff_price_divided_rate','recent_purchase_time','recent_purchase_price','recent_purchase_price_divided']

    # 打开文件准备读取
    with open(my_target_current_file, 'r', encoding='utf-8') as file:
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



# 获取最采购高价和出售最低价
# 获取当前的采购饰品情况
def get_my_target_List(exchange_rate=7.14):
    target_list=[]
    try:
        # 设置请求的URL
        url = 'https://api.dmarket.com/exchange/v1/user/targets'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': config.authorization,
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'jkkat': '50788078',
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
            "gameId": "a8db",
            "limit": 100,
            "currency": "USD",
            "platform": "browser",
            "priceTo": 0,
            "priceFrom": 0,
            "orderDir": "desc",
            "orderBy": "updated",
            "side": "user"
        }

        # 发送POST请求
        response = requests.get(url, params=params,headers=headers)
        reponse_json = json.loads(response.text)
        offers=reponse_json['objects']
        for offer in offers:
            target={}
            target['title']=offer['title']
            target['amount']=offer['amount']
            target['price']=round(float(offer['price']['USD'])/100*exchange_rate*recharge_rate,2)
            target['createdAt']=datetime.fromtimestamp(int(offer['createdAt'])).strftime('%Y-%m-%d %H:%M:%S')
            target_list.append(target)
            
    except Exception as e:
        print(e)
        return None
    return target_list


if __name__ == '__main__':
    start_time=int(time.time())


    # 下载所有的buff饰品名称
    # Skin86BaseData.get_skin_86_market_all(file_name=buff_file,limit_page=200,page=1,page_size=100,price_start=0.6,price_end=300,selling_num_start=200)
   
    
   


    # 追加所有的已购买  
    # create_my_buy_List_all(1,100,7.14,10)
    find_buy_price()
    export_json_to_excel()


    # # # 查看所有的采购单
    # exchange_rate=bastPricetSellSkin86.find_us_exchange()
    # target_list=get_my_target_List(exchange_rate)
    # find_target_price(target_list)
    # export_target_to_excel()


    end_time=int(time.time())
    print("运行时间："+str(end_time-start_time))
    
