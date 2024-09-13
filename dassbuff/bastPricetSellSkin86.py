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

import config
import offer_buy_product

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








def get_offer_from_market_average(day,title):
    try:
        market_response = requests.get(rootApiUrl + "/trade-aggregator/v1/avg-sales-graph?gameId=a8db&period="+day+"&title="+title)
        offers = json.loads(market_response.text)
        # f= open("offer_avarage.json","w")
        # f.write(json.dumps(offers))
        # f.close()
        # print(offers)   
        if offers["totalSales"] is None:
            return None
        return offers
    except Exception as e:
        print(e)
        return None




# 查询指定天数的平均销量数据，并构建目标数据
def build_target_body_from_offer_avarage(buff_price,market_price,key_info,exchange_rate,target_list):
    # print(market_price)
    if market_price is None or market_price["totalSales"] is None:
        print(threading.current_thread().name+"近期销售数据为空")
        return ""


    buff_avg_price= buff_price['sell_min_price']
    buff_sum_price= buff_price['sell_valuation']
    buff_statistic= buff_price['sell_max_num']

    buy_max_price= buff_price['buy_max_price']
    buy_max_num= buff_price['buy_max_num']
    price_alter_percentage_7d= buff_price['price_alter_percentage_7d']
    price_alter_value_7d= buff_price['price_alter_value_7d']
    category_group_name= buff_price['category_group_name']

    offer_price=key_info['offer_price'] if key_info['offer_price'] is not None else 999999
    target_price=key_info['target_price'] if key_info['target_price'] is not None else 999999
    target_account=key_info['target_account'] if key_info['target_account'] is not None else 999999


    # current_target_price=0.001
    # current_target_amount=0
    # current_target_createdAt=0
    # if target_list is not None and len(target_list)>1:
    #     for current_target in target_list:
    #         if current_target['title']==buff_price['en_name']:
    #             print("找到当前求购数据"+str(current_target))
    #             current_target_price=current_target['price']*recharge_rate
    #             current_target_amount=current_target['amount']
    #             current_target_createdAt=current_target['createdAt']
    #             break
        


    if offer_price is None or offer_price<=0:
        return ""

    if buff_avg_price is None or buff_avg_price<=0:
        buff_avg_price=0.001

    correlationd_data=[
        {"title":buff_price['market_name'],
         "drtitle":buff_price['en_name'],
         "totalSales":int(total_sales),
         "date":datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d'),
         "dmarket_sale_Price":round(float(avg_price)*exchange_rate,2),
         "offer_price":round(offer_price,2),
         "target_price":target_price,
         "target_account":target_account,
         "buff_avg_price":buff_avg_price,
         "buff_statistic":buff_statistic,
         "buff_sum_price":buff_sum_price,

     

        
        # # buff直接购买出售的，dmarket平均价格直接出售
        #  "buff_buy_dm_sale_avg": round(float(avg_price)*exchange_rate*bank_rate*trans_dm_service_change(price=float(avg_price)*exchange_rate)- buff_avg_price, 2),
        #  "buff_buy_dm_sale_avg_rate": round((float(avg_price)*exchange_rate*bank_rate*trans_dm_service_change(price=float(avg_price)*exchange_rate)- buff_avg_price)/buff_avg_price,3),

        # # buff直接购买的，dmarket直接的当前价格出售
        #  "buff_buy_dm_sale_min": round(float(offer_price)*bank_rate*trans_dm_service_change(price=offer_price)- offer_price, 2),
        #  "buff_buy_dm_sale_min_rate": round((float(offer_price)*bank_rate*trans_dm_service_change(price=offer_price)- offer_price)/offer_price,3),

     
        # dmarket平均价购买出售，buff直接出售
        "dm_buy_buff_sale_avg": round(buff_avg_price*trans_buff_service_change()-float(avg_price)*exchange_rate*recharge_rate, 2),
        "dm_buy_buff_sale_avg_rate": round((buff_avg_price*trans_buff_service_change()-float(avg_price)*exchange_rate*recharge_rate)/buff_avg_price,3),
       
        "dm_buy_buff_sale_seven_rate": round((buff_avg_price*trans_buff_service_change()-float(avg_price)*exchange_rate*recharge_rate)/buff_avg_price,3)-price_alter_percentage_7d,


        # dmarket最低价购买出售，buff直接出售
         "dm_buy_buff_sale_min": round(buff_avg_price*trans_buff_service_change()-offer_price*recharge_rate, 2),
         "dm_buy_buff_sale_min_rate": round((buff_avg_price*trans_buff_service_change()-offer_price*recharge_rate)/offer_price,2),

        
        "buy_max_price":buy_max_price,
        "buy_max_num":buy_max_num,
        "price_alter_percentage_7d":price_alter_percentage_7d,
        "price_alter_value_7d":price_alter_value_7d,
        "category_group_name":category_group_name,
        "buy_it_now":0,
        "buy_it":0,
        "buy_it_num":0,
        "us_price":key_info['us_price'] ,

        # "current_target_price":current_target_price,
        # "current_target_amount":current_target_amount,
        # "current_target_createdAt":current_target_createdAt,

        
        
        # dmarket采购价和buff出售价的差价和利润
        #  "current_target_price_diff": round(buff_avg_price*trans_buff_service_change()-target_price*recharge_rate, 2),
        #  "current_target_price_diff_rate": round((buff_avg_price*trans_buff_service_change()-target_price*recharge_rate)/target_price,2),
        #  "current_target_price_diff_avg": round(target_price*recharge_rate-float(avg_price)*recharge_rate, 2),

        

         }
        for total_sales,date,avg_price in zip(market_price["totalSales"],market_price["date"],market_price["avgPrice"])
    ]

    # all_correlationd_num=0
    # for i in correlationd_data:
    #     all_correlationd_num+=i["totalSales"]

    # avarage_num=all_correlationd_num/int(searchNum)
    # if avarage_num>filter_num:
    #     filter_list.extend(correlationd_data);

    # all_list.extend(correlationd_data);
    return correlationd_data




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



