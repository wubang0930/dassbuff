import requests
import gzip
import json
import certifi


def call_youpin_api():
    url = "http://api.youpin898.com/api/youpin/bff/trade/sale/v1/sell/list"
    
    

    payload = {
        "Version": "5.29.0",
        "AppType": "3",
        "orderStatus": 0,
        "Platform": "ios",
        "keys": "",
        "pageIndex": 1,
        "pageSize": 20,
        "SessionId": "913F9BD2-CD9A-40C0-A704-29A5A8F704D2"
    }

    data_str = json.dumps(payload)
    content_length = len(data_str)

    print(str(content_length))
    headers = {
        "Cache-Control": "no-cache",
        "Content-Length": str(content_length),
        "Host": "api.youpin898.com",
        "Cookie": "acw_tc=1a1c710a17416615477768507e0074bbf6ab642cc3a142061dc8602124cf82",
        "apptype": "3",
        "User-Agent": "",  
        "Content-Encoding": "gzip",
        "DeviceToken": "913F9BD2-CD9A-40C0-A704-29A5A8F704D2",
        "DeviceSysVersion": "15.5",
        "requesttag": "bab92394b7bfaa2a063126fc93296c44",
        "version": "5.29.0",
        "Gameid": "730",
        "uk": "5ClTf0C9HRUwILHMlmEvvKMwJ9Ihz95frWS1tgo8QknEYyUuhTf9dlj9W6G5Axp1K",
        "package-type": "uuyp",
        "platform": "ios",
        "Connection": "keep-alive",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NTM5OWY2MjAwNjg0ZDQwODY1NTJjNjg4Y2M0ZGYxMyIsIm5hbWVpZCI6IjY5MDQzOTQiLCJJZCI6IjY5MDQzOTQiLCJ1bmlxdWVfbmFtZSI6IjXliIbpkp_np5Llj5EiLCJOYW1lIjoiNeWIhumSn-enkuWPkSIsInZlcnNpb24iOiI2SWQiLCJuYmYiOjE3Mzk4ODIxOTksImV4cCI6MTc0NDA4Njk5OSwiaXNzIjoieW91cGluODk4LmNvbSIsImRldmljZUlkIjoiOTEzRjlCRDItQ0Q5QS00MEMwLUE3MDQtMjlBNUE4RjcwNEQyIiwiYXVkIjoidXNlciJ9.8rW7UmjOhxG9MTrkBAk4jJtMVHEGmBYeZDIoPWBDPHk",
        "tracestate": "bnro=iOS/15.5_iOS/8.15.100_NSURLSession",
        "api-version": "1.0",
        "Accept-Language": "zh-Hans-CN;q=1.0",
        "traceparent": "00-1b3c1e0e74af444496e66290135144a2-7ca972ed74919daa-01",
        "Content-Type": "application/json",
        "app-version": "5.29.0",
        "Accept-Encoding": "gzip",
        "currentTheme": "Light",
        "Accept": "*/*"
    }
    try:
        # 压缩请求体
        compressed_data = gzip.compress(json.dumps(payload).encode("utf-8"))
        
        response = requests.post(
            url,
            headers=headers,
            data=compressed_data,
            timeout=10,
            # verify=certifi.where()
            # verify="E:\\pythonFile\\python\\dassbuff\\venv\\Lib\\site-packages\\certifi\\cacert.pem"
        )

        response.raise_for_status()
        
        # 处理可能的gzip响应
        if response.headers.get("Content-Encoding") == "gzip":
            print("Decompressing gzip response...")
            content = gzip.decompress(response.content).decode("utf-8")
        else:
            content = response.text
            
        return {
            "status_code": response.status_code,
            "response": json.loads(content)
        }

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

# 调用示例
result = call_youpin_api()
if result:
    print(f"Status Code: {result['status_code']}")
    print("Response Data:", result['response'])