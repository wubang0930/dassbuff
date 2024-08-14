import json
from datetime import datetime

import pandas as pd
import requests
from datetime import datetime
import time

import config

# 查询dmarket里面的特殊磨损售卖，有合适价格的，就购买到buff出售



# change url to prod
rootApiUrl = "https://api.dmarket.com"
exchange_rate=7.18   #实际汇率*实际提现到手
all_data_list=[]

def get_current_market(extraValue,limit,title,cursor=""):
    key_info={}
    market_response = requests.get(rootApiUrl + "/exchange/v1/market/items?side=market&orderBy=best_discount&orderDir=desc&title="+title+"&priceFrom=0&priceTo=0&treeFilters=&gameId=a8db&myFavorites=false&types=dmarket&cursor="+cursor+"&limit="+str(limit)+"&currency=USD&platform=browser&isLoggedIn=false")
    reponse_json = json.loads(market_response.text)


        # 只获取cs的饰品数据名称
    objects=reponse_json['objects']
  
    
    for obj in objects:
        if obj['extra']['floatValue'] < extraValue:
            price={}
            price['price']= round(float(obj['price']['USD'])/100*7.18,2)
            price['extra_value']= round(float(obj['extra']['floatValue']),4)
            all_data_list.append(price)
    
    print(cursor)
    print(all_data_list)
    cursor=reponse_json['cursor']

    if len(objects) >= limit:
        time.sleep(1)
        get_current_market(extraValue,limit,title,cursor)



def export_file(title):
    filename="dassbuff/data/excel"+title+"_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
        # 按age字段降序排序字典列表
    sorted_list = sorted(all_data_list, key=lambda x: x['price'], reverse=True)
    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(sorted_list)
    # 写入Excel文件
    # 注意：如果你需要写入.xlsx文件，需要指定引擎为openpyxl
    df.to_excel(filename, index=False, engine='openpyxl')


if __name__ == '__main__':
    # 输入参数
    title="AK-47 | Head Shot (Field-Tested)"
    get_current_market(extraValue=0.18,limit=100,title=title)
    export_file(title="AK-47")