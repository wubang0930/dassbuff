import requests
import gzip
import json
import certifi
import time
import config
import os
from datetime import datetime
import pandas as pd


def call_youpin_api(page,pageSize,authorization):
    url = "http://api.youpin898.com/api/youpin/bff/trade/sale/v1/sell/list"
    
    

    


        
    headers = {
        "Cache-Control": "no-cache",
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
        "Authorization": authorization,
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

    payload = {
        "Version": "5.29.0",
        "AppType": "3",
        "orderStatus": 340,
        "Platform": "ios",
        "keys": "",
        "pageIndex": page,
        "pageSize": pageSize,
        "SessionId": "913F9BD2-CD9A-40C0-A704-29A5A8F704D2"
    }


     # 压缩请求体
    compressed_data = gzip.compress(json.dumps(payload).encode("utf-8"))
    content_length = len(compressed_data)
    try:
       
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10,
            # verify=certifi.where()
            # verify="E:\\pythonFile\\python\\dassbuff\\venv\\Lib\\site-packages\\certifi\\cacert.pem"
        )

        response.raise_for_status()
        
        # 处理可能的gzip响应
            
        content = response.text  
        return {
            "status_code": response.status_code,
            "response": json.loads(content)
        }

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None






def create_my_sell_List_all(page=1,pageSize=20,limitPage=2,authorization=config.authorization):
    history_list=[]

    file_path=config.my_sell_current_file_two
    print("存储数据文件为："+str(file_path))

    if not os.path.exists(file_path):
        open(file_path,'w',encoding='utf-8')
    else:
        with open(file_path, 'r', encoding='utf-8') as my_buy_list_file:
            for cur_data in my_buy_list_file:
                json_item=json.loads(cur_data)
                history_list.append(json_item)

    with open(file_path, 'a+', encoding='utf-8') as my_buy_list_file:
        while True:
            print("获取第"+str(page)+"页数据"+"pageSize="+str(pageSize))
            if page>limitPage:
                print("获取数据达到要求")
                break

            time.sleep(1)
            result=call_youpin_api(page,pageSize,authorization)

            if result is None:
                print("获取数据有误")
                break

            if result['response']['data'] is None or len(result['response']['data']['orderList'])<1  :
                print("获取数据完成")
                break
            
            
            all_filter_order = []
            for order in result['response']['data']['orderList']:
                # print(order)
                for num in range(1, int(order['commodityNum'])+1):
                    filter_order = {}
                    filter_order['commodityHashName']=order['productDetail']['commodityHashName']
                    filter_order['commodityName']=order['productDetail']['commodityName']
                    filter_order['price']=order['productDetail']['price']/100
                    filter_order['orderId']=order['orderId']
                    filter_order['orderNo']=order['orderNo']
                    filter_order['createOrderTime']=order['createOrderTime']  #时间戳时间
                    #时间戳时间 转换为年月日时分秒
                    filter_order['createOrderTimeStr'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(filter_order['createOrderTime']/1000))
                    all_filter_order.append(filter_order)


                    old_flag=True
                    for history_item in history_list:
                        if history_item['orderId'] == filter_order['orderId']:
                            old_flag=False
                            print("跳过数据："+str(filter_order))
                            break

                    # 追加到最后一行
                    if old_flag:
                        print("追加数据："+str(filter_order))
                        my_buy_list_file.write(json.dumps(filter_order,ensure_ascii=False)+"\n")

            
            if limitPage<page:
                break
            page=page+1


def sycBuyAndSellList():
    buy_history_list=[]
    with open(config.my_buy_current_file_two, 'r', encoding='utf-8') as my_buy_list_file:
        for cur_data in my_buy_list_file:
            json_item=json.loads(cur_data)
            json_item['updatedAtStr'] = json_item['updatedAt']
            json_item['updatedAt'] = tranStrToDatetime(json_item['updatedAtStr'])
            buy_history_list.append(json_item)

    sell_history_list=[]
    with open(config.my_sell_current_file_two, 'r', encoding='utf-8') as my_sell_list_file:
        for cur_data in my_sell_list_file:
            json_item=json.loads(cur_data)
            sell_history_list.append(json_item)

    # buy_history_list 按照updatedAt 升序排序

    


    # buy_history_list 过滤action包含 Target 且 updatedAt 大于 1736265600000 的数组
   


    filter_buy_history_list=[]
    for buy_item in buy_history_list:
        if 'Target' in buy_item['action'] and buy_item['updatedAt'] > 1736265600000:
            filter_buy_history_list.append(buy_item)

    filter_sell_history_list=[]
    for sell_item in sell_history_list:
        if sell_item['createOrderTime'] > 1739116800000:
            sell_item['sell_flag'] = False
            filter_sell_history_list.append(sell_item)


    filter_buy_history_list.sort(key=lambda x:x['updatedAt'])
    filter_sell_history_list.sort(key=lambda x:x['createOrderTime'])

    print("过滤后买单数据："+str(len(filter_buy_history_list)))
    print("过滤后卖单数据："+str(len(filter_sell_history_list)))

    # 合并两个列表，开始买的时间为2025年1月3日以后   开始卖的时间为2025年2月10日以后，
    all_history_list=[]
    for buy_item in filter_buy_history_list:
        buy_item['sell_price'] = None
        buy_item['sell_date'] = None
        buy_item['sell_flag'] = False
        
        for sell_item in filter_sell_history_list:
            if sell_item['sell_flag']:
                continue

            if sell_item['commodityName'] == buy_item['cn_name']:
                buy_item['sell_price'] = sell_item['price']
                buy_item['sell_date'] = sell_item['createOrderTimeStr']
                buy_item['sell_flag'] = True
                sell_item['sell_flag'] = True
                break
                

        all_history_list.append(buy_item)

    # save_file_path=config.my_buy_sell_current_file_two
    # with open(save_file_path, 'w', encoding='utf-8') as save_file:
    #     for all_item in all_history_list:
    #         save_file.write(json.dumps(all_item,ensure_ascii=False)+"\n")

    print("开始导出数据")
    filename=config.my_buy_sell_current_file_two_excel+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"

    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(all_history_list)
    df.to_excel(filename, index=False)
    print("导出数据完成")




def tranStrToDatetime(str_time):
    # 指定日期格式
    date_format = "%Y-%m-%d %H:%M:%S"

    # 使用strptime方法将日期字符串转换为datetime对象
    date_obj = datetime.strptime(str_time, date_format)

    # 使用timestamp()方法将datetime对象转换为以秒为单位的时间戳
    timestamp = int(date_obj.timestamp()*1000)
    return timestamp





if __name__ == '__main__':
    # create_my_sell_List_all(page=10,pageSize=20,limitPage=60,authorization=config.my_sell_uu_user_token)
    start_time = time.time()
    sycBuyAndSellList()
    end_time = time.time()
    print("运行时间："+str(end_time-start_time))
    
