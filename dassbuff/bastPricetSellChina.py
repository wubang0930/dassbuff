import json
from datetime import datetime

import pandas as pd
import re
from datetime import datetime
import time
from zipfile import ZipFile

import config
import Skin86BaseData
import bastPricetSellSkin86
import math


skin_86_product_all_buff=config.skin_86_product_all_buff
skin_86_product_all_yp=config.skin_86_product_all_yp
skin_86_product_all_igxe=config.skin_86_product_all_igxe
skin_86_product_all_steam=config.skin_86_product_all_steam
csgo_db_deal=config.csgo_db_deal
data_local_excel=config.data_local_excel



taobao_price=545


def get_zero_filled_string(number):
    # 将数字转为字符串，并计算长度
    length = len(str(abs(number)))  # 使用 abs() 处理负数
    # 生成对应的零填充字符串
    return '0' * length




def ananlyse_data(exchange_rate):
    all_data_list=[]


    buff_list=[]
    yp_list=[]
    igxe_list=[]
    steam_list=[]
    csgo_db_deal_list=[]
    with open(skin_86_product_all_buff, 'r', encoding='utf-8') as buff:
        for line in buff:
            buff_list.append(json.loads(line))
    with open(skin_86_product_all_yp, 'r', encoding='utf-8') as yp:
        for line in yp:
            yp_list.append(json.loads(line))
    with open(skin_86_product_all_igxe, 'r', encoding='utf-8') as igxe:
        for line in igxe:
            igxe_list.append(json.loads(line))
    with open(skin_86_product_all_steam, 'r', encoding='utf-8') as steam:   
        for line in steam:   
            steam_list.append(json.loads(line))
            
    with open(csgo_db_deal, 'r', encoding='utf-8') as csgo_db:
        for line in csgo_db:
            csgo_db_deal_list.append(json.loads(line))

    all_price_list={}
    min_price_list={}
    max_price_list={}
    min_price_platform_list={}
    max_price_platform_list={}

    all_target_list={}
    min_target_list={}
    max_target_list={}
    min_target_platform_list={}
    max_target_platform_list={}

    keys_to_delete=['rarity_color','is_follow','exterior','rarity','en_name']
    for i in buff_list:
        i['platform_id']='BUFF'        
        all_data_list.append(i)
    for i in yp_list:
        i['platform_id']='YP'
        all_data_list.append(i)
    for i in igxe_list:
        i['platform_id']='IGXE'
        all_data_list.append(i)
    for i in steam_list:
        i['platform_id']='STEAM'
        i['sell_min_price']=round(i['sell_min_price']*taobao_price/100/exchange_rate,1)
        all_data_list.append(i)

    for key in keys_to_delete:
        for i in all_data_list:
            i.pop(key,None)


    # 获取最小值 和最大值 和所有的价格列表



    count_one_data_list=[]
    for i in buff_list:
        i['sell_min_price']=math.ceil(i['sell_min_price'])

        # 磨损类型
        i['min_type']=''
        if '(' in i['market_name']  and ')' in i['market_name'] :
            i['min_type']=i['market_name'] [i['market_name'].index('(')+1:i['market_name'].index(')')]

        #当日成交
        i['today_count']=0
        i['today_price']=0
        for j in csgo_db_deal_list:
            if i['market_name']==j['goodsName'] :
                i['today_count']=j['count']
                if j['count']!=0:
                    i['today_price']=round(j['price']/j['count']/100,1)
                break
        
        # buff的价格拼接
        all_price_list[i['market_name']]=[]
        all_price_list[i['market_name']].append(i['sell_min_price'])
        min_price_list[i['market_name']]=i['sell_min_price']
        max_price_list[i['market_name']]=i['sell_min_price']
        min_price_platform_list[i['market_name']]=i['platform_id']
        max_price_platform_list[i['market_name']]=i['platform_id']


        # buff的采购价格拼接
        all_target_list[i['market_name']]=[]
        all_target_list[i['market_name']].append(i['buy_max_price'])
        min_target_list[i['market_name']]=i['buy_max_price']
        max_target_list[i['market_name']]=i['buy_max_price']
        min_target_platform_list[i['market_name']]=i['platform_id']
        max_target_platform_list[i['market_name']]=i['platform_id']


        yp_name_flag=False
        for j in yp_list:
            if i['market_name']==j['market_name'] :
                yp_name_flag=True
                all_price_list[i['market_name']].append(j['sell_min_price'])
                all_target_list[i['market_name']].append(j['buy_max_price'])

                if j['sell_min_price']<min_price_list[i['market_name']]:
                    min_price_list[j['market_name']]=j['sell_min_price']
                    min_price_platform_list[i['market_name']]=j['platform_id']
                
                if j['sell_min_price']>max_price_list[i['market_name']]:
                    max_price_list[j['market_name']]=j['sell_min_price']
                    max_price_platform_list[i['market_name']]=j['platform_id']

                if j['buy_max_price']<min_target_list[i['market_name']]:
                    min_target_list[j['market_name']]=j['buy_max_price']
                    min_target_platform_list[i['market_name']]=j['platform_id']
                
                if j['buy_max_price']>max_target_list[i['market_name']]:
                    max_target_list[j['market_name']]=j['buy_max_price']
                    min_target_platform_list[i['market_name']]=j['platform_id']

                
                break

        if yp_name_flag==False:
            all_price_list[i['market_name']].append(get_zero_filled_string(i['sell_min_price']))
            all_target_list[i['market_name']].append(get_zero_filled_string(i['buy_max_price']))

        igxe_name_flag=False
        for j in igxe_list:
            if i['market_name']==j['market_name'] :
                igxe_name_flag=True
                all_price_list[i['market_name']].append(j['sell_min_price'])
                all_target_list[i['market_name']].append(j['buy_max_price'])

                if j['sell_min_price']<min_price_list[i['market_name']]:
                    min_price_list[j['market_name']]=j['sell_min_price']
                    min_price_platform_list[i['market_name']]=j['platform_id']
                
                if j['sell_min_price']>max_price_list[i['market_name']]:
                    max_price_list[j['market_name']]=j['sell_min_price']
                    max_price_platform_list[i['market_name']]=j['platform_id']

                if j['buy_max_price']<min_target_list[i['market_name']]:
                    min_target_list[j['market_name']]=j['buy_max_price']
                    min_target_platform_list[i['market_name']]=j['platform_id']

                if j['buy_max_price']>max_target_list[i['market_name']]:
                    max_target_list[j['market_name']]=j['buy_max_price']
                    min_target_platform_list[i['market_name']]=j['platform_id']
                
                break
        if igxe_name_flag==False:
            all_price_list[i['market_name']].append(get_zero_filled_string(i['sell_min_price']))
            all_target_list[i['market_name']].append(get_zero_filled_string(i['buy_max_price']))


        steam_name_flag=False
        for j in steam_list:
            if i['market_name']==j['market_name'] :
                steam_name_flag=True
                all_price_list[i['market_name']].append(j['sell_min_price'])
                all_target_list[i['market_name']].append(j['buy_max_price'])

                # if j['sell_min_price']<min_price_list[i['market_name']]:
                #     min_price_list[j['market_name']]=j['sell_min_price']
                
                # if j['sell_min_price']>max_price_list[i['market_name']]:
                #     max_price_list[j['market_name']]=j['sell_min_price']
                
                break
        if steam_name_flag==False:
            all_price_list[i['market_name']].append(get_zero_filled_string(i['sell_min_price']))
            all_target_list[i['market_name']].append(get_zero_filled_string(i['buy_max_price']))




    for i in buff_list:

        i['all_max_price']=0
        i['all_max_price_platform']=""
        if i['market_name'] in max_price_list:
            i['all_max_price']=max_price_list[i['market_name']]
            i['all_max_price_platform']=max_price_platform_list[i['market_name']]

        i['all_min_price']=0
        i['all_min_price_platform']=""
        if i['market_name'] in min_price_list:
            i['all_min_price']=min_price_list[i['market_name']]
            i['all_min_price_platform']=min_price_platform_list[i['market_name']]

        i['all_price_list']=""
        if i['market_name'] in all_price_list:
            for x in all_price_list[i['market_name']]:
                i['all_price_list']=i['all_price_list']+"——"+str(x)
            i['all_price_list']=i['all_price_list'][2:]

        i['devilide_price']=i['all_max_price']-i['all_min_price']
        if i['all_max_price']>0:
            i['devilide_price_rate']=round(i['devilide_price']/i['all_max_price'],3)*100

        
        i['all_max_target']=0
        i['all_max_target_platform']=""
        if i['market_name'] in max_target_list:
            i['all_max_target']=max_target_list[i['market_name']]
            i['all_max_target_platform']=max_target_platform_list[i['market_name']]

        i['all_min_target']=0
        i['all_min_target_platform']=""
        if i['market_name'] in min_target_list:
            i['all_min_target']=min_target_list[i['market_name']]
            i['all_min_target_platform']=min_target_platform_list[i['market_name']]

        i['all_target_list']=""
        if i['market_name'] in all_target_list:
            for x in all_target_list[i['market_name']]:
                i['all_target_list']=i['all_target_list']+"——"+str(x)
            
            i['all_target_list']=i['all_target_list'][2:]

        i['price_target_devilide']=i['all_max_price']-i['all_min_target']
        i['price_target_devilide_rate']=round(i['price_target_devilide']/i['all_max_price'],3)*100
        
        


    # for i in all_data_list:
    #     # 磨损类型
    #     i['min_type']=''
    #     if '(' in i['market_name']  and ')' in i['market_name'] :
    #         i['min_type']=i['market_name'] [i['market_name'].index('(')+1:i['market_name'].index(')')]

    #     #当日成交
    #     i['today_count']=0
    #     i['today_price']=0
    #     for j in csgo_db_deal_list:
    #         if i['market_name']==j['goodsName'] :
    #             i['today_count']=j['count']
    #             if j['count']!=0:
    #                 i['today_price']=round(j['price']/j['count']/100,1)
    #             break
        
    #     i['all_min_price']=0
    #     if min_price_list[i['market_name']]==i['sell_min_price']:
    #         i['all_min_price']=min_price_list[i['market_name']]



    # buff_list.sort(key=lambda x:(x['goods_id'],x['platform_id']),reverse=True)
    buff_list.sort(key=lambda x:(x['goods_id']),reverse=True)
    export_json_to_excel(buff_list)

    # 汇总导出



    



