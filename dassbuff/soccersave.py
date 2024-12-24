import requests
import json
import datetime
import math
import config
import time
import mysql.connector
from mysql.connector import Error
import re
import messagesend as messagesend


# 数据库连接参数
host = '127.0.0.1'
database = 'csgo'
user = 'root'
password = 'bangye'

has_notified=False

# 数据
def getFbSoccerData():
    try:
        # 设置请求的URL
        url = 'https://api.xyz7477.com/v1/match/getList'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
            }
        # 设置请求的数据
        params = {
            "languageType": "CMN",
            "oddsType": 1,
            "current": 1,
            "orderBy": 1,
            "isPC": 'true',
            "sportId": 1,
            "type": 1
        }
        # 发送POST请求
        response = requests.post(url,headers=headers,json=params)
        # print(response)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            soccer=reponse_json['data']
            return soccer
        return None
    except Exception as e:
        print(e)
        return None




def tarnMySoccerData(soccer):
    all_data=[]
    if soccer is None or len(soccer['records'])==0:
        return None
    
    for item in soccer['records']:
        # print(item)
        single_data={}
        single_data['soccer_id'] = item['id']
        single_data['team_cr'] = item['lg']['rnm']
        single_data['race_name'] = item['lg']['na']
        single_data['team_home'] = item['ts'][0]['na']
        single_data['team_guest'] = item['ts'][1]['na']

        # 当前时间向下取整
        single_data['c_time'] = math.ceil(item['mc'].get('s',0)/60) 
        for t_type in item['mg']:
            if 1007 == t_type['mty'] and 1001 == t_type['pe'] :
                for t_type in t_type['mks'][0]['op']:
                    if '大' in t_type['na']:
                        if '/' in t_type['li']:
                            single_data['m_type_value'] =  (eval(t_type['li'].split('/')[0])+eval(t_type['li'].split('/')[1]))/2
                        else:
                            single_data['m_type_value'] = eval(t_type['li'])

                        single_data['m_type'] = t_type['na']
                        single_data['m_odds'] =  t_type['bod']
                    elif '小' in t_type['na']:
                        
                        if '/' in t_type['li']:
                            single_data['s_type_value'] =  (eval(t_type['li'].split('/')[0])+eval(t_type['li'].split('/')[1]))/2
                        else:
                            single_data['s_type_value'] = eval(t_type['li'])

                        single_data['s_type'] = t_type['na']
                        single_data['s_odds'] =  t_type['bod']


        #当前比分 和最终比分
        for goal in item['nsg']:
            if 1001 == goal['pe'] and 5 == goal['tyg']:
                single_data['goal_home'] = goal['sc'][0]
                single_data['goal_guest'] = goal['sc'][1]
        single_data['start_time'] = datetime.datetime.fromtimestamp(item['bt']/1000).strftime('%Y-%m-%d %H:%M:%S')
        single_data['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        all_data.append(single_data)


    return all_data

# 获取详情
def getMatchDetail(matchId,oddsType):
    try:
        # 设置请求的URL
        url = 'https://api.xyz2277.com/v1/match/getMatchDetail'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
            }
        # 设置请求的数据
        params = {
            "languageType": "CMN",
            "oddsType": oddsType,
            "matchId": matchId,
        }
        # 发送POST请求
        response = requests.post(url,headers=headers,json=params)
        # print(response)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            detail=reponse_json['data']
            # 过滤平均销量大于30的列表
            return detail
        return None
    except Exception as e:
        print(e)
        return None



