import requests
import json
import datetime
import math
import config

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
        print(response)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            soccer=reponse_json['data']
            # 过滤平均销量大于30的列表
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
        print(item)
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
        print(response)
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
            "singleBetList": singleBetList,
            "currencyId": 1,

        }
        # 发送POST请求
        response = requests.post(url,headers=headers,json=params)
        print(response)
        if response.status_code == 200:
            reponse_json = json.loads(response.text)
            print(reponse_json)
            if reponse_json['code'] == 0:
                detail=reponse_json['data']
                print(deatail)
                return detail
            else:
                print(reponse_json['message'])
        return None
    except Exception as e:
        print(e)
        return None



# 下注
def getStakeOrderStatus(authorization,orderIds):
    if len(orderIds)==0:
        return False
    
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
            if reponse_json['code'] == 0:
                return True

        return False
    except Exception as e:
        print(e)
        return False




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
            balance=reponse_json['data']
            # 过滤平均销量大于30的列表
            return balance
        return None
    except Exception as e:
        print(e)
        return None


def getMatchList(deatail,balance,bet_amount=10):
    # if balance is None or balance['bl']<bet_amount:
    #     print("余额不足,当前余额是："+str(balance['bl']))
    #     return None

    for mg in deatail['mg']:
        if 1007 == mg['mty'] and 1001 == mg['pe'] :
            marketId = mg['mks'][0]['id']
            for t_type in mg['mks'][0]['op']:
                if '大' in t_type['na']:
                    current_m_typy_value=0
                    if '/' in t_type['li']:
                        current_m_typy_value =  (eval(t_type['li'].split('/')[0])+eval(t_type['li'].split('/')[1]))/2
                    else:
                        current_m_typy_value = eval(t_type['li'])

                    odds =  t_type['bod']
                    oddsFormat =  t_type['odt']
                    optionType =  t_type['ty']

                    break
                elif '小' in t_type['na']:
                    current_s_typy_value=0
                    if '/' in t_type['li']:
                        current_s_typy_value =  (eval(t_type['li'].split('/')[0])+eval(t_type['li'].split('/')[1]))/2
                    else:
                        current_s_typy_value = eval(t_type['li'])


                    odds =  t_type['bod']
                    oddsFormat =  t_type['odt']
                    optionType =  t_type['ty']
                    break

    singleBetList=[]
    single={
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


    
if __name__ == '__main__':
    # soccer = getFbSoccerData()
    # tarnMySoccerData(soccer)
    #比赛详情
    # deatail = getMatchDetail(2570855,1)
    # print(deatail)
    
    # # 余额
    # balance=getBalance(config.itone_authorization)
    # # 单注下注列表
    # singleBetList=getMatchList(deatail,balance,bet_amount=13.26)
    # print(singleBetList)
    # # 下注
    # singlePassDetail=singlePass(config.itone_authorization,singleBetList)
    # orderIds=[]
    # if singlePassDetail is not None:
    #     for item in singlePassDetail:
    #         orderIds.append(item['id'])
    # print(deatail)

    orderIds=["1329802262804964140"]
    orderStatus=getStakeOrderStatus(config.itone_authorization,orderIds)
