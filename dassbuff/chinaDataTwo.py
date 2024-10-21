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

recharge_rate=1.027   #充值手续费
steam_exchange_rate=0.79   #实际汇率*实际提现到手

all_list=[]


filter_num=30   #过滤平均销量大于30的数量
filter_list=[]   #过滤平均销量大于30的列表

priority_archive=config.priority_archive
priority_archive_json=config.data_local_analysis+"/"+config.priority_archive

csgo_db_deal=config.csgo_db_deal
skin_86_product_all_buff=config.skin_86_product_all_buff




# 过滤出要查询的饰品的buff数据
def filter_buff_data():
    csgo_db_deal_list=[]
    with open(csgo_db_deal, "r", encoding='utf-8') as db_deal:
        for line in db_deal:
            csgo_db_deal_list.append(json.loads(line))

    buff_list=[]
    with open(skin_86_product_all_buff, "r", encoding='utf-8') as buff_file:
        for line in buff_file:
            buff_list.append(json.loads(line))




    all_base_info=[]
    with open(priority_archive_json, "r", encoding='utf-8') as cs_buff_uu_c5_base:
        for base_info_line in cs_buff_uu_c5_base:
            filter_data={}

            base_info_json=json.loads(base_info_line)
            if base_info_json['buff_buy']['price'] is None or base_info_json['buff_buy']['price']<100:
                continue

            filter_data['cn_name']=base_info_json['cn_name']
            filter_data['en_name']=base_info_json['en_name']
            filter_data['steam_volume']=base_info_json['steam_volume']['volume']

            filter_data['min_buy_price'] = 9999999
            filter_data['max_buy_price'] = 0
            filter_data['buy_price_list'] = []

            filter_data['min_buy_price_platform']=""
            filter_data['max_buy_price_platform']=""
            
            

            filter_data['buy_price_list'].append(base_info_json['buff_buy']['price'] is not None and base_info_json['buff_buy']['price'] or 0)
            filter_data['buy_price_list'].append(base_info_json['c5_buy']['price'] is not None and base_info_json['c5_buy']['price'] or 0)
            filter_data['buy_price_list'].append(base_info_json['igxe_buy']['price'] is not None and base_info_json['igxe_buy']['price'] or 0)
            filter_data['buy_price_list'].append(base_info_json['uuyp_buy']['price'] is not None and base_info_json['uuyp_buy']['price'] or 0)
            filter_data['buy_price_list'].append(base_info_json['steam_order']['buy_price'] is not None and base_info_json['steam_order']['buy_price'] or 0)
            
            if base_info_json['buff_buy']['price'] is not None and base_info_json['buff_buy']['price']<filter_data['min_buy_price']:
                filter_data['min_buy_price'] = base_info_json['buff_buy']['price']
                filter_data['min_buy_price_platform']="buff"
            if base_info_json['c5_buy']['price'] is not None and base_info_json['c5_buy']['price']<filter_data['min_buy_price']:
                filter_data['min_buy_price'] = base_info_json['c5_buy']['price']
                filter_data['min_buy_price_platform']="c5"
            if base_info_json['igxe_buy']['price'] is not None and base_info_json['igxe_buy']['price']<filter_data['min_buy_price']:
                filter_data['min_buy_price'] = base_info_json['igxe_buy']['price']
                filter_data['min_buy_price_platform']="igxe"
            if base_info_json['uuyp_buy']['price'] is not None and base_info_json['uuyp_buy']['price']<filter_data['min_buy_price']:
                filter_data['min_buy_price'] = base_info_json['uuyp_buy']['price']
                filter_data['min_buy_price_platform']="uupy"
           

            

            
            filter_data['max_buy_price_platform']=""
            if base_info_json['buff_buy']['price'] is not None and base_info_json['buff_buy']['price']>filter_data['max_buy_price']:
                filter_data['max_buy_price'] = base_info_json['buff_buy']['price']
                filter_data['max_buy_price_platform']="buff"
            if base_info_json['c5_buy']['price'] is not None and base_info_json['c5_buy']['price']>filter_data['max_buy_price']:
                filter_data['max_buy_price'] = base_info_json['c5_buy']['price']
                filter_data['max_buy_price_platform']="c5"
            if base_info_json['igxe_buy']['price'] is not None and base_info_json['igxe_buy']['price']>filter_data['max_buy_price']:
                filter_data['max_buy_price'] = base_info_json['igxe_buy']['price']
                filter_data['max_buy_price_platform']="igxe"
            if base_info_json['uuyp_buy']['price'] is not None and base_info_json['uuyp_buy']['price']>filter_data['max_buy_price']:
                filter_data['max_buy_price'] = base_info_json['uuyp_buy']['price']
                filter_data['max_buy_price_platform']="uupy"


            filter_data['min_sell_price'] = 9999999
            filter_data['max_sell_price'] = 0
            filter_data['sell_price_list'] = []
            filter_data['min_sell_price_platform']=""
            filter_data['max_sell_price_platform']=""

                   
            filter_data['sell_price_list'].append(base_info_json['buff_sell']['price'] is not None and base_info_json['buff_sell']['price'] or 0)
            filter_data['sell_price_list'].append(base_info_json['c5_sell']['price'] is not None and base_info_json['c5_sell']['price'] or 0)            
            filter_data['sell_price_list'].append(base_info_json['igxe_sell']['price'] is not None and base_info_json['igxe_sell']['price'] or 0)
            filter_data['sell_price_list'].append(base_info_json['uuyp_sell']['price'] is not None and base_info_json['uuyp_sell']['price'] or 0)
            filter_data['sell_price_list'].append(base_info_json['steam_order']['sell_price'] is not None and base_info_json['steam_order']['sell_price'] or 0)
            
            
            
            if base_info_json['buff_sell']['price'] is not None and base_info_json['buff_sell']['price']<filter_data['min_sell_price']:
                filter_data['min_sell_price'] = base_info_json['buff_sell']['price']
                filter_data['min_sell_price_platform']="buff"
            if base_info_json['c5_sell']['price'] is not None and base_info_json['c5_sell']['price']<filter_data['min_sell_price']:
                filter_data['min_sell_price'] = base_info_json['c5_sell']['price']
                filter_data['min_sell_price_platform']="c5"
            if base_info_json['igxe_sell']['price'] is not None and base_info_json['igxe_sell']['price']<filter_data['min_sell_price']:
                filter_data['min_sell_price'] = base_info_json['igxe_sell']['price']
                filter_data['min_sell_price_platform']="igxe"
            if base_info_json['uuyp_sell']['price'] is not None and base_info_json['uuyp_sell']['price']<filter_data['min_sell_price']:
                filter_data['min_sell_price'] = base_info_json['uuyp_sell']['price']
                filter_data['min_sell_price_platform']="uupy"


            
     
            if base_info_json['buff_sell']['price'] is not None and base_info_json['buff_sell']['price']>filter_data['max_sell_price']:
                filter_data['max_sell_price'] = base_info_json['buff_sell']['price']
                filter_data['max_sell_price_platform']="buff"
            if base_info_json['c5_sell']['price'] is not None and base_info_json['c5_sell']['price']>filter_data['max_sell_price']:
                filter_data['max_sell_price'] = base_info_json['c5_sell']['price']
                filter_data['max_sell_price_platform']="c5"
            if base_info_json['igxe_sell']['price'] is not None and base_info_json['igxe_sell']['price']>filter_data['max_sell_price']:
                filter_data['max_sell_price'] = base_info_json['igxe_sell']['price']
                filter_data['max_sell_price_platform']="igxe"
            if base_info_json['uuyp_sell']['price'] is not None and base_info_json['uuyp_sell']['price']>filter_data['max_sell_price']:
                filter_data['max_sell_price'] = base_info_json['uuyp_sell']['price']
                filter_data['max_sell_price_platform']="uupy"

            for j in buff_list:
                if base_info_json['cn_name']==j['market_name'] :
                    filter_data['7d_rate']=j['price_alter_percentage_7d']
                    filter_data['7d_price']=j['price_alter_value_7d']
                    break

            for j in csgo_db_deal_list:
                if base_info_json['cn_name']==j['goodsName'] :
                    filter_data['today_count']=j['count']
                    if j['count']!=0:
                        filter_data['today_price']=round(j['price']/j['count']/100,1)
                    break

            filter_data['all_buy_price_counts'] = []
            filter_data['all_buy_price_counts'].append(base_info_json['buff_buy']['count'] is not None and base_info_json['buff_buy']['count'] or 0)
            filter_data['all_buy_price_counts'].append(base_info_json['c5_buy']['count'] is not None and base_info_json['c5_buy']['count'] or 0)
            filter_data['all_buy_price_counts'].append(base_info_json['igxe_buy']['count'] is not None and base_info_json['igxe_buy']['count'] or 0)
            filter_data['all_buy_price_counts'].append(base_info_json['uuyp_buy']['count'] is not None and base_info_json['uuyp_buy']['count'] or 0)
            filter_data['all_buy_price_counts'].append(base_info_json['steam_order']['buy_order_count'] is not None and base_info_json['steam_order']['buy_order_count'] or 0)
            
            filter_data['all_sell_price_counts'] = []
            filter_data['all_sell_price_counts'].append(base_info_json['buff_sell']['count'] is not None and base_info_json['buff_sell']['count'] or 0)
            filter_data['all_sell_price_counts'].append(base_info_json['c5_sell']['count'] is not None and base_info_json['c5_sell']['count'] or 0)
            filter_data['all_sell_price_counts'].append(base_info_json['igxe_sell']['count'] is not None and base_info_json['igxe_sell']['count'] or 0)
            filter_data['all_sell_price_counts'].append(base_info_json['uuyp_sell']['count'] is not None and base_info_json['uuyp_sell']['count'] or 0)
            filter_data['all_sell_price_counts'].append(base_info_json['steam_order']['sell_order_count'] is not None and base_info_json['steam_order']['sell_order_count'] or 0)
            
            
            all_base_info.append(filter_data)
    
    export_json_to_excel(all_base_info)



