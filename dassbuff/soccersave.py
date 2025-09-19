from turtle import up
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
from logger_config import setup_loggers


logger = setup_loggers()

# 数据库连接参数
host = '127.0.0.1'
database = 'csgo'
user = 'root'
password = 'bangye'

has_notified=False


# 全局变量
domain_cookie = None
domain = None
cookies = None
authorization = None

def update_global_vars(new_domain_cookie):
    """更新全局变量"""
    global domain_cookie, domain, cookies, authorization
    domain_cookie = new_domain_cookie
    domain = domain_cookie.get("domain")
    cookies = domain_cookie.get("cookies")
    authorization = domain_cookie.get("authauthorization")


# 数据
def getFbSoccerData(domain_cookie):
    update_global_vars(domain_cookie)

    try:
        # 设置请求的URL
        url = f'{domain}/v1/match/getList'
        logger.debug(f"请求URL: {url}")
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
        logger.debug(f"请求响应: {response.status_code} {response.text[:200]}")
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            soccer=reponse_json['data']
            return soccer
        return None
    except Exception as e:
        logger.error(f"getFbSoccerData异常: {e}")
        return None




def tarnMySoccerData(soccer):
    all_data=[]
    if soccer is None or 'records' not in soccer or len(soccer['records']) == 0:
        return None
    
    for item in soccer['records']:
        # logger.debug(item)
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
        url = f'{domain}/v1/match/getMatchDetail'
        logger.debug(f"请求URL: {url}")
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
        logger.debug(f"请求响应: {response.status_code} {response.text[:200]}")
        # logger.debug(response)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            logger.debug(f"返回数据: {reponse_json}")
            detail=reponse_json['data']
            # 过滤平均销量大于30的列表
            return detail
        return None
    except Exception as e:
        logger.error(f"getMatchDetail异常: {e}")
        return None



# bet
def singlePass(singleBetList):
    # orderIds=[]
    try:
        # 设置请求的URL
        url = f'{domain}/v1/order/bet/singlePass'
        logger.debug(f"请求URL: {url}")
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
        logger.debug(f"bet参数: {params}")
        # 发送POST请求
        response = requests.post(url,headers=headers,json=params)
        logger.debug(f"bet响应: {response.status_code} {response.text[:200]}")
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            if reponse_json['code'] == 0:
                detail=reponse_json['data']
                return detail
            else:
                logger.debug(f"bet失败: {reponse_json.get('message', '')}")
        return None
    except Exception as e:
        logger.error(f"singlePass异常: {e}")
        return None



# bet
def getStakeOrderStatus(orderIds):
    status_result={}
    status_result['msg'] = ""
    status_result['orderStatus'] = False

    if len(orderIds)==0:
        return status_result
    
    try:
        # 设置请求的URL
        url = 'https://api.xyz2277.com/v1/order/getStakeOrderStatus'
        logger.debug(f"请求URL: {url}")
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
        logger.debug(f"订单状态响应: {response.status_code} {response.text[:200]}")
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            logger.info(f"查询订单状态为: {reponse_json}")
            if reponse_json['code'] == 0 and reponse_json['data'][0].get('rjs',None) is None:
                status_result['msg'] = reponse_json['data'][0].get('rjs',"成功")
                status_result['orderStatus'] = True

    except Exception as e:
        logger.error(f"getStakeOrderStatus异常: {e}")

    return status_result


# 获取余额
def getBalance(authorization):
    try:
        # 设置请求的URL
        url = 'https://api.xyz2277.com/v1/user/base'
        logger.debug(f"请求URL: {url}")
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
        logger.debug(f"余额查询响应: {response.status_code} {response.text[:200]}")
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            # if reponse_json['code'] == 14010:
            #     logger.debug("token失效")
            #     return None
                
            # if reponse_json['code'] == 0:
            #     logger.debug("查询成功："+reponse_json)
            #     balance=reponse_json['data']
            #     return balance
        return reponse_json
    except Exception as e:
        logger.error(f"getBalance异常: {e}")
        return None