def export_json_to_excel(all_data):
    print("开始导出数据")
    filename=config.data_local_excel+"/china_data_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"

        # 定义中文名和字段样式
    chinese_columns = {
    "goods_id": '商品id',
    "category_group_name": "类型",
    "min_type": "磨损类型",
    "market_name": "名称",
    "all_price_list": '所有售价(buff\yp\igxe\steam)',
    "all_min_price": '最低售卖价',
    "all_max_price": '最高售卖价',
    "devilide_price": '相差价',
    "devilide_price_rate": '相差价率',
    "all_min_price_platform": '最低售卖平台',
    "all_max_price_platform": "最高售卖平台",
    "sell_max_num": '出售数量',
    
    "today_count": '今日成交数量',
    "today_price": '今日成交均价',
    "price_target_devilide": '最高差价',
    "price_target_devilide_rate": '最高差价率',
    "all_min_target": '最低采购价',
    "all_max_target": '最高采购价',
    "all_target_list": '所有采购价',
    "all_min_target_platform": '最低采购价平台',
    "all_max_target_platform": '最高采购价平台',
    "buy_max_num": '采购数量',
    "price_alter_percentage_7d": '7天变化率',
    "price_alter_value_7d": '7天变化价格',
    "market_hash_name": "英文名称",
    "icon_url": "产品图片",
    "redirect_url": "购买链接",
    
    
    }
    column_order = ['category_group_name','min_type', 'market_name','all_price_list','all_min_price','all_max_price','devilide_price','devilide_price_rate','sell_max_num','all_min_price_platform','all_max_price_platform','today_count','today_price','price_target_devilide','price_target_devilide_rate','buy_max_num','all_min_target','all_max_target','all_target_list','all_min_target_platform','all_min_target_platform','price_alter_percentage_7d','price_alter_value_7d','market_hash_name','icon_url','redirect_url']

   


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
            column_width = 7  # 你可以根据需要调整这个值
            if 'market_name' in value or 'all_price_list' in value or 'all_target_list' in value :
                worksheet.set_column(col_num, col_num, 30)
            else:
                worksheet.set_column(col_num, col_num, column_width)
            worksheet.write(0, col_num, chinese_columns[value], yellow_format)


    # 完成后关闭文件
    # workbook.close()



