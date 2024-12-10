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
import mysql.connector
from mysql.connector import Error
import threading
import schedule
import soccersave

log_num=0

skin_86_product_all_buff_mysql=config.skin_86_product_all_buff_mysql
skin_86_product_all_yp_mysql=config.skin_86_product_all_yp_mysql
skin_86_product_all_igxe_mysql=config.skin_86_product_all_igxe_mysql
skin_86_product_all_steam_mysql=config.skin_86_product_all_steam_mysql
csgo_db_deal_mysql=config.csgo_db_deal_mysql

# 数据库连接参数
host = '127.0.0.1'
database = 'csgo'
user = 'root'
password = 'bangye'

taobao_price=545





def save_data_mysql():
    log_num=0
    print(getNowTime()+"开始查询数据")
    Skin86BaseData.get_skin_86_market_all(file_name= skin_86_product_all_buff_mysql,limit_page=200,page=0,page_size=100,price_start=40,price_end=10000,selling_num_start=2,platform='BUFF')
    Skin86BaseData.get_skin_86_market_all(file_name= skin_86_product_all_yp_mysql,limit_page=200,page=0,page_size=100,price_start=40,price_end=10000,selling_num_start=2,platform='YP')
    Skin86BaseData.get_skin_86_market_all(file_name= skin_86_product_all_igxe_mysql,limit_page=200,page=0,page_size=100,price_start=40,price_end=10000,selling_num_start=2,platform='IGXE')
    Skin86BaseData.get_skin_86_market_all(file_name= skin_86_product_all_steam_mysql,limit_page=200,page=0,page_size=100,price_start=40,price_end=10000,selling_num_start=2,platform='STEAM')
    Skin86BaseData.get_csgo_db_all(file_name=csgo_db_deal_mysql)
    print(getNowTime()+"查询数据成功")


    all_data_list=[]

    with open(skin_86_product_all_buff_mysql, 'r', encoding='utf-8') as buff:
        for line in buff:
            line_json=json.loads(line)
            line_json['platform_id']='BUFF' 
            all_data_list.append(line_json)
    with open(skin_86_product_all_yp_mysql, 'r', encoding='utf-8') as yp:
        for line in yp:
            line_json=json.loads(line)
            line_json['platform_id']='YP' 
            all_data_list.append(line_json)
    with open(skin_86_product_all_igxe_mysql, 'r', encoding='utf-8') as igxe:
        for line in igxe:
            line_json=json.loads(line)
            line_json['platform_id']='IGXE' 
            all_data_list.append(line_json)
    with open(skin_86_product_all_steam_mysql, 'r', encoding='utf-8') as steam:   
        for line in steam:
            line_json=json.loads(line)
            line_json['platform_id']='STEAM'    
            all_data_list.append(line_json)

    
    sale_data_list=[]
    with open(csgo_db_deal_mysql, 'r', encoding='utf-8') as csgo:
        for line in csgo:
            sale_data_list.append(json.loads(line))
            
    for all_data in all_data_list:
        all_data['today_sale_count']=0
        all_data['today_sale_price']=0
        
        for sale_data in sale_data_list:
            if all_data['market_name']==sale_data['goodsName']:
                all_data['today_sale_count']=sale_data['count']
                
                if sale_data['count'] != 0 and sale_data['count'] is not None:
                    all_data['today_sale_price']=round(float(sale_data['price'])/sale_data['count']/100,2)
                break
    

    # 先删除今天的数据 在插入今天的数据
    version_date=str(datetime.now().strftime('%Y-%m-%d'))
    print("version_date："+version_date)
    delete_today_data(version_date)


    # 插入数据的 SQL 查询
    # 调用插入数据的方法
    insert_today_buff_data( all_data_list,version_date)
    insert_today_sale_data( sale_data_list,version_date)

def delete_today_data(version_date):
    print(getNowTime()+"开始删除数据")
    try:
        # 连接到 MySQL 数据库
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        sql_cs_db_deal = "delete from csgo_db_deal where version_date = %s"
        sql_goods = "delete from goods where version_date = %s"
        
        values = [version_date]

        if connection.is_connected():
            cursor = connection.cursor()
            # 执行插入查询
            cursor.execute(sql_cs_db_deal, values)
            cursor.execute(sql_goods, values)
            connection.commit()  # 提交事务
            print(getNowTime()+"数据删除成功")
    
    except Error as e:
        print(f"数据库连接错误: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")


