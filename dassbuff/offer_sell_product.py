import json
from datetime import datetime
import requests
import config


# 获取当前的出售单
def get_my_offer_List(title="",limit=50):
    try:
        # 设置请求的URL
        url = 'https://api.dmarket.com/exchange/v1/user/offers'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': config.authorization,
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'jkkat': '2420eb2e',
            'language': 'ZH',
            'origin': 'https://dmarket.com',
            'payment-session-id': '40507796-c78e-470e-9ded-1a90e49c239f',
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
            "side":"user",
            "orderBy":"updated",
            "orderDir":"desc",
            "title":title,
            "priceFrom":"0",
            "priceTo":"0",
            "treeFilters":"",
            "gameId":"a8db",
            "myFavorites":"false",
            "cursor":"",
            "limit":limit,
            "currency":"USD",
            "platform":"browser"
        }

        # 发送POST请求
        response = requests.get(url, params=params,headers=headers)
        reponse_json = json.loads(response.text)
        offers=reponse_json['objects']

        return offers
    except Exception as e:
        print(e)
        return None



# 获取当前的库存
def get_my_invert_List(title="",limit=50,treeFilters=""):
    try:
        # 设置请求的URL
        url = 'https://api.dmarket.com/exchange/v1/user/items'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': config.authorization,
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'jkkat': '2420eb2e',
            'language': 'ZH',
            'origin': 'https://dmarket.com',
            'payment-session-id': '40507796-c78e-470e-9ded-1a90e49c239f',
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
            "side":"user",
            "orderBy":"updated",
            "orderDir":"desc",
            "title":title,
            "priceFrom":"0",
            "priceTo":"0",
            "treeFilters":treeFilters,
            "gameId":"a8db",
            "myFavorites":"false",
            "statuses":"",
            "cursor":"",
            "limit":limit,
            "currency":"USD",
            "platform":"browser"
        }

        # 发送POST请求
        response = requests.get(url, params=params,headers=headers)
        # print(response.text)
        reponse_json = json.loads(response.text)
        offers=reponse_json['objects']
        
        return offers
    except Exception as e:
        print(e)
        return None



def add_my_invert_List(items=[]):
    try:
        # 设置请求的URL
        url = 'https://api.dmarket.com/exchange/v1/selection/item'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': config.authorization,
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'jkkat': '2420eb2e',
            'language': 'ZH',
            'origin': 'https://dmarket.com',
            'payment-session-id': '40507796-c78e-470e-9ded-1a90e49c239f',
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
            "items":items,
            "gameId":"a8db"
        }

        # 发送POST请求
        response = requests.patch(url, headers=headers,json=params)
        print(response.text)
        
    except Exception as e:
        print(e)
        return None
    



def add_my_sell_List(items=[]):
    try:
        # 设置请求的URL
        url = 'https://api.dmarket.com/exchange/v1/selection/offer'
        # 设置请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': config.authorization,
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'jkkat': '2420eb2e',
            'language': 'ZH',
            'origin': 'https://dmarket.com',
            'payment-session-id': '40507796-c78e-470e-9ded-1a90e49c239f',
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
            "items":items,
            "gameId":"a8db"
        }

        # 发送POST请求
        response = requests.patch(url, headers=headers,json=params)
        print(response.text)
        
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    # # dmarket能提现到steam的物品
    title=""
    treeFilters="itemLocation[]=true,tradeLockTo[]=0"


    # steam库存添加售卖
    # title=""
    # treeFilters="itemLocation[]=false"

    # my_invert_list=get_my_invert_List(title=title,limit=100,treeFilters=treeFilters)
    # if my_invert_list is None or len(my_invert_list) == 0: 
    #     print("获取当前的采购饰品情况失败")
    #     exit()
    # add_list=[]
    # for item in my_invert_list:
    #     print(item['item'])
    #     add_list.append(item['itemId'])

    
    # user_input = input("准备开始添加到处理清单数量"+str(len(add_list))+"，请输入Y确认：\n")
    # # 开始添加到出售清单
    # if user_input == "Y":
    #     print("开始添加")
    #     add_my_invert_List(items=add_list)
    #     print("开始添加结束")
    #     exit()


    # 获取当前的出售单
    my_invert_list=get_my_offer_List(title="USP-S | Ticket to Hell (Minimal Wear)",limit=100)
    print(my_invert_list)
    if my_invert_list is None or len(my_invert_list) == 0: 
        print("获取当前的出售单情况失败")
        
    add_list=[]
    for item in my_invert_list:
        print(item['item'])
        add_list.append(item['itemId'])
    
    user_input = input("准备开始添加到出售清单数量"+str(len(add_list))+"，请输入Y确认：\n")
    # 开始添加到出售清单
    if user_input == "Y":
        print("开始添加") 
        add_my_sell_List(items=add_list)
        print("开始添加结束")
        exit()