if __name__ == '__main__':
# def start():    
    start_time=int(time.time())
    exchange_rate=bastPricetSellSkin86.find_us_exchange()
    print("当前的美元汇率是："+str(exchange_rate))

    
    # # 初始化数据
    # Skin86BaseData.get_skin_86_market_all(file_name= skin_86_product_all_buff,limit_page=100,page=0,page_size=100,price_start=500,price_end=1500,selling_num_start=10,platform='BUFF')
    # Skin86BaseData.get_skin_86_market_all(file_name= skin_86_product_all_yp,limit_page=100,page=0,page_size=100,price_start=500,price_end=1500,selling_num_start=10,platform='YP')
    # Skin86BaseData.get_skin_86_market_all(file_name= skin_86_product_all_igxe,limit_page=100,page=0,page_size=100,price_start=500,price_end=1500,selling_num_start=10,platform='IGXE')
    # Skin86BaseData.get_skin_86_market_all(file_name= skin_86_product_all_steam,limit_page=100,page=0,page_size=100,price_start=500,price_end=1500,selling_num_start=10,platform='STEAM')
   
   
    # 查询C5的当日成交 每天晚上查询一次就行
    # Skin86BaseData.get_csgo_db_all(file_name=csgo_db_deal)
    
    ananlyse_data(exchange_rate)
    #所有的数据，都遍历当道一个excel中

    end_time=int(time.time())
    print("运行时间："+str(end_time-start_time))