# 下注
def singlePass(authorization,singleBetList):
    # orderIds=[]
    try:
        # 设置请求的URL
        url = 'https://api.xyz2277.com/v1/order/bet/singlePass'
        # 设置请求头
        headers = {
            "Connection":"keep-alive",
            "Origin":"https://p.9512230.com",
            "Referer":"https://p.9512230.com/",
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Authorization': authorization,
            'content-type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
            }
        # 设置请求的数据
        params = {
            "languageType": "CMN",
            "singleBetList": [{
                "unitStake": singleBetList[0]['unitStake'],
                "oddsChange": singleBetList[0]['oddsChange'],
                "betOptionList": [
                    {
                        "marketId": singleBetList[0]['betOptionList'][0]['marketId'],
                        "odds": singleBetList[0]['betOptionList'][0]['odds']-0.1,
                        "optionType": singleBetList[0]['betOptionList'][0]['optionType'],
                        "oddsFormat": singleBetList[0]['betOptionList'][0]['oddsFormat']
                    }
                ]
            }],
            "currencyId": 1,

        }
        print(params)
        # 发送POST请求
        response = requests.post(url,headers=headers,json=params)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            print(reponse_json)
            if reponse_json['code'] == 0:
                detail=reponse_json['data']
                return detail
            else:
                print(reponse_json['message'])
        return None
    except Exception as e:
        print(e)
        return None



# 下注
def getStakeOrderStatus(authorization,orderIds):
    status_result={}
    status_result['msg'] = ""
    status_result['orderStatus'] = False

    if len(orderIds)==0:
        return status_result
    
    try:
        # 设置请求的URL
        url = 'https://api.xyz2277.com/v1/order/getStakeOrderStatus'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Authorization': authorization,
            'content-type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
            }
        # 设置请求的数据
        params = {
            "languageType": 'CMN',
            "orderIds": orderIds,
        }

        # 发送POST请求
        response = requests.post(url,headers=headers,json=params)
        print(response)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            print("查询订单状态为："+str(reponse_json))
            if reponse_json['code'] == 0 and reponse_json['data'][0].get('rjs',None) is None:
                status_result['msg'] = reponse_json['data'][0].get('rjs',"成功")
                status_result['orderStatus'] = True

    except Exception as e:
        print(e)

    return status_result


# 获取余额
def getBalance(authorization):
    try:
        # 设置请求的URL
        url = 'https://api.xyz2277.com/v1/user/base'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Authorization': authorization,
            'content-type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
            }
        # 设置请求的数据
        params = {
            "languageType": "CMN",
        }
        # 发送POST请求
        response = requests.post(url,headers=headers,json=params)
        print(response)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            # if reponse_json['code'] == 14010:
            #     print("token失效")
            #     return None
                
            # if reponse_json['code'] == 0:
            #     print("查询成功："+reponse_json)
            #     balance=reponse_json['data']
            #     return balance
        return reponse_json
    except Exception as e:
        print(e)
        return None


def tranTypeValue(typeValue):
    if '/' in typeValue:
        return  (eval(typeValue.split('/')[0])+eval(typeValue.split('/')[1]))/2
    else:
        return  eval(typeValue)

def getMatchList(deatail,bet_amount=10,type='大'):
    # if balance is None or balance['bl']<bet_amount:
    #     print("余额不足,当前余额是："+str(balance['bl']))
    #     return None
    
    hashFalg=False
    for mg in deatail['mg']:
        if 1007 == mg['mty'] and 1001 == mg['pe'] :
            marketId = mg['mks'][0]['id']
            for t_type in mg['mks'][0]['op']:
                if type in t_type['na']:
                    odds =  t_type['bod']
                    oddsFormat =  t_type['odt']
                    optionType =  t_type['ty']
                    currentValue=tranTypeValue(t_type['li'])
                    hashFalg=True
                    break
                elif type in t_type['na']:
                    odds =  t_type['bod']
                    oddsFormat =  t_type['odt']
                    optionType =  t_type['ty']
                    currentValue=tranTypeValue(t_type['li'])
                    hashFalg=True
                    break

    if not hashFalg:
        print("没有找到大盘数据")
        return None
    
    singleBetList=[]
    single={
        "currentValue": currentValue,
        "unitStake": bet_amount,
        "oddsChange": 1,
        "betOptionList": [
            {
                "marketId": marketId,
                "odds": odds,
                "optionType": optionType,
                "oddsFormat": oddsFormat
            }
        ]
    }
    singleBetList.append(single)
    return singleBetList


