import requests

def get_user_balance():
    url = "https://www.ltkavor.site/v1/asset/wallet/userbalance"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'apm-request-id': '8be1a64ae0f6734a',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJubyI6ImM3MDAyMTE2MzI0YmI5ODNlOGUwNDM1NWFjMGVkNWNkIiwidmUiOiIiLCJsYSI6InpoLWNuIiwidGkiOiIxIiwidWEiOiIycUFPYVFNUjVnSDVYSXdrQmZJa1orUkg4V21kWmJ3Ym5BSzBmS21LYWM2TGhPN24xZW9FazJwSWZPUDZ1QTk4TGFiL1NsWXpTRXRuaDZLejZTMlkzOStqYlhyendlM0pWNFZ0ZndFVjdHTzBKK01wTFlETnpuUGRXVk0vWEpNcCtOY3pXYTJ5ZXAvSFk0dHF5R2tHQ0E9PSIsImlhdCI6IjE3NTc0ODYyMTYiLCJpZCI6Ijg4Njk4NCIsIm5hIjoic2h1YWkxIiwidHYiOiI2Mzg5MzA4MzAxNjg0MjA0MDMiLCJyZSI6IjE3NTgwOTEwMTYiLCJuYmYiOjE3NTc0ODYyMTYsImV4cCI6MTc1NzUxNTAxNiwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIn0.UcWqgHJvquUFAdEa-0PceiEgND7TuBjBqNEfVv7XsCM',
        'baggage': 'sentry-environment=prod,sentry-release=prod.20250905.1,sentry-public_key=dff2ed5deeb9e10164ae35ec4a082539,sentry-trace_id=65ffa5cb97e445bbabc109d785d45009',
        'cache-control': 'no-store,no-cache',
        'content-type': 'application/json;charset=utf-8',
        'fp-visitor-id': '',
        'lang': 'zh-cn',
        'ngsw-bypass': 'true',
        'priority': 'u=1, i',
        'referer': 'https://www.ltkavor.site/zh-cn/play/FBSport-1/All',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '65ffa5cb97e445bbabc109d785d45009-8adfca3dc177c196',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
    }
    cookies = {
        'visid_incap_3227610': 'HYsKdnQaRb2An9C/Gyo/stzYwGgAAAAAQUIPAAAAAADsrjEpYu75vp8RTBhJqQSI',
        '_hjSessionUser_3823075': 'eyJpZCI6IjEyOGNlNTYyLWNmMjgtNTI5Yi1iNzQxLTgwZjJkNWViNmEwOSIsImNyZWF0ZWQiOjE3NTc0Njg5MDI1NjIsImV4aXN0aW5nIjp0cnVlfQ==',
        '_ga': 'GA1.1.1192171690.1757472075',
        '_ga_DP31FC7D8Z': 'GS2.1.s1757472074$o1$g1$t1757472091$j43$l0$h0',
        '_ga_2RY83PV4BH': 'GS2.1.s1757472075$o1$g1$t1757472091$j44$l0$h406946278',
        'nlbi_3227610': 'hT9gYcIAZTmkmTEBK7Qb8AAAAABk1sOBOawoU4uqjs3/XYl+',
        'incap_ses_138_3227610': 'gHYnStjnQ0DYvGKDZUbqAQsawWgAAAAABupavgVIF0626ebFU+2LTg==',
        '_hjSession_3823075': 'eyJpZCI6IjBhZGNkMmU3LTdlOGMtNDhmYS04MTZhLTI5NjJkZDQzNDFjZSIsImMiOjE3NTc0ODU1OTY3MjUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        '_hjHasCachedUserAttributes': 'true',
        'incap_ses_1510_3227610': 'w8+3MnKa+GbqxmaDNZn0FB0cwWgAAAAA+0oXmEI4CTA/jdPvVU4Jaw==',
        'JSESSIONID': 'B84CB55DED8574FEFFB200C1DBB6E418'
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        print("用户余额接口返回：", response.text)
        return response.json()
    except Exception as e:
        print("请求失败：", e)
        return None

if __name__ == '__main__':
    get_user_balance()