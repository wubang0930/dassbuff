import json
from datetime import datetime

import pandas as pd
import re
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
import os
import log_utils
import messagesend as messagesend


log_num=0

# 数据库连接参数
host = '127.0.0.1'
database = 'csgo'
user = 'root'
password = 'bangye'

taobao_price=545

# 全局变量
domain_cookie = None
domain = None
cookies = None
authorization = None
has_notified=False


def update_global_vars(new_domain_cookie):
    """更新全局变量"""
    global domain_cookie, domain, cookies, authorization
    domain_cookie = new_domain_cookie
    domain = domain_cookie.get("domain")
    cookies = domain_cookie.get("cookies")
    authorization = domain_cookie.get("authauthorization")




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


def getNowTime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')




def save_soccer_data():
    print("正在查询足球数据")
    # 保存足球数据
    soccer = soccersave.getFbSoccerData(domain_cookie)
    if soccer is None:
        print("获取足球数据失败")
        return
    
    all_data=soccersave.tarnMySoccerData(soccer)

    if all_data is None or len(all_data)==0:
        print("获取足球数据为空")
        return
    



    insert_query = "INSERT INTO `csgo`.`soccer_analysis`(`soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type`, `m_type_value`, `m_odds`, `goal_home`, `goal_guest`, `start_time`, `create_time`, `s_type`, `s_type_value`, `s_odds`) VALUES\
    (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s, %s,%s)"

    print("开始插入soccer_analysis数据")
    
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

                # 插入首次数据
                insert_soccer_analysis_start_new(cursor, values)
                

                connection.commit()  # 提交事务
            except Error as e:
                print(f"数据库soccer_analysis连接错误: {e}")
    if connection.is_connected():
        cursor.close()
        connection.close()
        # print("数据库soccer_analysis连接已关闭")


    bet_new_data=[\
# [1.75,3,0,'小',1.75,20],\
# [2.25,5,0,'小',2.25,20],\
# [3,78,3,'小',3.5,20],\
# [3,16,0,'小',2.5,20],\
# [3,78,1,'小',1.5,20],\ # 这个由小转为大
# [2,3,0,'大',2,50],\
# [2,35,0,'小',1.25,50],\
# [2.5,59,3,'小',4,50],\
# [2.5,64,1,'大',1.75,50],\
# [2.75,52,0,'小',1.25,50],\
# [3,78,1,'大',1.5,50],\
# [3.25,12,0,'小',3,50],\



#  这3个胜率比较大
[1.75,3,0,'小',1.75,50],\
[1.5,1,0,'小',1.5,90],\
[2,20,1,'大',2.75,50],\
[2,63,2,'大',2.75,50],\
[2.25,1,0,'小',2.25,90],\
[2.5,30,1,'大',2.75,50],\
[2.5,59,3,'小',4,50],\
[2.75,67,2,'大',2.75,50],\
[2.75,56,2,'小',3.25,50],\
[3,1,0,'小',3,90],\

                    ]
    # 初盘、时间、总进球（没有盘口参数）
    bet_new_data_two=[\
#  这3个胜率比较大
[2,40,0,'大',60],\
[2.25,56,0,'大',60],\
[2.5,37,1,'大',60],\
[2.75,20,0,'大',60],\
[2.75,60,1,'大',60],\

                    ]
        # 下注
    log_time="当前时间是：" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(log_time)
   

    # 获取余额，
    order_result = {}
    global has_notified
    balance_response=soccersave.getBalance(authorization)
    if balance_response and balance_response['code'] == 14010:
        order_result['msg'] = "token失效，通知管理员"
        order_result['orderStatus'] = True
        messagesend.notify_email(order_result['msg'],has_notified)
        has_notified=True
    elif balance_response and balance_response['code'] == 0:
        print("查询成功,余额为："+str(balance_response['data']['bl']) )
        order_result['balance'] = balance_response['data']['bl']
    else:
        order_result['msg'] = "余额查询失败："+str(balance_response)
        order_result['orderStatus'] = False
        messagesend.notify_email(order_result['msg'],has_notified)
        has_notified=True
    
   

    for values in all_data:
        log_head=str(values.get('soccer_id',"race_name"))+","+values.get('race_name',"race_name")+"，主队是："+values.get('team_home',"team_home")+"，客队是："+values.get('team_guest',"team_guest")+\
                "，时间："+str(values.get('c_time',''))
        log_line="大："+str(values.get('m_type_value',''))+"，赔率："+str(values.get('m_odds',''))+\
                "----小："+str(values.get('s_type_value',''))+",赔率："+str(values.get('s_odds',0))+\
                "----主队进球："+str(values.get('goal_home',''))+",客队进球："+str(values.get('goal_guest',''))
        
        print(log_head)
        print(log_line)



      
        # if values.get('c_time',0)==1 and values.get('m_type_value',0)==3:
        #     print("开始bet，第1分钟，小3球，开始盘口是："+str(values))
        #     time.sleep(1)
        #     threading.Thread(target=soccersave.save_bet_data,args=(values,'小',72,domain_cookie)).start()



        st_value= soccersave.get_soccer_data_start(values.get('soccer_id',0))
        print("初盘:"+str(st_value)+",当前时间："+str(values.get('c_time',0))+",当前总进球："+str(values.get('goal_home',0) +values.get('goal_guest',0))+ ',当前盘口：'+str(values.get('m_type_value',0)))

        if st_value is None:
            print("获取初盘数据失败")
            continue

        # [2.75,56,2,'小',3.25,50]
        for bet in bet_new_data:
            if st_value==bet[0] and values.get('c_time',0)==bet[1] and (values.get('goal_home',0)+ values.get('goal_guest',0))==bet[2]\
                  and bet[4]==values.get('m_type_value',0) :
                print("开始bet，开始盘口是："+str(st_value))
                time.sleep(2)
                threading.Thread(target=soccersave.save_bet_data,args=(values,bet[3],bet[5],domain_cookie)).start()

                continue
        # [2.75,60,1,'大',50]            
        for bet_two in bet_new_data_two:
            if st_value==bet_two[0] and values.get('c_time',0)==bet_two[1] and (values.get('goal_home',0)+ values.get('goal_guest',0))==bet_two[2] :
                print("开始bet第2类型，开始盘口是："+str(st_value))
                time.sleep(2)
                threading.Thread(target=soccersave.save_bet_data,args=(values,bet_two[3],bet_two[4],domain_cookie)).start()

                continue

        