def getNowTime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def insert_today_buff_data(data_tuple_list,version_date):
    insert_query = "INSERT INTO `csgo`.`goods`(`goods_id`, `platform_id`, `market_name`, `sell_min_price`, `sell_max_num`, `sell_valuation`, `buy_max_price`, `buy_max_num`, `price_alter_percentage_7d`, `price_alter_value_7d`, `category_group_name`, `rarity_color`, `icon_url`, `is_follow`, `redirect_url`, `exterior`, `rarity`, `market_hash_name`, `en_name`, `today_sale_count`, `today_sale_price`, `create_date`,`version_date`) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s,%s)"

    print(getNowTime()+"开始插入goods数据")
    try:
        # 连接到 MySQL 数据库
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # 执行插入查询
            for data in data_tuple_list:
                data['create_date']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                values = (
                    data['goods_id'],
                    data['platform_id'],
                    data['market_name'],
                    data['sell_min_price'],
                    data['sell_max_num'],
                    data['sell_valuation'],
                    data['buy_max_price'],
                    data['buy_max_num'],
                    data['price_alter_percentage_7d'],
                    data['price_alter_value_7d'],
                    data['category_group_name'],
                    data['rarity_color'],
                    data['icon_url'],
                    data['is_follow'],
                    data['redirect_url'],
                    data['exterior'],
                    data['rarity'],
                    data['market_hash_name'],
                    data['en_name'],
                    data['today_sale_count'],
                    data['today_sale_price'],
                    data['create_date'],
                    version_date
                )

                cursor.execute(insert_query, values)
                # cursor.execute("INSERT INTO `csgo`.`goods`( `goods_id`, `platform_id`, `market_name`, `sell_min_price`, `sell_max_num`, `sell_valuation`, `buy_max_price`, `buy_max_num`, `price_alter_percentage_7d`, `price_alter_value_7d`, `category_group_name`, `rarity_color`, `icon_url`, `is_follow`, `redirect_url`, `exterior`, `rarity`, `market_hash_name`, `en_name`) VALUES ('1', '1', '1', 1.00, 1, 1.00, 1.00, 1, 1.00, 1.00, '1', '1', '1', 1, '1', '1', '1', '1', '1')")
                connection.commit()  # 提交事务
            print(getNowTime()+"数据插入goods成功")
    
    except Error as e:
        print(f"数据库连接错误: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")

def insert_today_sale_data(data_tuple_list,version_date):
    insert_query = "INSERT INTO `csgo`.`csgo_db_deal`( `goods_name`, `icon_url`, `today_count`, `today_price`, `all_price`, `create_date`,`version_date`) VALUES (%s, %s,%s, %s,%s, %s, %s)"

    print(getNowTime()+"开始插入cs_db数据")
    try:
        # 连接到 MySQL 数据库
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # 执行插入查询
            for data in data_tuple_list:
                data['create_date']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                today_price=0
                if data['count']==0 or data['count'] is None:
                    today_price=0
                else:
                    today_price=round(data['price']/data['count']/100,2)
                
                price=0
                if data['price']==0 or data['price'] is None:
                    price=0
                else:
                    price=round(data['price']/100,2)
                    
                values = (
                    data['goodsName'],
                    data['iconUrl'],
                    data['count'],
                    today_price,
                    price,
                    data['create_date'],
                    version_date
                )

                cursor.execute(insert_query, values)
                connection.commit()  # 提交事务
            print(getNowTime()+"数据插入cs_db成功")
    
    except Error as e:
        print(f"数据库连接错误: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")



