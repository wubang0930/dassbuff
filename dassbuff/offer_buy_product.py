import json
from datetime import datetime

from nacl.bindings import crypto_sign
import requests
import config
public_key = config.dmarket_public_key
secret_key = config.dmarket_secret_key

# change url to prod
rootApiUrl = "https://api.dmarket.com"



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
def build_target_body_from_offer(offer,amount=1):
    return {"targets": [
        {"amount": amount, "gameId": offer["gameId"], "price": {"amount": "2", "currency": "USD"},
         "attributes": {"gameId": offer["gameId"],
                        "categoryPath": offer["extra"]["categoryPath"],
                        "title": offer["title"],
                        "name": offer["title"],
                        "image": offer["image"],
                        "ownerGets": {"amount": "1", "currency": "USD"}}}
    ]}







def create_target_order(body):
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

    resp = requests.post(rootApiUrl + api_url_path, json=body, headers=headers)
    result = json.loads(resp.text)
    if result["results"][0]['ok']:
        print("创建采购单成功："+result["results"][0]['targetId'])
    else:
        print("创建采购单失败："+result["results"][0]['message'])


if __name__ == '__main__':
    offer_from_market = get_offer_from_market(title="P250 | Verdigris (Battle-Scarred)")
    body = build_target_body_from_offer(offer=offer_from_market[0],amount=1)
    create_target_order(body)
