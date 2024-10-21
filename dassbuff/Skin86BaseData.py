import json
from datetime import datetime

import pandas as pd
import requests
from datetime import datetime
import time
import os
from zipfile import ZipFile

import config



# 获取csgodb的实时成交数据
def get_csgo_db_deal(page):
    try:
        # 设置请求的URL
        url = 'https://api-csob.ok-skins.com/api/v2/goods/vol/list'
        # 设置请求头
        headers = {
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Auth':'fbf272d3dc6f6840f14782454d66f8b6',
            'Connection':'keep-alive',
            'Content-Type':'application/json',
            'Origin':'https://csgoob.com',
            'Referer':'https://csgoob.com/',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'cross-site',
            'Timestamp':'1729065175829',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'Windows',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'sec-ch-ua': 'Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        }
        # 设置请求的数据
        data = {
            "type": 'vol',
            "categories": [],
            "keywords": '',
            "page": page
        }
        # 发送POST请求
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            offers=reponse_json['data']
            # 过滤平均销量大于30的列表
            return offers
        return None
    except Exception as e:
        print(e)
        return None
    

def get_csgo_db_all(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


    page=1
    while True:
        print("获取第"+str(page)+"页数据")
        time.sleep(1.5)
        page_data=get_csgo_db_deal(page)

        if page_data is None :
            print("获取数据为空，退出")
            break

        with open(file_name, 'a+', encoding='utf-8') as skin_file:
            list=page_data['list']
            if len(list)<1:
                print("获取数据完成,返回数据为空")
                break
            for item in list:
                item_json=json.dumps(item, ensure_ascii=False)
                skin_file.write(item_json+'\n')
        page=page+1




# 获取三羊数据
def get_skin_86_market(page=1,page_size=10,price_start=1,price_end=10000,selling_num_start=100,platform='YP'):
    try:
        # 设置请求的URL
        url = 'https://www.skin86.com/api/v1/skin/goods/list'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'cookie': 'Hm_lvt_29d04ae967672202d14e249fcbd647ec=1724293972; HMACCOUNT=7B6DFC0DE180F8A6; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIyNTY3MzA5NDIxMSwiaWF0IjoxNzI0Mjk0MjExLCJuYmYiOjE3MjQyOTQyMTEsInBob25lIjoiMTgzOTAyMzEzMDYiLCJ1aWQiOiIyMjc0NTI0OTU2NTczIiwidXNlcl9pZCI6MjA5OCwidXNlcm5hbWUiOiJDU3JoNURwWGl6In0.q8rbbWIpUrzMy1HJDCxNWvL8msJWx83ZkXxsUz8juE8; Hm_lpvt_29d04ae967672202d14e249fcbd647ec=1724294264',
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIyNTY3MzA5NDIxMSwiaWF0IjoxNzI0Mjk0MjExLCJuYmYiOjE3MjQyOTQyMTEsInBob25lIjoiMTgzOTAyMzEzMDYiLCJ1aWQiOiIyMjc0NTI0OTU2NTczIiwidXNlcl9pZCI6MjA5OCwidXNlcm5hbWUiOiJDU3JoNURwWGl6In0.q8rbbWIpUrzMy1HJDCxNWvL8msJWx83ZkXxsUz8juE8',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'referer': 'https://www.skin86.com/ornaments',
            'language': 'ZH',
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
            "page": page,
            "page_size": page_size,
            "price_start": price_start,
            "price_end": price_end,
            "selling_num_start": selling_num_start,
            # "platform": 'BUFF',
            "platform": platform,
            "order_key": 'sell_max_num',
            "order_type": 2,
        }
        # 发送POST请求
        response = requests.get(url, params=params,headers=headers)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            offers=reponse_json['data']
            # 过滤平均销量大于30的列表
            return offers
        return None
    except Exception as e:
        print(e)
        return None

def get_skin_86_market_all(file_name,limit_page=10,page=1,page_size=10,price_start=1,price_end=10000,selling_num_start=100,platform='YP'):
    if os.path.exists(file_name):
        os.remove(file_name)

    all_list=[]
    with open(config.cs_product_all_name, 'r', encoding='utf-8') as all_name_file:
        for line in all_name_file:
            all_list.append(line.strip())

    page=1
    while True:
        print("获取第"+str(page)+"页数据")
        time.sleep(0.5)
        if limit_page<page  :
            print("获取数据结束了，退出")
            break

        page_data=get_skin_86_market(page,page_size,price_start,price_end,selling_num_start,platform)

        if page_data is None :
            print("获取数据为空，退出")
            break

        with open(file_name, 'a+', encoding='utf-8') as skin_file:
            list=page_data['list']
            if len(list)<1:
                print("获取数据完成,返回数据为空")
                break
            for item in list:
                # 匹配英文名称
                item['en_name']="0"
                for cur_name in all_list:
                    try:
                        cn_name_list=cur_name.split("----")
                        if cn_name_list[0] == item['market_name']:
                            item['en_name']=cn_name_list[1]
                    except Exception as e:  
                        print(e)    
                        continue
                    
                # 过滤掉印花 涂鸦 纪念品 胶囊
                # if '印花' in item['category_group_name'] or '涂鸦' in item['market_name'] or '纪念品' in item['market_name'] or '胶囊' in item['market_name'] or '探员' in item['category_group_name']:
                #     continue

                item_json=json.dumps(item, ensure_ascii=False)
                skin_file.write(item_json+'\n')
        page=page+1
