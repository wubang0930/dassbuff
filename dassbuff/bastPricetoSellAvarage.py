import json
from datetime import datetime

import pandas as pd
import requests
from datetime import datetime
import time
import os
import shutil
from zipfile import ZipFile

import config

# change url to prod
rootApiUrl = "https://api.dmarket.com"
# exchange_rate=7.19   #实际汇率
recharge_rate=1.027   #充值手续费
bank_rate=0.985   #实际汇率*实际提现到手
steam_exchange_rate=0.7   #实际汇率*实际提现到手
searchNum="7"  #查询天数
searchUnit="D"  #查询单位

all_list=[]

data_path="E:/pythonFile/python/python_data/dassbuff/data"

filter_num=30   #过滤平均销量大于30的数量
filter_list=[]   #过滤平均销量大于30的列表

def get_skin_title():  
    # skins={"千瓦武器箱":"Kilowatt Case","梦魇武器箱":"Dreams%20%26%20Nightmares%20Case","英勇大行动":"Operation Bravo Case"}
    skins={"千瓦武器箱":"Kilowatt Case","变革武器箱":"Revolution Case","反冲武器箱":"Recoil Case","梦魇武器箱":"Dreams & Nightmares Case","“激流大行动”武器箱":"Operation Riptide Case","蛇咬武器箱":"Snakebite Case","“狂牙大行动”武器箱":"Operation Broken Fang Case","裂空武器箱":"Fracture Case","棱彩2号武器箱":"Prisma 2 Case","裂网大行动武器箱":"Shattered Web Case","反恐精英20周年武器箱":"CS20 Case","棱彩武器箱":"Prisma Case","命悬一线武器箱":"Clutch Case","地平线武器箱":"Horizon Case","“头号特训”武器箱":"Danger Zone Case","光谱2号武器箱":"Spectrum 2 Case","九头蛇大行动武器箱":"Operation Hydra Case","光谱武器箱":"Spectrum Case","手套武器箱":"Glove Case","伽马2号武器箱":"Gamma 2 Case","伽马武器箱":"Gamma Case","CS:GO武器箱":"CS:GO Weapon Case","CS:GO2号武器箱":"CS:GO Weapon Case 2","CS:GO3号武器箱":"CS:GO Weapon Case 3","幻彩武器箱":"Chroma Case","幻彩2号武器箱":"Chroma 2 Case","幻彩3号武器箱":"Chroma 3 Case","电竞2013武器箱":"eSports 2013 Case","电竞2013冬季武器箱":"eSports 2013 Winter Case","电竞2014夏季武器箱":"eSports 2014 Summer Case","弯曲猎手武器箱":"Falchion Case","猎杀者武器箱":"Huntsman Weapon Case","英勇大行动武器箱":"Operation Bravo Case","突围大行动":"Operation Breakout Weapon Case","凤凰大行动武器箱":"Operation Phoenix Weapon Case","先锋大行动武器箱":"Operation Vanguard Weapon Case","野火大行动武器箱":"Operation Wildfire Weapon Case","左轮武器箱武器箱":"Revolver Case","暗影武器箱":"Shadow Case","冬季攻势武器箱":"Winter Offensive Weapon Case"}
    return skins



def get_current_market(limit,title):
    key_info={}
    try:
        market_response = requests.get(rootApiUrl + "/exchange/v1/market/items?side=market&orderBy=price&orderDir=desc&title="+title+"&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&myFavorites=false&types=dmarket&cursor=&limit="+limit+"&currency=USD&platform=browser&isLoggedIn=false")
        reponse_json = json.loads(market_response.text)

        offers=reponse_json['objects']

        all_price=[]
        for offer in offers:
            all_price.append(round(float(offer['price']['USD'])/100*exchange_rate,2))
        
        print(all_price)
        # f= open("offer_avarage.json","w")
        # f.write(json.dumps(offers))
        # f.close()
        # print(offers)   
        key_info['price']=min(all_price)
        key_info['items']=reponse_json['total']['items']
        return key_info
    except Exception as e:
        print(e)
        key_info['price']=0
        key_info['items']=0
        return key_info
    

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
        key_info['target_account']=offers[0]['stats']['totalTargets']
        return key_info
    except Exception as e:
        print(e)
        key_info['target_price'] =0
        key_info['target_account']=0
        key_info['offer_price']=0
        return key_info


