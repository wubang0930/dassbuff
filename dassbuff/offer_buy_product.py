import json
from datetime import datetime

from nacl.bindings import crypto_sign
import requests
import config
import dassbuff.messagesend as messagesend

public_key = config.dmarket_public_key
secret_key = config.dmarket_secret_key

# change url to prod
rootApiUrl = "https://api.dmarket.com"
has_notified=False


def get_offer_from_market(limit=5,title="",orderBy='price'):

    treeFilters=""
    if 'StatTrak' not in title:
        treeFilters= 'category_0[]=not_stattrak_tm'
    elif 'StatTrak' in title:
        treeFilters= 'category_0[]=stattrak_tm'

    url=rootApiUrl + "/exchange/v1/market/items"
    params = {  
        "orderBy":orderBy,
        "orderDir":"asc",
        "title":title,
        "priceFrom":"0",
        "priceTo":"0",
        "treeFilters":treeFilters,
        "gameId":"a8db",
        "myFavorites":"false",
        "types":"dmarket",
        "cursor":"",
        "limit":str(limit),
        "currency":"USD",
        "platform":"browser"
    }

    market_response = requests.get(url, params=params)
    offers = json.loads(market_response.text)["objects"]
    return offers



# 创建采购单
def build_target_body_from_offer(price,amount,title,public_key,secret_key):
    if int(price) > 1000:
        print("价格超过10美元，不采购,当前价格为："+price)
        return
    
    body= {"targets": [
        {"amount": amount, "gameId": 'a8db', "price": {"amount": price, "currency": "USD"},
         "attributes": {"gameId": 'a8db',
                        # "categoryPath": offer["extra"]["categoryPath"],
                        "title": title,
                        "name": title,
                        # "image": offer["image"],
                        "ownerGets": {"amount": "1", "currency": "USD"}}}
    ]}
    create_target_order(body,public_key,secret_key)







def create_target_order(body,public_key,secret_key):
    print("开始创建采购单：产品是："+body["targets"][0]["attributes"]["title"]+"价格是："+str(body["targets"][0]["price"]["amount"])+"，数量是："+str(body["targets"][0]["amount"]))
    api_url_path = "/exchange/v1/target/create"
    method = "POST"
    nonce = str(round(datetime.now().timestamp()))
    string_to_sign = method + api_url_path + json.dumps(body) + nonce
    signature_prefix = "dmar ed25519 "
    encoded = string_to_sign.encode('utf-8')
    secret_bytes = bytes.fromhex(secret_key)
    signature_bytes = crypto_sign(encoded, bytes.fromhex(secret_key))
    signature = signature_bytes[:64].hex()
    headers = {
        "X-Api-Key": public_key,
        "X-Request-Sign": signature_prefix + signature,
        "X-Sign-Date": nonce
    }
    global has_notified
    try:
        resp = requests.post(rootApiUrl + api_url_path, json=body, headers=headers)
        result = json.loads(resp.text)
        if result["results"][0]['ok']:
            print("创建采购单成功："+result["results"][0]['targetId'])
        else:
            print("创建采购单失败："+result["results"][0]['message'])
            messagesend.notify_email("创建采购单失败："+result["results"][0]['message'],has_notified)
            has_notified=True
    except Exception as e:
        print(result)
        print("创建采购单异常："+str(e))


if __name__ == '__main__':
    offer_from_market = get_offer_from_market(title="StatTrak™ Five-SeveN | Hybrid (Field-Tested)")
    offer=offer_from_market[0]
    body = build_target_body_from_offer(price=offer["price"]['USD'],amount=1,title=offer["title"],public_key=config.dmarket_public_key,secret_key=config.dmarket_secret_key)
    