def tranTypeValue(typeValue):
    if '/' in typeValue:
        return  (eval(typeValue.split('/')[0])+eval(typeValue.split('/')[1]))/2
    else:
        return  eval(typeValue)

def getMatchList(deatail,bet_amount=10,type='大'):
    # if balance is None or balance['bl']<bet_amount:
    #     logger.debug("余额不足,当前余额是："+str(balance['bl']))
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
        logger.debug("没有找到大盘数据")
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
    # 获取余额，查询比赛，封装bet，bet，查询订单状态
    balance_response=getBalance(authorization)
    if balance_response['code'] == 14010:
        order_result['msg'] = "token失效，通知管理员"
        order_result['orderStatus'] = True
        logger.info(order_result['msg'])
        messagesend.notify_email(order_result['msg'],has_notified)
        has_notified=True
        return order_result
    
    elif balance_response['code'] == 0:
        logger.info(f"查询成功,余额为：{balance_response['data']['bl']}")
        order_result['balance'] = balance_response['data']['bl']
    else:
        order_result['msg'] = f"余额查询失败：{balance_response}"
        order_result['orderStatus'] = False
        logger.info(order_result['msg'])
        return order_result
    
    if float(order_result.get('balance',0)) < float(bet_amount):
        order_result['msg'] = f"余额不足，当前余额是：{order_result['balance']}"
        order_result['orderStatus'] = True
        logger.info(order_result['msg'])
        messagesend.notify_email(order_result['msg'],has_notified)
        has_notified=True
        return order_result

    deatail = getMatchDetail(matchId,1)
    singleBetList=getMatchList(deatail,bet_amount,type)
    # logger.debug(singleBetList)

    if singleBetList is None or len(singleBetList)==0:
        order_result['msg'] = "没有找到大盘数据,等几分钟在尝试"
        order_result['orderStatus'] = False
        logger.info(order_result['msg'])
        return order_result
# 
    # order_result['currentValue'] = singleBetList[0].get('currentValue',0) 
    # logger.debug("当前比赛盘口已变化，无需重复bet,当前盘口为："+str(singleBetList[0].get('currentValue',0) )+"，bet盘口为："+ str(currentNum))
    order_result['currentValue']=singleBetList[0].get('currentValue',0)


    if singleBetList[0].get('currentValue',0) != currentNum:
        logger.debug(f"当前比赛盘口已变化，无需重复bet,当前盘口为：{singleBetList[0].get('currentValue',0)}，bet盘口为：{currentNum}")
        order_result['msg'] = "当前比赛盘口已变化"
        return order_result

    #判断要bet的比赛大小，是否和当前比赛的大小一致

    # 太快会导致失败
    singlePassDetail=singlePass(singleBetList)


    orderIds=[]
    if singlePassDetail is not None:
        order_result['bet_id']=singlePassDetail[0]['id']
        for item in singlePassDetail:
            orderIds.append(item['id'])

    # 这里暂停3秒后再次查询
    time.sleep(3)
    status_result=getStakeOrderStatus(orderIds)
    if status_result['orderStatus']:
        order_result['msg'] = status_result['msg']
        order_result['orderStatus'] = status_result['orderStatus']
        logger.debug(f"bet结果: {order_result['msg']}")
    
    return order_result

def start_buy_itone(matchId,currentNum,bet_amount,type):
    for i in range(1, 2):
        logger.info(f"开始第{i}次尝试下单")
        order_result = gobuyitone(matchId, currentNum, bet_amount, type)
        if order_result['orderStatus']:
            logger.info(f"第{i}次尝试成功")
            return order_result
        # 失败，则等待x秒后再试
        logger.info(f"第{i}次尝试失败，等待10秒后再试")
        time.sleep(10)
    return order_result


def getNowTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def save_bet_data(values,type='大',bet_amount=10,domain_cookie=None):
    update_global_vars(domain_cookie)

    logger.debug("正在存储bet数据")
    # 这里取bet
    order_result=start_buy_itone(values.get('soccer_id',None),values.get('m_type_value',0),bet_amount,type)

    # order_result = start_buy_itone(2775624,0.75,bet_amount)
    logger.debug(f"bet结果: {order_result}")
    
    insert_query = "INSERT INTO `csgo`.`soccer_bet`(`soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type`, `m_type_value`, `m_odds`, `odds_amount`, `odds_result`, `start_time`, `create_time`,`odds_status`,`actual_type_value`,`bet_id`) VALUES\
    (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, %s, %s, %s, %s)"

    logger.debug("开始插入 soccer_bet 数据")
    
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
            cursor.execute(insert_query, inert_values)
            connection.commit()  # 提交事务
        except Error as e:
            logger.error(f"数据库soccer_bet连接错误: {e}")
        logger.debug("数据插入soccer_bet成功")
    if connection.is_connected():
        cursor.close()
        connection.close()

    return True






# 获取余额
def getMyBetHistoryList(page=1,page_size=10):
    try:
        # 设置请求的URL
        url = f'{domain}/v1/order/new/bet/list'
        logger.debug(f"请求URL: {url}")
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
        logger.debug(f"请求响应: {response.status_code} {response.text[:200]}")
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            if reponse_json['code'] == 14010:
                logger.debug("token失效")
                return None
            
        return reponse_json
    except Exception as e:
        logger.error(f"getMyBetHistoryList异常: {e}")
        return None



def saveMyBetHistoryList(domain_cookie2=None,limit_page=5,page=1,page_size=10):
    update_global_vars(domain_cookie2)
    logger.debug(f"limit_page={limit_page}, page={page}, page_size={page_size}")
    while True:
        logger.debug(f"获取第{page}页数据")
        time.sleep(2)
        if limit_page<page:
            logger.debug("获取数据结束了，退出")
            break
        
        # 睡眠1秒，防止频繁请求
        page_data=getMyBetHistoryList(page,page_size)
        if page_data is None:
            logger.debug("获取数据失败，退出")
            break
        
        if page_data['code']!= 0:
            logger.debug("获取数据失败，退出")
            break
        
        if 'data' not in page_data or len(page_data['data']['records'])==0 :
            logger.debug("没有数据了，退出")
            break
        
        
        for item in page_data['data']['records']:
            try:
                # logger.debug(item)
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
                # logger.debug(bet_history_data)
                insert_if_not_exists(item['id'], item['ops'][0]['mid'], bet_history_data)
            except Exception as e:
                logger.error("解析数据失败")
                logger.error(f"{e}")


        page+=1
    logger.debug("获取数据结束,开始更新历史数据")
    update_cr_bettime()



