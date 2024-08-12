import json
from datetime import datetime

from nacl.bindings import crypto_sign
import pandas as pd
import requests
from datetime import datetime
import time

import config

# change url to prod
rootApiUrl = "https://api.dmarket.com"
exchange_rate=7.13*0.985   #实际汇率*实际提现到手
searchNum="7"  #查询天数
searchUnit="D"  #查询单位

all_list=[]

filter_num=30   #过滤平均销量大于30的数量
filter_list=[]   #过滤平均销量大于30的列表

def get_skin_title():  
    # skins={"千瓦武器箱":"Kilowatt Case","梦魇武器箱":"Dreams%20%26%20Nightmares%20Case","英勇大行动":"Operation Bravo Case"}
    skins={"千瓦武器箱":"Kilowatt Case","变革武器箱":"Revolution Case","反冲武器箱":"Recoil Case","梦魇武器箱":"Dreams & Nightmares Case","“激流大行动”武器箱":"Operation Riptide Case","蛇咬武器箱":"Snakebite Case","“狂牙大行动”武器箱":"Operation Broken Fang Case","裂空武器箱":"Fracture Case","棱彩2号武器箱":"Prisma 2 Case","裂网大行动武器箱":"Shattered Web Case","反恐精英20周年武器箱":"CS20 Case","棱彩武器箱":"Prisma Case","命悬一线武器箱":"Clutch Case","地平线武器箱":"Horizon Case","“头号特训”武器箱":"Danger Zone Case","光谱2号武器箱":"Spectrum 2 Case","九头蛇大行动武器箱":"Operation Hydra Case","光谱武器箱":"Spectrum Case","手套武器箱":"Glove Case","伽马2号武器箱":"Gamma 2 Case","伽马武器箱":"Gamma Case","CS:GO武器箱":"CS:GO Weapon Case","CS:GO2号武器箱":"CS:GO Weapon Case 2","CS:GO3号武器箱":"CS:GO Weapon Case 3","幻彩武器箱":"Chroma Case","幻彩2号武器箱":"Chroma 2 Case","幻彩3号武器箱":"Chroma 3 Case","电竞2013武器箱":"eSports 2013 Case","电竞2013冬季武器箱":"eSports 2013 Winter Case","电竞2014夏季武器箱":"eSports 2014 Summer Case","弯曲猎手武器箱":"Falchion Case","猎杀者武器箱":"Huntsman Weapon Case","英勇大行动武器箱":"Operation Bravo Case","突围大行动":"Operation Breakout Weapon Case","凤凰大行动武器箱":"Operation Phoenix Weapon Case","先锋大行动武器箱":"Operation Vanguard Weapon Case","野火大行动武器箱":"Operation Wildfire Weapon Case","左轮武器箱武器箱":"Revolver Case","暗影武器箱":"Shadow Case","冬季攻势武器箱":"Winter Offensive Weapon Case"}
    return skins



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
def build_target_body_from_offer_avarage(buff_price,market_price):
    if market_price is None:
        return ""
    buff_buy_price= buff_price['buff_buy']['price']
    buff_sale_price= buff_price['buff_sell']['price']
    c5_buy_price= buff_price['c5_buy']['price']
    c5_sale_price= buff_price['c5_sell']['price']
    igxe_buy_price= buff_price['igxe_buy']['price']
    igxe_sale_price= buff_price['igxe_sell']['price']
    uuyp_buy_price= buff_price['uuyp_buy']['price']
    uuyp_sale_price= buff_price['uuyp_sell']['price']

    min_buy_price=min(buff_buy_price,c5_buy_price,igxe_buy_price,igxe_buy_price)
    min_sale_price=min(buff_sale_price,c5_sale_price,igxe_sale_price,uuyp_sale_price)


    correlationd_data=[
        {"title":buff_price['cn_name'],
         "drtitle":buff_price['en_name'],
         "totalSales":int(total_sales),
         "date":datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d'),
         "avgPrice":round(float(avg_price)*exchange_rate,2),
         "dayTotalAmount":round(float(total_sales)*float(avg_price)*exchange_rate,2),
         "buff_buy_price":buff_buy_price,
         "buff_sale_price":buff_sale_price,
         "c5_buy_price":c5_buy_price,
         "c5_sale_price":c5_sale_price,
         "igxe_buy_price":igxe_buy_price,
         "igxe_sale_price":igxe_sale_price,
         "uuyp_buy_price":uuyp_buy_price,
         "uuyp_sale_price":uuyp_sale_price,
         "min_buy_price":min_buy_price,
         "min_sale_price":min_sale_price,
         "price_duct": round(float(avg_price)*exchange_rate- min_buy_price, 2)  
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


# 过滤出要查询的饰品的buff数据

def filter_buff_data():
    all_base_info=[]
    with open("dassbuff/data/1_cs_buff_uu_c5_base.json", "r", encoding='utf-8') as cs_buff_uu_c5_base:
        for base_info_line in cs_buff_uu_c5_base:
            base_info_json=json.loads(base_info_line)
            all_base_info.append(base_info_json)


    with open("dassbuff/data/0_origin_filter.json", "r", encoding='utf-8') as origin_filter:
        duplicate_value=set()
        with open("dassbuff/data/1_cs_buff_uu_c5_base_filter.json", "w", encoding='utf-8') as cs_buff_uu_c5_base_filter:
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

def find_buff_dmarket_price():
    with open("dassbuff/data/1_cs_buff_uu_c5_base_filter.json", "r", encoding='utf-8') as cs_buff_uu_c5_base_filter:
        # with open("dassbuff/data/2_cs_all_product_filter.txt", "w", encoding='utf-8') as product_filter_file:
        with open("dassbuff/data/3_cs_dmarket_price_filter.txt", "w", encoding='utf-8') as price_filter_file:
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
                    correlationd_data=build_target_body_from_offer_avarage(buff_price=base_filter_line_date,market_price=market_price)
                    price_filter_file.write(json.dumps(correlationd_data,ensure_ascii=False)+"\n")

                    # product_filter_file.write(all_names+"\n")


# 一行一行的读取json数组，并写入到excel中
def export_json_to_excel():
    print("开始导出数据")
    filename="dmakert_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    all_data=[]
    # 打开文件准备读取
    with open('dassbuff/data/3_cs_dmarket_price_filter.txt', 'r', encoding='utf-8') as file:
       for line in file:
           json_data=json.loads(line.replace("\\b",""))
           for single in json_data:
               all_data.append(single)


    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(all_data)
    # 写入Excel文件
    # 注意：如果你需要写入.xlsx文件，需要指定引擎为openpyxl
    df.to_excel(filename, index=False, engine='openpyxl')




if __name__ == '__main__':
    filter_buff_data()
    find_buff_dmarket_price()
    export_json_to_excel()
                        
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