def save_soccer_data():
    print(str(datetime.now())+"  正在查询足球数据")
    # 保存足球数据
    soccer = soccersave.getFbSoccerData()
    if soccer is None:
        print("获取足球数据失败")
        return
    
    all_data=soccersave.tarnMySoccerData(soccer)

    if all_data is None or len(all_data)==0:
        print("获取足球数据为空")
        return
    



    insert_query = "INSERT INTO `csgo`.`soccer_analysis`(`soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type`, `m_type_value`, `m_odds`, `goal_home`, `goal_guest`, `start_time`, `create_time`, `s_type`, `s_type_value`, `s_odds`) VALUES\
    (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s, %s,%s)"

    print(getNowTime()+"开始插入soccer_analysis数据")
    
    # 连接到 MySQL 数据库
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
        
    if connection.is_connected():
        cursor = connection.cursor()
        # 执行插入查询
        for values in all_data:
            try:
                # print(values)
                inert_values = (
                    values.get('soccer_id',''),
                    values.get('race_name',''),
                    values.get('team_home',''),
                    values.get('team_guest',''),
                    values.get('team_cr',''),
                    values.get('c_time',0),
                    values.get('m_type',''),
                    values.get('m_type_value',0),
                    values.get('m_odds',0),
                    values.get('goal_home',''),
                    values.get('goal_guest',''),
                    values.get('start_time',None),
                    values['create_time'],
                    values.get('s_type',''),
                    values.get('s_type_value',0),
                    values.get('s_odds',0)
                )
                cursor.execute(insert_query, inert_values)
                connection.commit()  # 提交事务
            except Error as e:
                print(f"数据库soccer_analysis连接错误: {e}")
        # print(getNowTime()+"数据插入soccer_analysis成功")
    if connection.is_connected():
        cursor.close()
        connection.close()
        # print("数据库soccer_analysis连接已关闭")


    #  更新时间2024-12-09 12：00：00  