# # 获取最采购高价和出售最低价
# # 获取当前的采购饰品情况
# def get_my_target_List(exchange_rate=7.14):
#     target_list=[]
#     try:
#         # 设置请求的URL
#         url = 'https://api.dmarket.com/exchange/v1/user/targets'
#         # 设置请求头
#         headers = {
#             'accept': 'application/json, text/plain, */*',
#             'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmNjk0NjQzNy0wN2ZlLTRhMWYtOTMxYi1jN2JiZmYzMzdlMWEiLCJleHAiOjE3MjYwNTU4MTQsImlhdCI6MTcyMzQ2MzgxNCwic2lkIjoiNDM1ZTEzMTMtNjEyOC00OGY4LWEyNmEtMTA3YmVlMTRiMWIzIiwidHlwIjoiYWNjZXNzIiwiaWQiOiI0MWU0Y2RlZC1hMDcxLTRiMDUtODRjYS1lYzM2OWEzZjYyZjUiLCJwdmQiOiJyZWd1bGFyIiwicHJ0IjoiMjQwOCIsImF0dHJpYnV0ZXMiOnsid2FsbGV0X2lkIjoiZjg1MTM4Yjc0NWFiNGIyY2FjNTY3ZTFmMDVmN2VmNGZlNDJjMTUzYzJkMTg0NDM1Yjg2OTk3ODNkMDljOTgxNSIsInNhZ2Ffd2FsbGV0X2FkZHJlc3MiOiIweEM3OWZlMzhjM0I4MzJkODU2ZDJGMUVmQTBGYzAwRUUzMThBOTM2NjQiLCJhY2NvdW50X2lkIjoiODZhZmQxZmYtMDVlOC00NzM5LTkzNmQtN2I2NWUwOWQ3ODVlIn19.Bnig8ltKoIqd8XHScE5RlDjBC3yRh5DYMdabUJibWD1In5MQTrnTngYBUbioXrRsHzxDZWThoEOpKqQhd5_-mQ',
#             'accept-language': 'zh-CN,zh;q=0.9',
#             'content-type': 'application/json',
#             'jkkat': '50788078',
#             'language': 'ZH',
#             'origin': 'https://dmarket.com',
#             'payment-session-id': '77af0392-9f37-40c8-9e68-4bbaf9f5cf00',
#             'priority': 'u=1, i',
#             'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'same-site',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
#         }
#         # 设置请求的数据
#         params = {
#             "gameId": "a8db",
#             "limit": 100,
#             "currency": "USD",
#             "platform": "browser",
#             "priceTo": 0,
#             "priceFrom": 0,
#             "orderDir": "desc",
#             "orderBy": "updated",
#             "side": "user"
#         }

