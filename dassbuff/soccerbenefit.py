import requests
from requests import auth


authauthorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJubyI6IjQ5OTE3OTY2M2FlOGU4YTRjZGYyODBjOWE3ZGQxOTAyIiwidmUiOiIiLCJsYSI6InpoLWNuIiwidGkiOiIxIiwidWEiOiIycUFPYVFNUjVnSDVYSXdrQmZJa1orUkg4V21kWmJ3Ym5BSzBmS21LYWM2TGhPN24xZW9FazJwSWZPUDZ1QTk4TGFiL1NsWXpTRXRuaDZLejZTMlkzOStqYlhyendlM0pWNFZ0ZndFVjdHUDgvOUM3dVZteHJyaHd6elBHUEY1U0djSTdHKzV2Rnlyb2Y3enRucUN6dlE9PSIsImlhdCI6IjE3NTc0MTI5NjQiLCJpZCI6Ijg4Njk4NCIsIm5hIjoic2h1YWkxIiwidHYiOiI2Mzg5MzAwOTc2NDgzNTUyNjAiLCJyZSI6IjE3NTgwMTc3NjQiLCJuYmYiOjE3NTc0MTI5NjQsImV4cCI6MTc1NzQ0MTc2NCwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIn0.-ikNKT0PCPDkYNVOh2nMAJxaC1_NvcKaefTTIM1MsyE"

def get_long_term_bonus_detail(authorization):
    url = 'https://www.lt100.xyz/v2/asset/bonus/longtermbonusdetail'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apm-request-id': '2650414d93336ca6',
        'authorization': authorization,
        'baggage': 'sentry-environment=prod,sentry-release=prod.20250905.1,sentry-public_key=dff2ed5deeb9e10164ae35ec4a082539,sentry-trace_id=00ed60a954f9425784458a5f3e8b8374,sentry-sample_rate=0.2,sentry-transaction=%2F%3AlanguageCode%2Fvoucher%2Fcoupon%2F,sentry-sampled=false',
        'cache-control': 'no-store,no-cache',
        'content-type': 'application/json;charset=utf-8',
        'fp-visitor-id': 'iG6iZ0t1N37lsdvkNXRp',
        'lang': 'zh-cn',
        'ngsw-bypass': 'true',
        'priority': 'u=1, i',
        'referer': 'https://www.lt100.xyz/zh-cn/voucher/coupon',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '00ed60a954f9425784458a5f3e8b8374-9be4fdd36773bcd0-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }
    # 如果需要带cookie，可以加上cookies参数
    cookies = {
        '_ga': 'GA1.1.714685064.1756178500',
        '_hjSessionUser_3823075': 'eyJpZCI6ImJlMjFlZGJlLTRjZTItNThmNC1hYTc2LWM4YjgyOTg0MWMwOCIsImNyZWF0ZWQiOjE3NTYxNzg0OTkxNjMsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjUserAttributesHash': '6b88065dfe6e9520eec28f8db1e7d9ce',
        '_hjHasCachedUserAttributes': 'true',
        '_hjSession_3823075': 'eyJpZCI6ImRkYzZkYmQ1LTExYTctNGQ3Yi1hNmQ2LTU1NWEyOWE2NmU4NCIsImMiOjE3NTc0MTExNzgxNTIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        '_vid_t': 'vkrzPg1Oss5U0ZGcn9oKAIUpCA0fZiX+aG1rsr8fenpO6W80xa2xWMO1FcDJ1x4Mrb/7YX5kTZke2w==',
        'JSESSIONID': 'A70118D1EF1F5A90DBADF02B6F1E4559',
        '_ga_DP31FC7D8Z': 'GS2.1.s1757411177$o59$g1$t1757413246$j60$l0$h0',
        '_ga_2RY83PV4BH': 'GS2.1.s1757411177$o59$g1$t1757413246$j60$l0$h1233480035'
    }
    try:
        response = requests.post(url, headers=headers, cookies=cookies)
        print("接口返回：", response.text)
        return response.json()
    except Exception as e:
        print("请求失败：", e)
        return None

# 示例调用
get_long_term_bonus_detail(authauthorization)          