import requests
from lxml import etree
import json
import time

#--------------------------------需要录入的数据（每个list的长度要保证相同，且物品和磨损是对应的）---------------------------------------
ig_logger=['','']                         #输入igxe用户名和密码用于登录进行检索
abrution=[0.036,0.036,0.036,0.036,0.036,0.03,0.01]           #在多少磨损以下可以购买，溢价
ig_keys=['炎龙之焰','AWP暴怒野兽','FN57暴怒野兽','龙王','地狱烈焰','生化短吻鳄','复古圣杯']         #igxe搜索关键词，要配合ig_outlook
c5_numbers=['334737338','24262','553428006','22934','553427241','553455826','25592']               #c5搜索关键词，包含名称和outlook
#-----------------------------------------------------------------------------------------------------------------------------------------

########################################################################
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
#
#       Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
#   Everyone is permitted to copy and distribute verbatim or modified
#   copies of this license document, and changing it is allowed as long
#   as the name is changed.
#
#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#            0. You just DO WHAT THE FUCK YOU WANT TO.
########################################################################

start = time.time()                #计算程序运行时间

def c5_search(n):
    url = "https://www.c5game.com/csgo/item/index.html?item_id=" + c5_numbers[n] + "&type=S"
    ses=requests.session()
    source=ses.get(url)
    selector = etree.HTML(source.text)
    api=selector.xpath('//*[@id="sale"]/table/tbody/@data-url')[0]
    sale_url = "https://www.c5game.com/"+api
    # &callback=jQuery11110649451053797665_1518405192625&_=1518405192626
    c5_headers = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.c5game.com',
        'Referer':url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    #访问销售信息api
    sale = ses.get(sale_url, headers=c5_headers)
    decoded = json.loads(sale.text)
    item_list = decoded['body']['items']
    lowest=0
    for i in range(0, len(item_list)):
        item = item_list[i]
        if item['wear']:wear=float(item['wear'])
        else:wear=1
        price=item['price']
        if i==0:lowest=price+10
        print("c5:\t", item['wear'],"\t￥", item['price'],"\t",ig_keys[n])
        if wear<abrution[n] and price<lowest:print("positive")

print("匹配中...")
for i in range(0,len(c5_numbers)):
    c5_search(i)
end=time.time()
print("\n检索完成，花费时间:",end-start)
# os.system("pause")