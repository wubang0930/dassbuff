import json
import requests
import log_utils
import datetime
import time


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

def get_long_term_bonus_detail():

    url = f'{domain}/v2/asset/bonus/longtermbonusdetail'
    print("请求地址：", url)
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apm-request-id': 'f282f52c2e4d10ac',  # 变化值
        'authorization': authorization,
        'baggage': 'sentry-environment=prod,sentry-release=prod.20250905.1,sentry-public_key=dff2ed5deeb9e10164ae35ec4a082539,sentry-trace_id=3df2c9992a524054bcbfb8f9b3c918d5,sentry-sample_rate=0.2,sentry-transaction=%2F%3AlanguageCode%2Fvoucher%2Fcoupon%2F,sentry-sampled=false',
        'cache-control': 'no-store,no-cache',
        'content-type': 'application/json;charset=utf-8',
        'fp-visitor-id': '',  # 变化值
        'lang': 'zh-cn',
        'ngsw-bypass': 'true',
        'priority': 'u=1, i',
        'referer': f'{domain}/zh-cn/voucher/coupon',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',  # 变化值
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '3df2c9992a524054bcbfb8f9b3c918d5-9eb6885c2e444160-0',  # 变化值
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'  # 变化值
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        print("接口返回：", response.text)
        return response.json()
    except Exception as e:
        print("请求失败：", e)
        return None

    
    
def receive_backwater_bonus_action(result):


    if not result or "data" not in result or "list" not in result["data"]:
        print("未获取到有效的长期彩金数据")
        return

    bonus_list = result["data"]["list"]

    for item in bonus_list:
        is_accumulate = item.get("isAccumulate", False)
        amount = item.get("amount", 0)
        if is_accumulate and amount > 0:
            print(f"检测到可累积彩金，ID: {item.get('id')}, 标题: {item.get('title')}, 金额: {amount}")
            receive_backwater_bonus(item.get('id'))
            # 这里可以进行下一步操作，比如调用领取接口等
            # do_next_operation(item)
        else:
            print(f"跳过彩金，ID: {item.get('id')}, isAccumulate: {is_accumulate}, amount: {amount}")




def receive_backwater_bonus(bonus_id):
    """
    领取返水彩金接口
    :param bonus_id: 返水彩金ID
    :return: 返回接口响应的json数据
    """

    url = f'{domain}/v2/asset/bonus/receivebackwater?bonusId={bonus_id}'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apm-request-id': '77dc36eeff6a1692',
        'authorization': authorization,
        'baggage': 'sentry-environment=prod,sentry-release=prod.20250905.1,sentry-public_key=dff2ed5deeb9e10164ae35ec4a082539,sentry-trace_id=490712c7449f4b53a83abbddb406dae4',
        'cache-control': 'no-store,no-cache',
        'content-type': 'application/json;charset=utf-8',
        'fp-visitor-id': '',
        'lang': 'zh-cn',
        'ngsw-bypass': 'true',
        'priority': 'u=1, i',
        'referer': f'{domain}/zh-cn/voucher/coupon',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '490712c7449f4b53a83abbddb406dae4-88e0fb801355f0d3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        print("领取返水彩金接口返回：", response.text)
        return response.json()
    except Exception as e:
        print("领取返水彩金请求失败：", e)
        return None