def gobuyitone(matchId,currentNum,bet_amount,type):
    order_result={}
    order_result['orderStatus']=False
    order_result['require_amount']=currentNum
    order_result['msg']=''
    order_result['bet_amount']=bet_amount
    order_result['matchId']=matchId
    

    global has_notified
    # 获取余额，查询比赛，封装下注，下注，查询订单状态
    balance_response=getBalance(config.itone_authorization)
    if balance_response['code'] == 14010:
        order_result['msg'] = "token失效，通知管理员"
        order_result['orderStatus'] = True
        messagesend.notify_email(order_result['msg'],has_notified)
        has_notified=True
        return order_result
    
    elif balance_response['code'] == 0:
        print("查询成功,余额为："+str(balance_response['data']['bl']) )
        order_result['balance'] = balance_response['data']['bl']
    else:
        order_result['msg'] = "余额查询失败："+str(balance_response)
        order_result['orderStatus'] = False
        return order_result
    
    if float(order_result.get('balance',0)) < float(bet_amount):
        order_result['msg'] = "余额不足，当前余额是："+str(order_result['balance'])
        order_result['orderStatus'] = True
        messagesend.notify_email(order_result['msg'],has_notified)
        has_notified=True
        return order_result

    deatail = getMatchDetail(matchId,1)
    singleBetList=getMatchList(deatail,bet_amount,type)
    print(singleBetList)

    if singleBetList is None or len(singleBetList)==0:
        order_result['msg'] = "没有找到大盘数据,等几分钟在尝试"
        order_result['orderStatus'] = False
        return order_result
# 
    # order_result['currentValue'] = singleBetList[0].get('currentValue',0) 
    # print("当前比赛盘口已变化，无需重复下注,当前盘口为："+str(singleBetList[0].get('currentValue',0) )+"，下注盘口为："+ str(currentNum))
    order_result['currentValue']=singleBetList[0].get('currentValue',0)


    if singleBetList[0].get('currentValue',0) != currentNum:
        print("当前比赛盘口已变化，无需重复下注,当前盘口为："+str(singleBetList[0].get('currentValue',0) )+"，下注盘口为："+ str(currentNum))
        order_result['msg'] = "当前比赛盘口已变化"
        return order_result

    #判断要下注的比赛大小，是否和当前比赛的大小一致

    # 太快会导致失败
    singlePassDetail=singlePass(config.itone_authorization,singleBetList)


    orderIds=[]
    if singlePassDetail is not None:
        order_result['bet_id']=singlePassDetail[0]['id']
        for item in singlePassDetail:
            orderIds.append(item['id'])

    
    status_result=getStakeOrderStatus(config.itone_authorization,orderIds)
    if status_result['orderStatus']:
        order_result['msg'] = status_result['msg']
        order_result['orderStatus'] = status_result['orderStatus']
    
    return order_result

def start_buy_itone(matchId,currentNum,bet_amount,type):
    for i in range(1,3):
        order_result=gobuyitone(matchId,currentNum,bet_amount,type)
        if order_result['orderStatus']:
            return order_result
        # 失败，则等待x秒后再试
        time.sleep(15)
    
    return order_result


def getNowTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def save_bet_data(values,type='大',bet_amount=10):
    print(getNowTime()+"  正在存储下注数据")
    # 这里取下注
    order_result=start_buy_itone(values.get('soccer_id',None),values.get('m_type_value',0),bet_amount,type)

    # order_result = start_buy_itone(2775624,0.75,bet_amount)
    print(order_result)
    
    insert_query = "INSERT INTO `csgo`.`soccer_bet`(`soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type`, `m_type_value`, `m_odds`, `odds_amount`, `odds_result`, `start_time`, `create_time`,`odds_status`,`actual_type_value`,`bet_id`) VALUES\
    (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s, %s, %s, %s)"

    print(getNowTime()+"开始插入 soccer_bet 数据")
    
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
        try:
            print(values)
            inert_values = (
                values.get('soccer_id',''),
                values.get('race_name',''),
                values.get('team_home',''),
                values.get('team_guest',''),
                values.get('team_cr',''),
                values.get('c_time',0),
                type,
                values.get('m_type_value',0),
                values.get('m_odds',0),
                bet_amount,
                order_result.get('msg','无日志'),
                values.get('start_time',None),
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                order_result.get('orderStatus',False),
                order_result.get('currentValue',0),
                order_result.get('bet_id',""),
            )
            print(inert_values)
            cursor.execute(insert_query, inert_values)
            connection.commit()  # 提交事务
        except Error as e:
            print(f"数据库soccer_bet连接错误: {e}")
        print(getNowTime()+"数据插入soccer_bet成功")
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("数据库soccer_bet连接已关闭")

    return True






# 获取余额
def getMyBetHistoryList(authorization,page=1,page_size=10):
    try:
        # 设置请求的URL
        url = 'https://api.xyz2277.com/v1/order/new/bet/list'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Authorization': authorization,
            'content-type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
            }
        # 设置请求的数据
        params = {
            "languageType": "CMN",
            "isSettled": True,
            "current": page,
            "size": page_size,
        }
        # 发送POST请求
        response = requests.post(url,headers=headers,json=params)
        print(response)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            if reponse_json['code'] == 14010:
                print("token失效")
                return None
            
        return reponse_json
    except Exception as e:
        print(e)
        return None



def saveMyBetHistoryList(limit_page=5,page=1,page_size=10):
     
    while True:
        print("获取第"+str(page)+"页数据")
        time.sleep(2)
        if limit_page<page:
            print("获取数据结束了，退出")
            break
        
        # 睡眠1秒，防止频繁请求
        page_data=getMyBetHistoryList(config.itone_authorization,page,page_size)
        if page_data is None:
            print("获取数据失败，退出")
            break
        
        if page_data['code']!= 0:
            print("获取数据失败，退出")
            break
        
        if 'data' not in page_data or len(page_data['data']['records'])==0 :
            print("没有数据了，退出")
            break
        
        
        for item in page_data['data']['records']:
            try:
                # print(item)
                # save_bet_data(item)
                if 'bsc' in item['ops'][0]:
                    goal=extract_numbers(item['ops'][0]['bsc'])
                else:
                    goal=[0,0]
                goal_reslut=extract_numbers(item['ops'][0].get('rs',"0-0"))



                bet_history_data=(
                    item['id'],
                    item['ops'][0]['mid'],
                    item['ops'][0]['ln'],
                    item['ops'][0]['te'][0]['na'],
                    item['ops'][0]['te'][1]['na'],
                    "",
                    0,
                    item['ops'][0]['on'],
                    item['ops'][0]['li'],
                    item['ops'][0]['bo'],

                    goal[0],
                    goal[1],
                    item['sat'],
                    goal_reslut[0],
                    goal_reslut[1],
                    item['uwl'],
                    datetime.datetime.fromtimestamp(item['cte']/1000).strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.datetime.fromtimestamp(item['ops'][0]['bt']/1000).strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    bet_history_victory(float(item['sat']),float(item['ops'][0]['bo']),float(item['uwl'])),
                    datetime.datetime.now().strftime('%Y-%m-%d'),
                )
                # print(bet_history_data)
                insert_if_not_exists(item['id'], item['ops'][0]['mid'], bet_history_data)
            except Exception as e:
                print("解析数据失败")
                print(e)


        page+=1
    print("获取数据结束,开始更新历史数据")
    update_cr_bettime()