def insert_soccer_analysis_start_new(cursor, values):
    """
    判断soccer_analysis_start_new表中是否有该数据，如果没有则插入
    """
    # BUG分析：
    # 1. SQL: SELECT * ... WHERE soccer_id = %s 只判断了soccer_id，未判断c_time，可能导致同一场比赛多条c_time=0,1,2,3,4的数据只插入一条
    # 2. inert_values 直接用，可能与soccer_analysis_start_new表字段不完全匹配，尤其是create_time等字段
    # 3. insert_query变量名重复，容易混淆
    # 4. values.get('soccer_id',0)如果为0，可能插入脏数据
    # 修正建议：增加c_time判断，且只插入c_time<5的唯一数据
    if values.get('c_time') is not None and values.get('c_time') <= 5:
        sql_check_start_new = "SELECT * FROM `csgo`.`soccer_analysis_start_new` WHERE `soccer_id` = %s"
        cursor.execute(sql_check_start_new, (values.get('soccer_id',''),))
        result = cursor.fetchone()
        if result is None:
            print("插入soccer_analysis_start_new数据")
            insert_query_start_new = "INSERT INTO `csgo`.`soccer_analysis_start_new`(`soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type`, `m_type_value`, `m_odds`, `goal_home`, `goal_guest`, `start_time`, `create_time`, `s_type`, `s_type_value`, `s_odds`) VALUES\
            (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s,%s, %s,%s)"
            inert_values_start_new = (
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
            cursor.execute(insert_query_start_new, inert_values_start_new)
        else:
            print("soccer_analysis_start_new数据已存在")    




def updateMyBetHistoryList(domain_cookie2,limit_page,page,page_size):
    update_global_vars(domain_cookie2)
    print("正在更新bet_history数据", domain_cookie2, limit_page, page, page_size)
    soccersave.saveMyBetHistoryList(domain_cookie2=domain_cookie2, limit_page=limit_page, page=page, page_size=page_size)

    now_ts = int(time.time() * 1000)
    begin_time = now_ts - 6 * 60 * 60 * 1000
    end_time = now_ts
    print("开始时间："+str(begin_time)+"结束时间："+str(end_time))
    soccersave.get_all_match_result_page(domain_cookie2, begin_time, end_time, 2, 0, "CMN", "1", 50)


def init_file():
    if os.path.exists(config.log_file):
        os.remove(config.log_file)
        
    with open(config.log_file, 'a+', encoding='utf-8') as f:
        f.write("日志文件初始化"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'\n')


def startBetSoccer(domain_cookie):
        # 更新全局变量
    update_global_vars(domain_cookie)
    schedule.every().minutes.at(":01").do(save_soccer_data)
    log_num=0
    while True:
        schedule.run_pending()
        time.sleep(1)
        log_num+=1

        if log_num%10==0:
            print("正在运行中,第"+str(log_num//10)+"次执行")




if __name__ == '__main__':
# def start():    
    start_time=int(time.time())
    log_file_name = f"main-{datetime.now().strftime('%Y%m%d')}"
    log_utils.init_logger(log_file_name)
    # # save_soccer_data()
    # print(str(datetime.now())+"  开始运行了")
    # # init_file()

    # # 每天晚上11点执行
    # # schedule.every().day.at("23:00").do(save_data_mysql)
    # # 持续运行以保持调度
    # # 每隔一分钟执行一次
    # schedule.every().minutes.at(":01").do(save_soccer_data)

    # schedule.every().hour.do(updateMyBetHistoryList)

    # log_num=0
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    #     log_num+=1

    #     if log_num%10==0:
    #         print(str(datetime.now())+"  正在运行中,第"+str(log_num//10)+"次执行")



    # # save_data_mysql()

    # end_time=int(time.time())
    # print("运行时间："+str(end_time-start_time))