# 时间 盘口 当前进数 类型 金额   
    # bet_data=[[3,2,0,'大',20],[37,2.25,1,'大',20],[25,2.5,0,'大',40],[22,2.5,1,'大',40],[30,2.75,1,'大',40],[21,3,1,'大',20],[23,3.5,1,'大',20],\
    #             [3,1.75,0,'小',20],[13,3,0,'小',20],[5,3.25,0,'小',20],[22,3.25,1,'小',20],\
    #             [11,3.75,1,'大',40],[21,3.75,2,'大',40],[27,4,2,'大',20],\
    #                 [22,3.75,1,'小',20],[20,4,1,'小',20],[31,4.25,2,'小',20],[36,4.5,2,'小',20],\
                    
    #                     [65,2.75,2,'大',30],\
    #                         [29,1.75,0,'小',15],[68,1.75,1,'小',15],[56,1.5,0,'小',15],[74,1.5,1,'小',15]
    #                     ]
    
    bet_new_data=[[2,13,0,'大',1.75,20],\
                    [2,35,0,'大',1.5,20],\
                    [2,58,0,'大',0.75,20],\
                    [2,35,0,'小',1.25,20],\
                    [2,20,1,'大',2.75,20],\
                    [2,60,1,'大',1.75,20],\
                    [2.25,19,0,'大',1.75,20],\
                    [2.25,41,0,'小',1.25,20],\
                    [2.25,26,1,'大',2.75,20],\
                    [2.25,65,1,'大',1.75,20],\
                    [2.25,66,2,'大',2.75,20],\
                    [2.5,15,0,'小',2.25,20],\
                    [2.5,38,0,'小',1.5,20],\
                    [2.5,27,0,'大',1.75,20],\
                    [2.5,64,0,'大',0.75,20],\
                    [2.5,30,1,'大',2.75,20],\
                    [2.5,64,1,'大',1.75,20],\
                    [2.5,76,1,'小',1.5,20],\
                    [2.5,15,1,'小',3.25,20],\
                    [2.5,54,1,'小',2.25,20],\
                    [2.5,61,1,'小',2,20],\
                    [2.5,54,2,'小',3.25,20],\
                    [2.5,66,2,'大',2.75,20],\
                    [3,16,0,'大',2.75,20],\
                    [3,16,0,'小',2.5,20],\
                    [3,40,1,'大',2.75,20],\
                    [3,78,1,'小',1.5,20],\
                    [3,56,2,'小',3.25,20]]


    # bet_data=[[3,2,0,'大',40],[4,4,0,'大',20],\
    #     [3,1.75,0,'小',30],[29,1.75,0,'小',30],[28,2,0,'小',30],[23,2.25,0,'小',30],[24,2.5,0,'小',30],\
    #         [22,2.75,0,'小',30],[12,3,0,'小',30],[21,3.25,0,'小',20],[14,3.5,0,'小',20],[9,3.75,0,'小',20],\
                
    #             [29,2.25,1,'大',30],[23,2.5,1,'大',30],[29,2.75,1,'大',30],[22,3,1,'大',30],[34,3.5,1,'大',30],[10,3.75,1,'大',30],\
    #                 [35,3.25,1,'小',30],\
                        
    #                     [33,3.25,2,'大',20],[19,3.75,2,'大',20],\
    #                         [31,4.5,2,'小',20],\
                            


    #                         [58,1,0,'小',15],[51,1.25,0,'小',15],[56,1.5,0,'小',15],\
    #                         [74,1.5,1,'小',15],[68,1.75,1,'小',15],[62,2,1,'小',15],[55,2.25,1,'小',15],[51,2.5,1,'小',15],\
                            
    #                         [69,2.5,2,'大',15],[65,2.75,2,'大',15],\
    #                         [72,2.75,2,'小',15],[65,3,2,'小',15],[56,3.25,2,'小',15],[54,3.5,2,'小',15],
        


    #                         ]


        # 下注
    for values in all_data:
        print()
        print(str(values.get('soccer_id',"race_name"))+","+values.get('race_name',"race_name")+"，主队是："+values.get('team_home',"team_home")+"，客队是："+values.get('team_guest',"team_guest")+\
                "，时间："+str(values.get('c_time',''))
              )
        print("大："+str(values.get('m_type_value',''))+"，赔率："+str(values.get('m_odds',''))+\
                "----小："+str(values.get('s_type_value',''))+",赔率："+str(values.get('s_odds',0))+\
                "----主队进球："+str(values.get('goal_home',''))+",客队进球："+str(values.get('goal_guest',''))
              )

        # for bet in bet_data:
        #     if values.get('c_time',0)==bet[0] and values.get('m_type_value',0)==bet[1] and (values.get('goal_home',0)+ values.get('goal_guest',0))==bet[2]:
        #         time.sleep(1)
        #         print("开始bet"+str(values))
        #         threading.Thread(target=soccersave.save_bet_data,args=(values,bet[3],bet[4])).start()
        #         continue

        st_value= soccersave.get_soccer_data_start(values.get('soccer_id',0))
        print(str(st_value)+","+str(values.get('c_time',0))+","+str(values.get('goal_home',0) +values.get('goal_guest',0))+ ',x,'+str(values.get('m_type_value',0))+ ',20')

        if st_value is None:
            print("获取初盘数据失败")
            continue

        
        for bet in bet_new_data:
            if st_value==bet[0] and values.get('c_time',0)==bet[1] and (values.get('goal_home',0)+ values.get('goal_guest',0))==bet[2]\
                  and bet[4]==values.get('m_type_value',0) :
                print("开始bet，开始盘口是："+str(st_value))
                time.sleep(1)
                threading.Thread(target=soccersave.save_bet_data,args=(values,bet[3],bet[5])).start()
                continue




def updateMyBetHistoryList():
    print(str(datetime.now())+"  正在更新bet_history数据")
    soccersave.saveMyBetHistoryList(limit_page=6,page=1,page_size=10)



if __name__ == '__main__':
# def start():    
    start_time=int(time.time())
    # save_soccer_data()
    print(str(datetime.now())+"  开始运行了")

    # 每天晚上11点执行
    # schedule.every().day.at("23:00").do(save_data_mysql)
    # 持续运行以保持调度
    # 每隔一分钟执行一次
    schedule.every().minutes.at(":01").do(save_soccer_data)

    schedule.every().hour.do(updateMyBetHistoryList)

    log_num=0
    while True:
        schedule.run_pending()
        time.sleep(1)
        log_num+=1

        if log_num%10==0:
            print(str(datetime.now())+"  正在运行中,第"+str(log_num//10)+"次执行")



    # save_data_mysql()

    end_time=int(time.time())
    print("运行时间："+str(end_time-start_time))