def get_offer_from_market_average(day,title):
    try:
        market_response = requests.get(rootApiUrl + "/trade-aggregator/v1/avg-sales-graph?gameId=a8db&period="+day+"&title="+title)
        offers = json.loads(market_response.text)
        # f= open("offer_avarage.json","w")
        # f.write(json.dumps(offers))
        # f.close()
        # print(offers)   
        return offers
    except Exception as e:
        print(e)
        return None




# 查询指定天数的平均销量数据，并构建目标数据
def build_target_body_from_offer_avarage(buff_price,market_price,key_info,exchange_rate):
    #
    if market_price is None:
        return ""


    buff_buy_price= buff_price['buff_buy']['price']
    buff_sale_price= buff_price['buff_sell']['price']
    buff_buy_count= buff_price['buff_buy']['count'] if buff_price['buff_buy']['count'] is not None else 0
    buff_sale_count= buff_price['buff_sell']['count'] if buff_price['buff_sell']['count'] is not None else 0

    c5_buy_price= buff_price['c5_buy']['price']
    c5_sale_price= buff_price['c5_sell']['price']
    c5_buy_count= buff_price['c5_buy']['count'] if buff_price['c5_buy']['count'] is not None else 0
    c5_sale_count= buff_price['c5_sell']['count'] if buff_price['c5_sell']['count'] is not None else 0

    igxe_buy_price= buff_price['igxe_buy']['price']
    igxe_sale_price= buff_price['igxe_sell']['price']
    igxe_buy_count= buff_price['igxe_buy']['count'] if buff_price['igxe_buy']['count'] is not None else 0
    igxe_sale_count= buff_price['igxe_sell']['count'] if buff_price['igxe_sell']['count'] is not None else 0


    uuyp_buy_price= buff_price['uuyp_buy']['price']
    uuyp_sale_price= buff_price['uuyp_sell']['price']
    uuyp_buy_count= buff_price['uuyp_buy']['count'] if buff_price['uuyp_buy']['count'] is not None else 0
    uuyp_sale_count= buff_price['uuyp_sell']['count'] if buff_price['uuyp_sell']['count'] is not None else 0


    steam_buy_price= buff_price['steam_order']['buy_price']  if buff_price.get('steam_order', {}).get('buy_price') is not None else 99999
    steam_sale_price= buff_price['steam_order']['sell_price']  if buff_price.get('steam_order', {}).get('sell_price') is not None else 99999
    steam_buy_count= buff_price['steam_order']['buy_order_count']  if buff_price.get('steam_order', {}).get('buy_order_count') is not None else 99999
    steam_sale_count= buff_price['steam_order']['sell_order_count']  if buff_price.get('steam_order', {}).get('sell_order_count') is not None else 99999


    buy_prices=[buff_buy_price,c5_buy_price,igxe_buy_price,uuyp_buy_price]
    sale_prices=[buff_sale_price,c5_sale_price,igxe_sale_price,uuyp_sale_price]
    max_sale_price_num_all=[buff_sale_count,c5_sale_count,igxe_sale_count,uuyp_sale_count]


    buy_prices_none=[price for price in buy_prices if price is not None]
    sale_prices_none=[price for price in sale_prices if price is not None]
    sale_price_num_all_none=[price for price in max_sale_price_num_all if price is not None]

    min_buy_price=min(buy_prices_none) if buy_prices_none else -99999
    min_sale_price=min(sale_prices_none) if sale_prices_none else -99999
    
    max_buy_price=max(buy_prices_none) if buy_prices_none else 99999
    max_sale_price=max(sale_prices_none) if sale_prices_none else 99999


    max_sale_price_num=max(sale_price_num_all_none) if sale_price_num_all_none else 99999


    offer_price=key_info['offer_price'] if key_info['offer_price'] is not None else 999999
    target_price=key_info['target_price'] if key_info['target_price'] is not None else 999999
    target_account=key_info['target_account'] if key_info['target_account'] is not None else 999999

    correlationd_data=[
        {"title":buff_price['cn_name'],
         "drtitle":buff_price['en_name'],
         "totalSales":int(total_sales),
         "date":datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d'),
         "dmarket_sale_Price":round(float(avg_price)*exchange_rate,2),
         "dmarket_buy_Price":round(float(avg_price)*exchange_rate*bank_rate,2),
         "offer_price":offer_price,
         "target_price":target_price,
         "target_account":target_account,
         "dayTotalAmount":round(float(total_sales)*float(avg_price)*exchange_rate,2),
         "buff_buy_price":buff_buy_price,
         "buff_buy_count":buff_buy_count,
         "buff_sale_price":buff_sale_price,
         "buff_sale_count":buff_sale_count,
        #  "c5_buy_price":c5_buy_price,
        #  "c5_buy_count":c5_buy_count,
        #  "c5_sale_price":c5_sale_price,
        #  "c5_sale_count":c5_sale_count,
         "igxe_buy_price":igxe_buy_price,
         "igxe_buy_count":igxe_buy_count,
         "igxe_sale_price":igxe_sale_price,
         "igxe_sale_count":igxe_sale_count,
         "uuyp_buy_price":uuyp_buy_price,
         "uuyp_buy_count":uuyp_buy_count,
         "uuyp_sale_price":uuyp_sale_price,
         "uuyp_sale_count":uuyp_sale_count,
         "steam_buy_price":steam_buy_price,
         "steam_sale_price":steam_sale_price,
         "steam_buy_count":steam_buy_count,
         "steam_sale_count":steam_sale_count,
         "min_buy_price":min_buy_price,
         "min_sale_price":min_sale_price,
         "max_sale_price_num_all":max_sale_price_num_all,
         "max_sale_price_num":max_sale_price_num,
         "max_buy_price":max_buy_price,
         "max_sale_price":max_sale_price,


        # buff直接购买出售的，dmarket平均价格直接出售
         "buff_buy_max_dmarket_sale_min": round(float(avg_price)*exchange_rate*bank_rate*trans_dm_service_change(price=min_sale_price)- min_sale_price, 2),
         "buff_buy_max_dmarket_sale_min_rate": round((float(avg_price)*exchange_rate*bank_rate*trans_dm_service_change(price=min_sale_price)- min_sale_price)/min_buy_price,3),

        # buff直接购买的，dmarket直接的当前价格出售
         "buff_buy_max_dmarket_sale_current": round(float(offer_price)*bank_rate*trans_dm_service_change(price=offer_price)- min_sale_price, 2),
         "buff_buy_max_dmarket_sale_current_rate": round((float(offer_price)*bank_rate*trans_dm_service_change(price=offer_price)- min_sale_price)/min_buy_price,3),

         
        # # buff挂采购单，然后dmarket最低价出售
        #  "buff_buy_min_dmarket_sale_min": round(float(avg_price)*exchange_rate*bank_rate*trans_dm_service_change(price=max_sale_price)- max_sale_price, 2),
        #  "buff_buy_min_dmarket_sale_min_rate": "{:.1f}%".format((float(avg_price)*exchange_rate*bank_rate*trans_dm_service_change(price=max_sale_price)- max_sale_price)/min_buy_price*100),


        # dmarket直接购买出售，buff直接出售
         "dmarket_buy_min_buff_sale_max": round(min_sale_price*trans_buff_service_change()-offer_price*recharge_rate, 2),
         "dmarket_buy_min_buff_sale_max_rate": round((min_sale_price*trans_buff_service_change()-offer_price*recharge_rate)/min_sale_price,3),


        # dmarket采购单，buff直接出售
         "dmarket_target_min_buff_sale_max": round(min_sale_price*trans_buff_service_change()-target_price*recharge_rate, 2),
         "dmarket_target_min_buff_sale_max_rate": round((min_sale_price*trans_buff_service_change()-target_price*recharge_rate)/min_sale_price,3),


        # dmarket直接购买出售，buff满足采购单
         "dmarket_buy_min_buff_sale_min": round(max_buy_price*trans_buff_service_change()-float(avg_price)*exchange_rate, 2),
         "dmarket_buy_min_buff_sale_min_rate": round((max_buy_price*trans_buff_service_change()-float(avg_price)*exchange_rate)/min_sale_price,3),

        # steam购买后，buff直接出售
         "steam_buy": round(min_sale_price-steam_buy_price*steam_exchange_rate, 2),
         "steam_buy_rate": round((min_sale_price-steam_buy_price*steam_exchange_rate)/(steam_buy_price*steam_exchange_rate),3),


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
    

# 手续费 
def trans_buff_service_change():
    return 0.975


# 过滤出要查询的饰品的buff数据
def filter_buff_data():
    all_base_info=[]
    with open(data_path+"/analysis/1_cs_buff_uu_c5_base.json", "r", encoding='utf-8') as cs_buff_uu_c5_base:
        for base_info_line in cs_buff_uu_c5_base:
            base_info_json=json.loads(base_info_line)
            all_base_info.append(base_info_json)


    with open("data/0_origin_filter.json", "r", encoding='utf-8') as origin_filter:
        duplicate_value=set()
        with open(data_path+"/analysis/1_cs_buff_uu_c5_base_filter.json", "w", encoding='utf-8') as cs_buff_uu_c5_base_filter:
            for origin_line in origin_filter:
                origin_line_data=str(origin_line.replace("\n",""))

                # 去重
                if origin_line_data not in duplicate_value:
                    duplicate_value.add(origin_line_data)
                    print(origin_line_data)
                    for base_info in all_base_info:
                        if  origin_line_data == base_info['cn_name']:
                                cs_buff_uu_c5_base_filter.write(json.dumps(base_info,ensure_ascii=False)+"\n")



                # with open("dassbuff/data/1_cs_buff_uu_c5_base.json", "r", encoding='utf-8') as cs_buff_uu_c5_base:
                #     for base_info_line in cs_buff_uu_c5_base:
                #         base_info_json=json.loads(base_info_line)
                #         if  origin_line_data == base_info_json['cn_name']:
                #             # print(base_info_line)
                #             cs_buff_uu_c5_base_filter.write(base_info_line)





# skins=get_skin_title()

def find_buff_dmarket_price(exchange_rate):
    print("开始查询数dmarket据")
    with open(data_path+"/analysis/1_cs_buff_uu_c5_base_filter.json", "r", encoding='utf-8') as cs_buff_uu_c5_base_filter:
        # with open("dassbuff/data/2_cs_all_product_filter.txt", "w", encoding='utf-8') as product_filter_file:
        with open(data_path+"/analysis/3_cs_dmarket_price_filter.txt", "w", encoding='utf-8') as price_filter_file:
            num=0
            for base_filter_line in cs_buff_uu_c5_base_filter:
                num += 1
                base_filter_line_date=json.loads(base_filter_line)
                # 只获取cs的饰品数据名称
                if  "appid" in base_filter_line_date.keys() and base_filter_line_date["appid"]== 730 :
                    all_names=base_filter_line_date['cn_name']+':'+base_filter_line_date['en_name']
                    print(str(base_filter_line_date["appid"])+":"+all_names)

                    time.sleep(1)
                    market_price = get_offer_from_market_average(day=searchNum+searchUnit,title=base_filter_line_date['en_name'])
                    # key_info=get_current_market(limit="10",title=base_filter_line_date['en_name'])
                    target_info=get_target_market(title=base_filter_line_date['en_name'],exchange_rate=exchange_rate)
                    print(target_info)
                    correlationd_data=build_target_body_from_offer_avarage(buff_price=base_filter_line_date,market_price=market_price,key_info=target_info,exchange_rate=exchange_rate)
                    price_filter_file.write(json.dumps(correlationd_data,ensure_ascii=False)+"\n")

                    # product_filter_file.write(all_names+"\n")


# 一行一行的读取json数组，并写入到excel中
def export_json_to_excel():
    print("开始导出数据")
    filename=data_path+"/excel/"+"dmakert_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    all_data=[]

        # 定义中文名和字段样式
    chinese_columns = {
        'title':'中文名',
        'drtitle':'英文名',
        'totalSales':'销售数量',
        'date':'日期',
        'dmarket_sale_Price':'平均购买价',
        'dmarket_buy_Price':'平均购买价-提现价',
        'offer_price':'当前出售价',
        'target_price':'当前采购价',
        'target_account':'当前采购数量',
        'dayTotalAmount':'每天销售总价',
        'buff_buy_price':'buff购买价',
        'buff_buy_count':'buff购买数量',
        'buff_sale_price':'buff出售价',
        'buff_sale_count':'buff出售数量',
        'igxe_buy_price':'ig购买价',
        'igxe_buy_count':'ig购买数量',
        'igxe_sale_price':'ig出售价',
        'igxe_sale_count':'ig出售数量',
        'uuyp_buy_price':'uu购买价',
        'uuyp_buy_count':'uu购买数量',
        'uuyp_sale_price':'uu出售价',
        'uuyp_sale_count':'uu出售数量',
        'steam_buy_price':'steam购买价',
        'steam_sale_price':'steam购买数量',
        'steam_buy_count':'steam出售价',
        'steam_sale_count':'steam出售数量',
        'min_buy_price':'最低购买价',
        'min_sale_price':'最低出售价',
        'max_sale_price_num':'最大出售数量',
        'max_sale_price_num_all':'所有出售数量',
        'max_buy_price':'最高购买价',
        'max_sale_price':'最高出售价',
        'buff_buy_max_dmarket_sale_min':'buff购买dr平均价出售',
        'buff_buy_max_dmarket_sale_min_rate':'buff购买dr平均价出售率',
        'buff_buy_max_dmarket_sale_current':'buff购买dr当前价出售',
        'buff_buy_max_dmarket_sale_current_rate':'buff购买dr当前价出售率',
        # 'buff_buy_min_dmarket_sale_min':'buff采购dr出售',
        # 'buff_buy_min_dmarket_sale_min_rate':'buff采购dr出售率',
        'dmarket_buy_min_buff_sale_max':'dr购买buff出售',
        'dmarket_buy_min_buff_sale_max_rate':'dr购买buff出售率',
        'dmarket_target_min_buff_sale_max':'dm采购单buff出售',
        'dmarket_target_min_buff_sale_max_rate':'dm采购单buff出售率',
        'dmarket_buy_min_buff_sale_min':'dr购买buff满足采购单',
        'dmarket_buy_min_buff_sale_min_rate':'dr购买buff满足采购单率',
        'steam_buy':'steam购买buff出售',
        'steam_buy_rate':'steam购买buff出售率',
    }

    # 打开文件准备读取
    with open(data_path+'/analysis/3_cs_dmarket_price_filter.txt', 'r', encoding='utf-8') as file:
       for line in file:
           json_data=json.loads(line.replace("\\b",""))
           for single in json_data:
               all_data.append(single)


    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(all_data)
    # 写入Excel文件
    # 注意：如果你需要写入.xlsx文件，需要指定引擎为openpyxl
    # df.to_excel(filename, index=False, engine='openpyxl')

    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        # 获取工作簿和工作表对象
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # 定义加粗和颜色格式
        bold_format = workbook.add_format({'bold': True})
        red_format = workbook.add_format({'bold': True, 'font_color': 'red'})
        
        # 设置列标题的中文名和样式
        for col_num, value in enumerate(df.columns.values):
            # 设置中文名
            worksheet.write(0, col_num, chinese_columns[value], bold_format)
            
            # # 如果需要，根据某些条件设置列的颜色（例如，分数列）
            # if value == 'score':
            #     # 为第一行之后的数据行设置颜色
            #     for row_num in range(1, len(df) + 1):
            #         worksheet.write(row_num, col_num, None, red_format)

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
        key="7LONCJBBWIZWMX2FXTQM"
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




if __name__ == '__main__':
    # 下载buff数据
    # dir_name='base_archive'
    # buff_zip_file_data=get_buff_data_file_name(dir_name)
    # down_buff_zip_file(dir_name,buff_zip_file_data)

    start_time=int(time.time())
    exchange_rate=find_us_exchange()
    print("当前的美元汇率是："+str(exchange_rate))
    filter_buff_data()
    find_buff_dmarket_price(exchange_rate)
    export_json_to_excel()
    end_time=int(time.time())
    print("运行时间："+str(end_time-start_time))



    # key_info=get_current_market(limit="5",title="Revolution Case")
    # print(key_info)
                        
# for key,value in skins.items():
#     offer_from_market = get_offer_from_market_average(day=searchNum+searchUnit,title=value)
#     build_target_body_from_offer_avarage(title=key,drtitle=value,offers=offer_from_market)


# 过滤


# # 将JSON数组转换为pandas DataFrame
# df=pd.DataFrame (all_list)
# # 将DataFrame导出为Excel文件
# # 需要指定文件名和路径，以及是否包含索引（index=False表示不包含索引）
# filename="offer_avarage_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
# df.to_excel(filename,index=False, engine='openpyxl')


# # 导出筛选后的数据
# filter_df=pd.DataFrame (filter_list)
# filter_filename="offer_avarage_filter_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
# filter_df.to_excel(filter_filename,index=False, engine='openpyxl')