def bet_history_victory(odds_amount,m_odds,odds_amount_result):
    logger.debug(f"odds_amount={odds_amount}, m_odds={m_odds}, odds_amount_result={odds_amount_result}")
    if odds_amount_result > 0 and odds_amount_result > odds_amount*(m_odds-1)*0.9:
        return "胜"
    elif odds_amount_result > 0 and odds_amount_result < odds_amount*(m_odds-1)*0.9:
        return "胜一半"
    elif odds_amount_result < 0 and odds_amount == -odds_amount_result:
        return "负"
    elif odds_amount_result < 0 and -odds_amount_result == odds_amount*0.5:
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
                logger.debug("开始插入")
                insert_query = "INSERT INTO `csgo`.`soccer_bet_history`(`bet_id`, `soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type`, `m_type_value`, `m_odds`, `goal_home`, `goal_guest`, `odds_amount`, `goal_home_result`, `goal_guest_result`, `odds_amount_result`, `bet_time`, `start_time`, `create_time`, `result_flag`,`bet_time_day`) VALUES\
                (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s,%s)"
                cursor.execute(insert_query, insert_data)
                conn.commit()
            else:
                logger.debug("数据已存在，未进行插入操作")
            


    except Error as e:
       logger.error(f"数据库 soccer_bet_history 连接错误: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

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
            cursor.execute("select m_type_value from soccer_analysis_start_new where c_time<80 and soccer_id ="+str(soccer_id) + " limit 1")
            row = cursor.fetchone()
            if row is not None :
                return row[0]
            else:
                logger.debug("初盘数据不存在")
    except Error as e:
       logger.error(f"数据库 soccer_analysis_start_new 连接错误: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

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
            logger.debug("更新soccer_bet_history成功")
            conn.commit()
    except Error as e:
       logger.error(f"数据库 soccer_bet_history 连接错误: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return True



def extract_numbers(s):
    # 使用正则表达式提取数字
    numbers = re.findall(r'\d+', s)
    # 将提取的数字转为集合，确保唯一性
    return numbers



import requests

def get_all_match_result_page(domain_cookie2, begin_time, end_time, match_type=2, order_by=0, language_type="CMN", sport_id="1", page_size=50):
    update_global_vars(domain_cookie2)
    """
    递归查询 https://a.a5y8i.com/v1/match/matchResultPage 接口，获取所有分页数据
    :param domain: 域名，如 'https://a.a5y8i.com'
    :param authorization: 授权token
    :param begin_time: 开始时间（时间戳，毫秒）
    :param end_time: 结束时间（时间戳，毫秒）
    :param match_type: 比赛类型，默认2
    :param order_by: 排序，默认0
    :param language_type: 语言类型，默认"CMN"
    :param sport_id: 体育类型，默认"1"
    :param page_size: 每页数量，默认50
    :return: 所有records的列表
    """
    url = f"{domain}/v1/match/matchResultPage"
    logger.debug(f"请求URL: {url}")
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': authorization,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://c.e70cz.com',
        'Referer': 'https://c.e70cz.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    all_records = []
    current = 1

    while True:
        payload = {
            "sportId": sport_id,
            "beginTime": begin_time,
            "endTime": end_time,
            "languageType": language_type,
            "current": current,
            "size": page_size,
            "matchType": match_type,
            "orderBy": order_by
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logger.error(f"请求第{current}页数据失败: {e}")
            break

        if not data.get("success", False) or "data" not in data:
            logger.error(f"接口返回异常: {data}")
            break

        page_data = data["data"]
        records = page_data.get("records", [])

        total = page_data.get("total", 0)
        size = page_data.get("size", page_size)
        cur = page_data.get("current", current)
        # INSERT INTO `csgo`.`soccer_analysis_end_new`(`id`, `soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type_value`, `goal_home_first`, `goal_guest_first`, `goal_home_second`, `goal_guest_second`, `goal_home`, `goal_guest`, `start_time`, `create_time`, `race_id`)
        # 连接到 MySQL 数据库
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
            
        if connection.is_connected():
            cursor = connection.cursor()
            for record in records:
                # 按照要求提取数据，组装为插入数据库的字典或元组
                try:
                    
                    soccer_id = record.get('id', None)
                    lg = record.get('lg', {})
                    race_name = lg.get('na', '')
                    race_id = lg.get('id', '')
                    ts = record.get('ts', [])
                    team_home = ts[0].get('na', '') if len(ts) > 0 else ''
                    team_guest = ts[1].get('na', '') if len(ts) > 1 else ''
                    team_cr = ''  # 未指定来源，置空
                    c_time = 90
                    nsg = record.get('nsg', [])
                    # 进球相关字段，注意判空
                    # 优化进球相关字段提取，避免变量未定义和重复遍历
                    goal_home = goal_guest = goal_home_first = goal_guest_first = goal_home_second = goal_guest_second = None
                    for nsg_item in nsg:
                        if nsg_item.get('tyg') != 5 or 'pe' not in nsg_item or 'sc' not in nsg_item:
                            continue
                        if nsg_item['pe'] == 1001:
                            goal_home, goal_guest = nsg_item['sc'][0], nsg_item['sc'][1]
                        elif nsg_item['pe'] == 1002:
                            goal_home_first, goal_guest_first = nsg_item['sc'][0], nsg_item['sc'][1]
                        elif nsg_item['pe'] == 1003:
                            goal_home_second, goal_guest_second = nsg_item['sc'][0], nsg_item['sc'][1]

                    m_type_value = None
                    if goal_home is not None and goal_guest is not None:
                        m_type_value = goal_home + goal_guest

                    # 开始时间
                    bt = record.get('bt', None)
                    if bt is not None:
                        start_time = datetime.datetime.fromtimestamp(bt/1000).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        start_time = None
                    # 当前时间
                    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # 修复：原代码中查询soccer_analysis_start_new时用到了未定义的values变量，应该用当前record的soccer_id
                    # 组装插入数据
                    row = (
                        soccer_id,
                        race_name,
                        team_home,
                        team_guest,
                        team_cr,
                        c_time,
                        m_type_value,
                        goal_home_first,
                        goal_guest_first,
                        goal_home_second,
                        goal_guest_second,
                        goal_home,
                        goal_guest,
                        start_time,
                        create_time,
                        race_id
                    )
                    # 将组装好的 row 插入到 csgo.soccer_analysis_end_new 表
                    insert_sql = """
                        INSERT INTO `csgo`.`soccer_analysis_end_new`
                        (`soccer_id`, `race_name`, `team_home`, `team_guest`, `team_cr`, `c_time`, `m_type_value`, 
                        `goal_home_first`, `goal_guest_first`, `goal_home_second`, `goal_guest_second`, 
                        `goal_home`, `goal_guest`, `start_time`, `create_time`, `race_id`)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """


                    logger.debug("soccer_analysis_end_new删除后再次插入")
                    # 刪除这一条数据
                    delete_sql = "DELETE FROM `csgo`.`soccer_analysis_end_new` WHERE `soccer_id` = %s"
                    cursor.execute(delete_sql, (soccer_id,))
                    
                    # 覆盖插入
                    cursor.execute(insert_sql, row)
                    connection.commit()
                    logger.debug("插入soccer_analysis_end_new成功")

                except Exception as e:
                    logger.error(f"插入soccer_analysis_end_new出错: {e}")
                except Exception as e:
                    logger.error(f"解析record出错: {e}")
                # logger.debug(record)
            
        logger.debug(f"已获取第{cur}页，共{len(records)}条，累计{len(all_records)}/{total}")

        # 判断是否还有下一页
        if cur * size >= total or len(records) == 0:
            break
        current += 1
        # 暂停1秒，防止请求过快
        time.sleep(1)



    

    
if __name__ == '__main__':
        # 全局变量
    domain_cookie = {
        "domain": "https://a.a5y8i.com",
        "authauthorization": "tt_zT2e8C2LF9WLSZ375DsKzFZptfVGOeS9.cfb7eec82c9d9e487697e045e821654e"
    }

    update_global_vars(domain_cookie)
    # # bet
    # values={}
    # values['soccer_id']= 3675319
    # values['m_type_value']=2.75
    # values['c_time']=7
    # bet_amount=20
    # save_bet_data(values,type='大',bet_amount=bet_amount,domain_cookie=domain_cookie)
# 示例字符串
    # saveMyBetHistoryList(limit_page=5,page=1,page_size=10)
    # notify_email("测试邮件")
    # get_soccer_data_start(2846449)
    get_all_match_result_page(domain_cookie,1757520000000, 1757951999999, match_type=2, order_by=0, language_type="CMN", sport_id="1", page_size=50)

