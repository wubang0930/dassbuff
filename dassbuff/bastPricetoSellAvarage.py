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
def build_target_body_from_offer_avarage(title,drtitle,offers):
    if offers is None:
        return ""
    correlationd_data=[
        {"title":title,"drtitle":drtitle,"totalSales":int(total_sales),"date":datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d'),"avgPrice":round(float(avg_price)*exchange_rate,2),"dayTotalAmount":round(float(total_sales)*float(avg_price)*exchange_rate,2),"totalAmount":round(float(total_sales)*float(avg_price)*exchange_rate,2)}
        for total_sales,date,avg_price in zip(offers["totalSales"],offers["date"],offers["avgPrice"])
    ]

    # all_correlationd_num=0
    # for i in correlationd_data:
    #     all_correlationd_num+=i["totalSales"]

    # avarage_num=all_correlationd_num/int(searchNum)
    # if avarage_num>filter_num:
    #     filter_list.extend(correlationd_data);

    # all_list.extend(correlationd_data);
    return correlationd_data



skins=get_skin_title()


with open("dassbuff/data/base_name_copy.txt", "r", encoding='utf-8') as all_data_file:
    with open("dassbuff/data/base_name_copy_anallysis.txt", "w", encoding='utf-8') as write_file:
        num=0
        for line in all_data_file:
            cn_en=line.strip().split(":")
            if len(cn_en)==2 and cn_en[1] != "":
                time.sleep(1)
                offer_from_market = get_offer_from_market_average(day=searchNum+searchUnit,title=cn_en[1])
                correlationd_data=build_target_body_from_offer_avarage(title=cn_en[0],drtitle=cn_en[1],offers=offer_from_market)
                write_file.write(json.dumps(correlationd_data,ensure_ascii=False)+"\n")

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