def bet_history_victory(odds_amount,m_odds,odds_amount_result):
    print(odds_amount,m_odds,odds_amount_result)
    if odds_amount_result > 0 and odds_amount_result > odds_amount*(m_odds-1)*0.9:
        return "胜"
    elif odds_amount_result > 0 and odds_amount_result < odds_amount*(m_odds-1)*0.9:
        return "胜一半"
    elif odds_amount_result < 0 and odds_amount == -odds_amount_result:
        return "负"
    elif odds_amount_result < 0 and odds_amount == -odds_amount_result*0.5:
        return "负一半"
    elif odds_amount_result == 0:
        return "平"
    else:
        return "未知"


def insert_if_not_exists(bet_id, soccer_id, insert_data):
  
    try:
        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        # 连接到数据库
        if conn.is_connected():
            cursor = conn.cursor()

            # 构建查询条件

            # 查询是否存在
            cursor.execute("select count(1) from soccer_bet_history where bet_id="+str(bet_id)+" and soccer_id="+str(soccer_id))
            exists = cursor.fetchone()[0] > 0
            if not exists:
                print(insert_data)
                insert_query = "INSERT INTO `csgo`.`soccer_bet_history`(`bet_id`, `soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type`, `m_type_value`, `m_odds`, `goal_home`, `goal_guest`, `odds_amount`, `goal_home_result`, `goal_guest_result`, `odds_amount_result`, `bet_time`, `start_time`, `create_time`, `result_flag`,`bet_time_day`) VALUES\
                (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s,%s)"
                cursor.execute(insert_query, insert_data)
                conn.commit()

                print(getNowTime()+"数据插入 soccer_bet_history 成功")
            else:
                print("数据已存在，未进行插入操作")
    except Error as e:
       print(f"数据库 soccer_bet_history 连接错误: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库 soccer_bet_history 连接已关闭")

    return True



def get_soccer_data_start(soccer_id):
  
    try:
        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        # 连接到数据库
        if conn.is_connected():
            cursor = conn.cursor()

            # 构建查询条件

            # 查询是否存在
            cursor.execute("select m_type_value from soccer_analysis_start where c_time<10 and soccer_id ="+str(soccer_id) + " limit 1")
            row = cursor.fetchone()
            if row is not None :
                return row[0]
            else:
                print("数据不存在")
    except Error as e:
       print(f"数据库 soccer_analysis_start 连接错误: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库 soccer_analysis_start 连接已关闭")

    return None




def update_cr_bettime():
  
    try:
        # 连接到 MySQL 数据库
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        # 连接到数据库
        if conn.is_connected():
            cursor = conn.cursor()

            # 构建查询条件

            # 查询是否存在
            cursor.execute("UPDATE soccer_bet_history his LEFT JOIN soccer_bet bet on his.soccer_id  =bet.soccer_id and his.m_type  =bet.m_type and his.m_type_value  =bet.m_type_value set his.team_cr= bet.team_cr, his.c_time= bet.c_time where his.team_cr=''  and his.c_time=0")
            print(getNowTime()+"更新国家和时间成功")
            conn.commit()
    except Error as e:
       print(f"数据库 soccer_bet_history 连接错误: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库 soccer_bet_history 连接已关闭")

    return True



def extract_numbers(s):
    # 使用正则表达式提取数字
    numbers = re.findall(r'\d+', s)
    # 将提取的数字转为集合，确保唯一性
    return numbers





    

    
if __name__ == '__main__':
    # 下注
    # values={}
    # values['soccer_id']= 2868972
    # values['m_type_value']=6
    # # values['c_time']=45
    # bet_amount=12
    # save_bet_data(values,type='大',bet_amount=bet_amount)
# 示例字符串
    saveMyBetHistoryList(limit_page=5,page=1,page_size=10)
    # notify_email("测试邮件")
    # get_soccer_data_start(2846449)