def get_user_balance():
    """
    查询用户钱包余额接口
    :return: 返回接口响应的json数据
    """

    url = f"{domain}/v1/asset/wallet/userbalance"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apm-request-id': '1605b3678edf1fe1',
        'authorization': authorization,
        'baggage': 'sentry-environment=prod,sentry-release=prod.20250905.1,sentry-public_key=dff2ed5deeb9e10164ae35ec4a082539,sentry-trace_id=490712c7449f4b53a83abbddb406dae4',
        'cache-control': 'no-store,no-cache',
        'content-type': 'application/json;charset=utf-8',
        'fp-visitor-id': '',
        'lang': 'zh-cn',
        'ngsw-bypass': 'true',
        'priority': 'u=1, i',
        'referer': f'{domain}/zh-cn/voucher/coupon',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '490712c7449f4b53a83abbddb406dae4-88e0fb801355f0d3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
    }

 

    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        print("用户余额接口返回：", response.text)
        jsondata = response.json()
        usdt_balance = None
        cny_balance = None
        if jsondata.get("success") and isinstance(jsondata.get("data"), list):
            for wallet in jsondata["data"]:
                if wallet.get("currency") == "USDT":
                    usdt_balance = wallet.get("balance")
                if wallet.get("currency") == "CNY":
                    cny_balance = wallet.get("balance")
        if usdt_balance is not None:
            try:
                usdt_balance = round(float(usdt_balance), 2)
            except Exception:
                pass
        if cny_balance is not None:
            try:
                cny_balance = round(float(cny_balance), 2)
            except Exception:
                pass
        print(f"USDT余额: {usdt_balance}, CNY余额: {cny_balance}")
        
    except Exception as e:
        print("用户余额请求失败：", e)
        return None


def get_vip_bonus_detail():


    """
    获取未领取的vip奖金详情
    :param auth: 授权token字符串（Bearer ...）
    :return: 返回接口返回的json数据，若失败返回None
    """
    url = f"{domain}/v2/asset/bonus/bonusdetail?pageIndex=1&pageSize=6&status=Unclaimed&ascSort=false"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apm-request-id': 'c41e769d430d2724',
        'authorization': authorization,
        'baggage': 'sentry-environment=prod,sentry-release=prod.20250905.1,sentry-public_key=dff2ed5deeb9e10164ae35ec4a082539,sentry-trace_id=490712c7449f4b53a83abbddb406dae4',
        'cache-control': 'no-store,no-cache',
        'content-type': 'application/json;charset=utf-8',
        'fp-visitor-id': '',
        'lang': 'zh-cn',
        'ngsw-bypass': 'true',
        'priority': 'u=1, i',
        'referer': f'{domain}/zh-cn/voucher/coupon',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '490712c7449f4b53a83abbddb406dae4-88e0fb801355f0d3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        print("vip奖金详情接口返回：", response.text)
        jsondata = response.json()
        return jsondata
    except Exception as e:
        print("vip奖金详情请求失败：", e)
        return None


def receive_vip_bonus(bonus_id, collected_currency="CNY"):
    """
    领取返水彩金
    :param bonus_id: 返水彩金ID
    :param collected_currency: 领取币种，默认为CNY
    :return: 返回接口返回的json数据，若失败返回None
    """
    url = f"{domain}/v2/asset/bonus/receivebackwater?bonusId={bonus_id}&collectedCurrency={collected_currency}"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apm-request-id': '61080989bc8f04b9',
        'authorization': authorization,
        'baggage': 'sentry-environment=prod,sentry-release=prod.20250905.1,sentry-public_key=dff2ed5deeb9e10164ae35ec4a082539,sentry-trace_id=490712c7449f4b53a83abbddb406dae4',
        'cache-control': 'no-store,no-cache',
        'content-type': 'application/json;charset=utf-8',
        'fp-visitor-id': '',
        'lang': 'zh-cn',
        'ngsw-bypass': 'true',
        'priority': 'u=1, i',
        'referer': f'{domain}/zh-cn/voucher/coupon',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '490712c7449f4b53a83abbddb406dae4-88e0fb801355f0d3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        print("领取vip彩金接口返回：", response.text)
        return response.json()
    except Exception as e:
        print("领取vip彩金请求失败：", e)
        return None

    
def receive_vip_bonus_action(result):
    print("领取vip奖励开始")

    if not result or "data" not in result or "list" not in result["data"] or not result["data"]["list"]:
        print("未获取到有效的vip彩金数据")
        return
    vip_list = result["data"]["list"]
    for item in vip_list:
        print(f"检测到可累积彩金，ID: {item.get('id')}, 标题: {item.get('title')}, 金额: {item.get('amount')}")
        receive_vip_bonus(item.get('id'))



