
import re


def parse_curl_to_params(curl_str):
    """
    解析curl命令字符串，返回包含domain、authauthorization、cookies的对象
    :param curl_str: 选中的curl命令字符串
    :return: dict，包含domain, authauthorization, cookies
    """

    # 1. 解析domain
    domain_match = re.search(r"curl\s+'(https?://[^/]+)", curl_str)
    domain = domain_match.group(1) if domain_match else ""

    # 2. 解析authorization
    auth_match = re.search(r"-H\s+'authorization:\s*([^']+)'", curl_str)
    authauthorization = auth_match.group(1) if auth_match else ""

    # 3. 解析cookies
    cookies_match = re.search(r"-b\s+'([^']+)'", curl_str)
    cookies_str = cookies_match.group(1) if cookies_match else ""
    cookies = {}
    if cookies_str:
        for item in cookies_str.split(";"):
            if "=" in item:
                k, v = item.strip().split("=", 1)
                cookies[k.strip()] = v.strip()

    return {
        "domain": domain,
        "authauthorization": authauthorization,
        "cookies": cookies
    }

# 示例用法
curl_str = """curl 'https://www.lt100.xyz/v2/asset/bonus/longtermbonusdetail' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'apm-request-id: e413a6cb054a3913' \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJubyI6IjQ5OTE3OTY2M2FlOGU4YTRjZGYyODBjOWE3ZGQxOTAyIiwidmUiOiIiLCJsYSI6InpoLWNuIiwidGkiOiIxIiwidWEiOiIycUFPYVFNUjVnSDVYSXdrQmZJa1orUkg4V21kWmJ3Ym5BSzBmS21LYWM2TGhPN24xZW9FazJwSWZPUDZ1QTk4TGFiL1NsWXpTRXRuaDZLejZTMlkzOStqYlhyendlM0pWNFZ0ZndFVjdHUDgvOUM3dVZteHJyaHd6elBHUEY1U0djSTdHKzV2Rnlyb2Y3enRucUN6dlE9PSIsImlhdCI6IjE3NTc0NzYzNDEiLCJpZCI6Ijg4Njk4NCIsIm5hIjoic2h1YWkxIiwidHYiOiI2Mzg5MzA3MzE0MTcwODY4NjAiLCJyZSI6IjE3NTgwODExNDEiLCJuYmYiOjE3NTc0NzYzNDEsImV4cCI6MTc1NzUwNTE0MSwiaXNzIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIn0.wI79twYJc9St_VWTGjSpy_lyAr8cz54DubnZKUmwz4k' \
  -H 'baggage: sentry-environment=prod,sentry-release=prod.20250905.1,sentry-public_key=dff2ed5deeb9e10164ae35ec4a082539,sentry-trace_id=0643a829933b492f926fd81b357ca19e,sentry-sample_rate=0.2,sentry-transaction=%2F%3AlanguageCode%2Fvoucher%2Fcoupon%2F,sentry-sampled=false' \
  -H 'cache-control: no-store,no-cache' \
  -H 'content-type: application/json;charset=utf-8' \
  -b '_ga=GA1.1.714685064.1756178500; _hjSessionUser_3823075=eyJpZCI6ImJlMjFlZGJlLTRjZTItNThmNC1hYTc2LWM4YjgyOTg0MWMwOCIsImNyZWF0ZWQiOjE3NTYxNzg0OTkxNjMsImV4aXN0aW5nIjp0cnVlfQ==; _hjHasCachedUserAttributes=true; _vid_t=vkrzPg1Oss5U0ZGcn9oKAIUpCA0fZiX+aG1rsr8fenpO6W80xa2xWMO1FcDJ1x4Mrb/7YX5kTZke2w==; _hjSession_3823075=eyJpZCI6ImRlMDk2NmQ1LTBjZGYtNDQxNi1hZDY1LTE4YzQ5ZGYyYTFkMyIsImMiOjE3NTc0NzYyNzE3NjgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; JSESSIONID=85938CF1B39672C45838B98C2DD6B2BF; _ga_2RY83PV4BH=GS2.1.s1757476271$o61$g1$t1757476360$j39$l0$h1775096820; _ga_DP31FC7D8Z=GS2.1.s1757476271$o61$g1$t1757476360$j41$l0$h0' \
  -H 'fp-visitor-id: iG6iZ0t1N37lsdvkNXRp' \
  -H 'lang: zh-cn' \
  -H 'ngsw-bypass: true' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.lt100.xyz/zh-cn/voucher/coupon' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sentry-trace: 0643a829933b492f926fd81b357ca19e-9b15c76766286922-0' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'"""



def parse_curl_to_params_bet(curl_str):
    """
    解析a5y8i.com专用curl字符串，返回domain和authauthorization
    :param curl_str: curl命令字符串
    :return: dict，包含domain和authauthorization
    """
    # 1. 解析domain
    domain_match = re.search(r"curl\s+'(https?://[^/]+)", curl_str)
    domain = domain_match.group(1) if domain_match else ""

    # 2. 解析Authorization（注意A大写）
    auth_match = re.search(r"-H\s+'Authorization:\s*([^']+)'", curl_str)
    authauthorization = auth_match.group(1) if auth_match else ""

    return {
        "domain": domain,
        "authauthorization": authauthorization
    }

# 示例用法
curl_str_a5y8i = """curl 'https://a.a5y8i.com/v1/match/getBannerMatchList' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Authorization: tt_Q7bFpw0b7R8i4GYjOrdn3R4q0HtNuKZF.c11b0753b61d9fd90f247f44f4e99775' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Origin: https://c.e70cz.com' \
  -H 'Referer: https://c.e70cz.com/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  --data-raw '{"languageType":"CMN","platform":1}'"""

# 测试
# params = parse_curl_to_params_a5y8i(curl_str_a5y8i)
# print(params)




# params = parse_curl_to_params(curl_str)
# print('domain:', params['domain'], '\n')
# print('authauthorization:', params['authauthorization'], '\n')
# print('cookies:', params['cookies'])

if __name__ == '__main__':
    # 示例用法
    print("启动了")
    json=parse_curl_to_params_bet(curl_str_a5y8i)
    print(json)