def export_json_to_excel(all_data):
    print("开始导出数据")
    filename=config.data_local_excel+"/china_data_two_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"

    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(all_data)
    df.to_excel(filename, index=False)
    print("导出数据完成")
    
    
 




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
        temp_file_path = config.data_local_analysis+"/temp.zip"

        
        # 解压缩到的目标文件夹
        extract_dir = config.data_local_analysis
        extract_file = priority_archive
        file_path = os.path.join(extract_dir, extract_file)

        zip_json_path = os.path.join(extract_dir, file_name.replace(".zip", ".json"))
        

        # 发送GET请求并下载文件
        response = requests.get(url, params=params, stream=True)
        if response.status_code == 200:
            # 以二进制写模式打开文件，并写入内容
            with open(temp_file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
           
            # 解压文件
            with ZipFile(temp_file_path, 'r') as zip_ref:
                # 解压文件到指定文件夹，并覆盖已有文件
                zip_ref.extractall(extract_dir)
                shutil.move(zip_json_path, file_path)
        else:
            print(f"Failed to download file, status code: {response.status_code}")

        print("Download and extraction complete.")
    except Exception as e:
        print(e)




if __name__ == '__main__':

    # # 下载buff数据
    # dir_name='priority_archive'
    # buff_zip_file_data=get_buff_data_file_name(dir_name)
    # down_buff_zip_file(dir_name,buff_zip_file_data)

    filter_buff_data()