def receive_all_bonus_action(domain_cookie):
    # 更新全局变量
    update_global_vars(domain_cookie)
    
    # 获取余额
    get_user_balance()
    # 获取返水彩金
    result=get_long_term_bonus_detail()
    # 领取返水彩金
    receive_backwater_bonus_action(result)
    # 获取余额
    get_user_balance()
    # 获取VIP奖励详情
    vip_result = get_vip_bonus_detail()
    # 获取VIP奖励
    receive_vip_bonus_action(vip_result)


# 示例调用
# process_long_term_bonus(authauthorization)
if __name__ == '__main__':
    start_time=int(time.time())
    log_file_name = f"main-{datetime.now().strftime('%Y%m%d')}"
    log_utils.init_logger(log_file_name)
    print("类开始启动")

    # domain = 'https://www.ltkavor.site'
    # authauthorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJubyI6ImM3MDAyMTE2MzI0YmI5ODNlOGUwNDM1NWFjMGVkNWNkIiwidmUiOiIiLCJsYSI6InpoLWNuIiwidGkiOiIxIiwidWEiOiIycUFPYVFNUjVnSDVYSXdrQmZJa1orUkg4V21kWmJ3Ym5BSzBmS21LYWM2TGhPN24xZW9FazJwSWZPUDZ1QTk4TGFiL1NsWXpTRXRuaDZLejZTMlkzOStqYlhyendlM0pWNFZ0ZndFVjdHTzBKK01wTFlETnpuUGRXVk0vWEpNcCtOY3pXYTJ5ZXAvSFk0dHF5R2tHQ0E9PSIsImlhdCI6IjE3NTc0Njg5NzUiLCJpZCI6Ijg4Njk4NCIsIm5hIjoic2h1YWkxIiwidHYiOiI2Mzg5MzA2NTc3NTQ3MjE1NTkiLCJyZSI6IjE3NjAwODk3NzUiLCJuYmYiOjE3NTc0Njg5NzUsImV4cCI6MTc1NzQ5Nzc3NSwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIn0.VxMN-dtFHx1vIx4xLpHn0CkLwupQEZb_3paCYNrSVLI"
    # cookies = {
    #     'visid_incap_3227610': 'HYsKdnQaRb2An9C/Gyo/stzYwGgAAAAAQUIPAAAAAADsrjEpYu75vp8RTBhJqQSI',
    #     'nlbi_3227610': 'oVNJGwe8wRZgRLspK7Qb8AAAAADVEbv/sqPC5Vs/cB3iVil0',
    #     'incap_ses_1510_3227610': 'yosrRzGqvny1aAuDNZn0FN7YwGgAAAAA358J9MYFmcIVi04XrZgUsw==',
    #     '_hjSessionUser_3823075': 'eyJpZCI6IjEyOGNlNTYyLWNmMjgtNTI5Yi1iNzQxLTgwZjJkNWViNmEwOSIsImNyZWF0ZWQiOjE3NTc0Njg5MDI1NjIsImV4aXN0aW5nIjp0cnVlfQ==',
    #     '_hjSession_3823075': 'eyJpZCI6IjUyNDkzYjU1LWUzNzAtNGU0My1iNDRjLTgwNDE4N2QwYTdiMyIsImMiOjE3NTc0Njg5MDI1NjMsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=',
    #     '_hjHasCachedUserAttributes': 'true',
    #     '_hjUserAttributesHash': '6b88065dfe6e9520eec28f8db1e7d9ce',
    #     'JSESSIONID': '60FA9437501CE282D072E73E708C248F'
    # }

    # domain_cookie = {
    #     'domain': domain,
    #     'authorization': authauthorization,
    #     'cookies': cookies
    # }

    # # 获取余额
    # receive_all_bonus_action(domain_cookie)