#         # 发送POST请求
#         response = requests.get(url, params=params,headers=headers)
#         reponse_json = json.loads(response.text)
#         offers=reponse_json['objects']
#         for offer in offers:
#             target={}
#             target['title']=offer['title']
#             target['amount']=offer['amount']
#             target['price']=round(float(offer['price']['USD'])/100*exchange_rate,2)
#             target['createdAt']=datetime.fromtimestamp(int(offer['createdAt'])).strftime('%Y-%m-%d')
#             target_list.append(target)
            
#     except Exception as e:
#         print(e)
#         return None
#     return target_list




# 获取最采购高价和出售最低价
def get_target_market(title,exchange_rate):
    key_info={}
    try:
        # 设置请求的URL
        url = 'https://api.dmarket.com/exchange/v1/appraise/targets'
        # 设置请求头
        headers = {
            'authorization': 'eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJjZGEyZDg5OS1iNWZkLTRiMmEtODVhNC05MzI4MjY4ZWEyYjYiLCJleHAiOjE3MjYyMzM1NzUsImlhdCI6MTcyMzY0MTU3NSwic2lkIjoiODE0ZDhkZTktMzJiYy00NzFjLWI3OWMtNDkyMzc1MDAzZmI5IiwidHlwIjoiYWNjZXNzIiwiaWQiOiJiYjNmNTkyZS03ZWEwLTQ2ZDQtODYzMS1lNTk5ODE2YzI4ZjMiLCJwdmQiOiJyZWd1bGFyIiwicHJ0IjoiMjQwOCIsImF0dHJpYnV0ZXMiOnsiYWNjb3VudF9pZCI6IjUxYjU0MjYzLTFhZGYtNDJlZS04OWNlLThmZGE2M2YzNDFkYiIsIndhbGxldF9pZCI6IjdkZWY1ZGU1MTI0NTQ0ZjZiOTA3Y2ZiNWIyNDcwZTc4YThjY2RkYzRlMDk2NDNhNmFmYjVmMWNjZmZhMGE2ZGEiLCJzYWdhX3dhbGxldF9hZGRyZXNzIjoiMHg3ZmRmMmQwRWVhMDE3RTYxYTc4OTI4YmQyNDdDNzJjOTQ1NkE5ZUU1In19.W4yu4Dz1Bvzb5AKJCrwHpPkkBjR2b1LB9lYliiYrShsotsJ8KnBBO5TSQ9Jdmsp-QMp1ibX9euowVlEF9q97oA',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'jkkat': 'cde0c75',
            'language': 'ZH',
            'origin': 'https://dmarket.com',
            'payment-session-id': '5c4ea682-e877-4309-b231-c5cabdb684d8',
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
        data = {
            "gameId": "a8db",
            "objects": [{"title": title}]
        }
        # 发送POST请求
        response = requests.post(url, headers=headers, json=data)
        reponse_json = json.loads(response.text)
        offers=reponse_json['objects']
        prices=offers[0]['stats']['prices']

        for price in prices:
            if price['name'] == 'maxTargetPrice':
                key_info['target_price']=round(float(price['amount'])/100*exchange_rate,3)
            elif price['name'] =='minOfferPrice':
                key_info['offer_price']=round(float(price['amount'])/100*exchange_rate,3)
                key_info['us_price']=price['amount']
        key_info['target_account']=offers[0]['stats']['totalTargets']
        return key_info
    except Exception as e:
        print(e)
        key_info['target_price'] =0.01
        key_info['target_account']=0.01
        key_info['offer_price']=0.01
        key_info['us_price']=0.01
        return key_info
# skins=get_skin_title()




def process_file_in_threads(thread_size,exchange_rate,target_list):
    origin_file_path=data_path+skin_86_path
    target_file_path=data_path+"/analysis/skin_86_filter_file.txt"

    if os.path.exists(target_file_path):
        os.remove(target_file_path)
        open(target_file_path,'w',encoding='utf-8')
    else:
        open(target_file_path,'w',encoding='utf-8')
    
    # 读取文件A的所有行
    with open(origin_file_path, 'r',encoding='utf-8') as fileA:
        lines = fileA.readlines()

    # 过滤印花
    filter_list=[]
    for line in lines:
        if "印花" not in line and '涂鸦' not in line :
            filter_list.append(line)




    chunk_size = len(filter_list) // thread_size  # 这里除以线程数10


    # 创建线程列表
    threads = []

    # 分割数据并创建线程
    for i in range(thread_size):
        # 计算每个线程的起始和结束索引
        start = i * chunk_size
        end = start + chunk_size if i < thread_size+1 else len(filter_list)
        print(f"线程{i}处理数据: {start} - {end}")
        # 获取对应的数据批次
        chunks = filter_list[start:end]
        
        # 创建线程
        thread = threading.Thread(target=process_line, args=(chunks,exchange_rate,target_list,target_file_path))
        threads.append(thread)
        thread.start()  # 启动线程


    # 等待所有线程完成
    for thread in threads:
        thread.join()

# 锁，用于同步写入文件B
write_lock = threading.Lock()

def process_line(chunks,exchange_rate,target_list,target_file_path):
    # print(threading.current_thread().name+"开始处理数据")

    
    for line in chunks:
        try:
            # 解析每一行中的JSON对象
            skin_json=json.loads(line.replace("\\b",""))
            # 只获取cs的饰品数据名称
            all_names=skin_json['market_name']+':'+skin_json['en_name']
            print(threading.current_thread().name+"开始查询---"+all_names)
            time.sleep(1)
            market_price = get_offer_from_market_average(day=searchNum+searchUnit,title=skin_json['en_name'])
            # key_info=get_current_market(limit="10",title=base_filter_line_date['en_name'])
            target_info=get_target_market(title=skin_json['en_name'],exchange_rate=exchange_rate)
            # print(threading.current_thread().name+":"+str(target_info))
            correlationd_data=build_target_body_from_offer_avarage(buff_price=skin_json,market_price=market_price,key_info=target_info,exchange_rate=exchange_rate,target_list=target_list)
            

                # #平均价购买，判断 0.5<当前价<5 且 当前价率>0.2 且小于1   当前价购买了，评价就不去购买了
                # create_target=correlationd_data[len(correlationd_data)-1]
                # buy_it_num=1
                # if not_buy_it_exist and create_target['offer_price']>0.5 and create_target['offer_price']<5 and create_target['dm_buy_buff_sale_avg_rate']>0.20 and create_target['dm_buy_buff_sale_avg_rate']<1 :
                #     print(threading.current_thread().name+"开始购买---"+all_names+"价格是："+str(create_target['offer_price'])+"利率润是："+str(create_target['dm_buy_buff_sale_avg_rate']))
                #     offer_buy_product.build_target_body_from_offer(price=target_info["us_price"],amount=buy_it_num,title=create_target["drtitle"])
                #     correlationd_data[len(correlationd_data)-1]['buy_it']=create_target['offer_price']
                #     correlationd_data[len(correlationd_data)-1]['buy_it_num']=buy_it_num

            # 写入结果到文件B
            with write_lock:
                with open(target_file_path, 'a',encoding='utf-8') as fileB:
                    fileB.write(json.dumps(correlationd_data,ensure_ascii=False)+"\n")

        except json.JSONDecodeError as e:
            print(f"JSON 解码错误: {e}")
        except Exception as e:
            print(f"请求处理中发生错误: {e}")



# def find_buff_dmarket_price(exchange_rate,target_list):
#     print("开始查询数dmarket据")

    
#     with open(data_path+skin_86_path, "r", encoding='utf-8') as skin_86_file:
#         with open(data_path+"/analysis/skin_86_filter_file.txt", "w", encoding='utf-8') as skin_86__filter_file:
#             for skin_line in skin_86_file:
#                 skin_json=json.loads(skin_line.replace("\\b",""))
            
#                 # 只获取cs的饰品数据名称
#                 all_names=skin_json['market_name']+':'+skin_json['en_name']
#                 print("开始查询---"+all_names)

#                 time.sleep(1)
#                 market_price = get_offer_from_market_average(day=searchNum+searchUnit,title=skin_json['en_name'])
#                 # key_info=get_current_market(limit="10",title=base_filter_line_date['en_name'])
#                 target_info=get_target_market(title=skin_json['en_name'],exchange_rate=exchange_rate)
#                 print(target_info)
#                 correlationd_data=build_target_body_from_offer_avarage(buff_price=skin_json,market_price=market_price,key_info=target_info,exchange_rate=exchange_rate,target_list=target_list)
#                 skin_86__filter_file.write(json.dumps(correlationd_data,ensure_ascii=False)+"\n")

        # 定义中文名和字段样式
chinese_columns = {
    "title":'中文名',
    "drtitle":'英文名',
    "totalSales":'销售数量',
    "date":'日期',
    "dmarket_sale_Price":'平均购买价',
    "offer_price":'当前出售价',
    "target_price":'当前采购价',
    "target_account":'当前采购数量',
    "buff_avg_price":'buff在售价',
    "buff_statistic":'buff在售数量',
    "buff_sum_price":'buff总交易额度',
    "buff_updated_at":'buff数据更新时间',

    "buy_max_price":'buff购买价格',
    "buy_max_num":'buff购买数量',
    "price_alter_percentage_7d":'buff-7天价格变化率',
    "price_alter_value_7d":'buff-7天价格变化价格',
    "category_group_name":'饰品类型',

# # buff直接购买出售的，dmarket平均价格直接出售
#     "buff_buy_dm_sale_avg": 'buff购买dm出售-平均价',
#     "buff_buy_dm_sale_avg_rate": 'buff购买dm出售-平均价率',

# # buff直接购买的，dmarket直接的当前价格出售
#     "buff_buy_dm_sale_min": 'buff购买dm出售-当前价',
#     "buff_buy_dm_sale_min_rate": 'buff购买dm出售-当前价',


# dmarket平均价购买出售，buff直接出售
    "dm_buy_buff_sale_avg": 'dm购买buff出售-平均价',
    "dm_buy_buff_sale_avg_rate": 'dm购买buff出售-平均价率',

    "dm_buy_buff_sale_seven_rate": 'dm购买buff出售-7天净变化率',

# dmarket最低价购买出售，buff直接出售
    "dm_buy_buff_sale_min": 'dm购买buff出售-当前价',
    "dm_buy_buff_sale_min_rate": 'dm购买buff出售-当前价率',
    "buy_it_now": '是否购买',
    "buy_it": '当前价购买',
    "buy_it_num": '购买数量',
    "us_price": '购买金额-美元',


    #  "current_target_price":'当前采购价',
    # "current_target_amount":'当前采购数量',
    # "current_target_createdAt":'创建时间',

    # "current_target_price_diff":'当前采购价盈利',
    # "current_target_price_diff_rate":'当前采购价盈利率',
    # "current_target_price_diff_avg":'当前采购价和平均价的差价',

}



# 一行一行的读取json数组，并写入到excel中
def export_market_data():
    print("开始创建采购单数据")
    filename=data_path+"/excel/"+"dmakert_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    all_data=[]


    # 打开文件准备读取
    with open(data_path+'/analysis/skin_86_filter_file.txt', 'r', encoding='utf-8') as file:
       for line in file:
           json_data=json.loads(line.replace("\\b",""))
           for single in json_data:
                all_data.append(single)
    export_json_to_excel(all_data,filename)



    # 完成后关闭文件
    # workbook.close()

# 获取美元汇率
def find_us_exchange(): 
    try:
            # 设置API endpoint
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        # 发起GET请求
        response = requests.get(url)
        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()
            # 打印所有汇率
            rates = data['rates']
            for currency, rate in rates.items():
                if currency == 'CNY':
                    exchange_rate=float(rate)
                    return  exchange_rate
    except Exception as e:
        print(e)

    return 7.20

def get_buff_data_file_name(dir_name):
    try:
            # 设置API endpoint
        url = "https://api.iflow.work/export/list?dir_name="+dir_name
        # 发起GET请求
        response = requests.get(url)
        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()
            files=data['files']
            new_file=files[len(files)-1]
            return new_file
    except Exception as e:
        print(e)
    

def down_buff_zip_file(dir_name,file_name):
    print("开始下载buff数据,dir_name:"+dir_name+",file_name:"+file_name)
    try:
            # 设置API endpoint
        key="M04VML9CQ683EA47X2E5"
        url = "https://api.iflow.work/export/download"
        params = {
            'dir_name': dir_name,
            'file_name': file_name,
            'key': key
        }
                # 下载文件的临时路径
        temp_file_path = data_path+"/zip/temp.zip"

        # 最终保存的文件名
        final_file_name=data_path+"/zip/"+"buff_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".zip"
        
        # 解压缩到的目标文件夹
        extract_dir = data_path+"/analysis/"
        extract_file = "1_cs_buff_uu_c5_base.json"
        file_path = os.path.join(extract_dir, extract_file)

        zip_json_path = os.path.join(extract_dir, file_name.replace(".zip", ".json"))
        

        # 发送GET请求并下载文件
        response = requests.get(url, params=params, stream=True)
        if response.status_code == 200:
            # 以二进制写模式打开文件，并写入内容
            with open(temp_file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            # 重命名文件
            shutil.move(temp_file_path, final_file_name)
            
            # 解压文件
            with ZipFile(final_file_name, 'r') as zip_ref:
                # 如果extract_dir已经存在，先清空该文件夹
                # if os.path.exists(file_path):
                #     shutil.rmtree(file_path)
                #     print('该文件已存在，删除：'+extract_file)
                
                # 解压文件到指定文件夹，并覆盖已有文件
                zip_ref.extractall(extract_dir)
                shutil.move(zip_json_path, file_path)
        else:
            print(f"Failed to download file, status code: {response.status_code}")

        print("Download and extraction complete.")
    except Exception as e:
        print(e)




# 一行一行的读取json数组，并写入到excel中
def create_avg_target_avg(exchange_rate,limit):
    print("开始创建采购单数据-平均价")
    
    all_data=[]
    filter_data=[]
    create_target_list=[]

    create_num=0
    # 打开文件准备读取
    with open(data_path+'/analysis/skin_86_filter_file.txt', 'r', encoding='utf-8') as file:
       for line in file:
           json_data=json.loads(line.replace("\\b",""))
           if len(json_data)>0:
                json_data.sort(key=lambda x:datetime.strptime(x['date'], "%Y-%m-%d"),reverse=True)
                
                # 判断是否有符合条件的
                for create_target in json_data:
                    if create_target['totalSales']>=3 :
                        #当前价购买，判断 0.5<当前价<3 且 当前价率>0.15 且小于1 
                        buy_flag=False
                        buy_it_num=1
                        us_price= int(round(create_target['dmarket_sale_Price']/exchange_rate*100,0))

                        if create_target['dmarket_sale_Price']>1 and create_target['dmarket_sale_Price']<5 and create_target['dm_buy_buff_sale_avg_rate']>0.2 and create_target['price_alter_percentage_7d']<20:
                            buy_flag=True
                            us_price= us_price+1
                            buy_it_num=10
                        elif create_target['dmarket_sale_Price']>=5 and create_target['dmarket_sale_Price']<15 and create_target['dm_buy_buff_sale_avg_rate']>0.15  and create_target['price_alter_percentage_7d']<20:
                            buy_flag=True
                            us_price= us_price+3
                            buy_it_num=2
                        elif create_target['dmarket_sale_Price']>=15 and create_target['dmarket_sale_Price']<50 and create_target['dm_buy_buff_sale_avg_rate']>0.10  and create_target['price_alter_percentage_7d']<10 :
                            buy_flag=True
                            us_price= us_price+10
                            buy_it_num=1

                        # 比平均价高0.01美金
                        if buy_flag:   
                            create_target['buy_it_num']=buy_it_num
                            create_target['us_price']=us_price
                            create_target['buy_it']=round(us_price/100*exchange_rate,2)
                            create_target_list.append(create_target)
                            break
    filename=data_path+"/excel/"+"creat_target_avg_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    creat_now(create_target_list,filename,limit,"avg")
    


# 一行一行的读取json数组，并写入到excel中
def create_avg_target_min(exchange_rate,limit):
    print("开始创建采购单数据-最低价")
    
    all_data=[]
    filter_data=[]
    create_target_list=[]

    create_num=0
    # 打开文件准备读取
    with open(data_path+'/analysis/skin_86_filter_file.txt', 'r', encoding='utf-8') as file:
       for line in file:
           json_data=json.loads(line.replace("\\b",""))
           if len(json_data)>0:
                json_data.sort(key=lambda x:datetime.strptime(x['date'], "%Y-%m-%d"),reverse=True)
                
                # 判断是否有符合条件的
                for create_target in json_data:
                    if create_target['totalSales']>=3 :
                        #当前价购买，判断 0.5<当前价<3 且 当前价率>0.15 且小于1 
                        buy_flag=False
                        buy_it_num=1
                        us_price= int(round(create_target['offer_price']/exchange_rate*100,0))

                        if create_target['offer_price']>1 and create_target['offer_price']<5 and create_target['dm_buy_buff_sale_min_rate']>0.1 and create_target['price_alter_percentage_7d']<20:
                            buy_flag=True
                            us_price= us_price+1
                            buy_it_num=1
                        elif create_target['offer_price']>=5 and create_target['offer_price']<15 and create_target['dm_buy_buff_sale_min_rate']>0.1  and create_target['price_alter_percentage_7d']<15:
                            buy_flag=True
                            us_price= us_price+3
                            buy_it_num=1
                        elif create_target['offer_price']>=15 and create_target['offer_price']<50 and create_target['dm_buy_buff_sale_min_rate']>0.10  and create_target['price_alter_percentage_7d']<10 :
                            buy_flag=True
                            us_price= us_price+10
                            buy_it_num=1

                        # 比平均价高0.01美金
                        if buy_flag:   
                            create_target['buy_it_num']=buy_it_num
                            create_target['us_price']=us_price
                            create_target['buy_it']=round(us_price/100*exchange_rate,2)
                            create_target_list.append(create_target)
                            break
    filename=data_path+"/excel/"+"creat_target_min_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    creat_now(create_target_list,filename,limit,"min")



def creat_now(create_target_list,filename,limit,type):
    create_num=1
    for now_target in create_target_list:
        if '探员' in now_target['title']:
            print("跳过探员不购买："+now_target['title'])
            continue

        if create_num>=limit:
            print("已经创建采购单数量达到"+str(limit)+"个，退出循环")
            break
        time.sleep(1)
        create_num=create_num+1

        if "avg" in type:
            print(threading.current_thread().name+"开始购买---"+now_target['title']+"购买价格是："+str(now_target['buy_it'])+"，销售价是："+ str(now_target['buff_avg_price']) +",利率润是："+str(now_target['dm_buy_buff_sale_avg_rate']))
        else:
            print(threading.current_thread().name+"开始购买---"+now_target['title']+"购买价格是："+str(now_target['buy_it'])+"，销售价是："+ str(now_target['buff_avg_price']) +",利率润是："+str(now_target['dm_buy_buff_sale_min_rate']))

        offer_buy_product.build_target_body_from_offer(price=str(now_target['us_price']),amount=now_target['buy_it_num'],title=now_target["drtitle"])
        now_target['buy_it_now']=1
        now_target['buy_it_now']=now_target['buy_it_num']
    export_json_to_excel(create_target_list,filename)
               


def export_json_to_excel(all_data,filename):
    print("开始导出数据到excel")
    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(all_data)
    # 写入Excel文件
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        # 获取工作簿和工作表对象
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        # 定义加粗和颜色格式
        bold_format = workbook.add_format({'bold': True})
        yellow_format = workbook.add_format({'bold': True, 'bg_color': '#ffff00'})  # 黄色背景色代码
        buff_format = workbook.add_format({'bold': True, 'bg_color': '#c7b5c2'}) 
        cul_format = workbook.add_format({'bold': True, 'bg_color': '#85b05f'})  
        #指定列 设置黄色背景
        yellow_format_columns={'dmarket_sale_Price','offer_price','target_account'}
        buff_format_columns={'buff_avg_price','buff_statistic','buff_sum_price'}
        cul_format_columns={'dm_buy_buff_sale_avg','dm_buy_buff_sale_min','dm_buy_buff_sale_seven_rate'}
                # 设置列标题的中文名和样式
        for col_num, value in enumerate(df.columns.values):
            # 设置列宽
            column_width = 9  # 你可以根据需要调整这个值
            worksheet.set_column(col_num, col_num, column_width)

            # 设置中文名
            if value in yellow_format_columns:
                worksheet.write(0, col_num, chinese_columns[value], yellow_format)
            elif value in buff_format_columns:
                worksheet.write(0, col_num, chinese_columns[value], buff_format)
            elif value in cul_format_columns:
                worksheet.write(0, col_num, chinese_columns[value], cul_format)
            else:
                worksheet.write(0, col_num, chinese_columns[value], bold_format)




if __name__ == '__main__':
    start_time=int(time.time())
    buff_file=data_path+skin_86_path
    # 初始化数据
    # Skin86BaseData.get_skin_86_market_all(file_name=buff_file,limit_page=500,page=1,page_size=100,price_start=1,price_end=500,selling_num_start=200)


    exchange_rate=find_us_exchange()
    
    print("当前的美元汇率是："+str(exchange_rate))

    # thread_size=5
    # process_file_in_threads(thread_size,exchange_rate,None)

    # #导出市场数据
    # export_market_data()

    # user_input = input("程序运行中 键入quit退出\n")
    #     # 当用户输入"quit"后，等待线程完成
    # if user_input == "quit":
    #     print("程序执行完当前轮之后将退出")
    #     exit()

    # while True:
    #     print("等待执行中")
    #     time.sleep(360)  # 暂停 1 小时（360 秒）
    #     print("开始执行数据"+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #     create_avg_target_min(exchange_rate,100)
        

    create_avg_target_min(exchange_rate,100)
    create_avg_target_avg(exchange_rate,50)
    end_time=int(time.time())
    print("运行时间："+str(end_time-start_time))
    # create_avg_target_now(exchange_rate,20)




