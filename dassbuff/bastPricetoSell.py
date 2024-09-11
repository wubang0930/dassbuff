import json
from datetime import datetime

from nacl.bindings import crypto_sign
import requests

import config
public_key = config.dmarket_public_key
secret_key = config.dmarket_secret_key


# change url to prod
rootApiUrl = "https://api.dmarket.com"


def get_skin_title():  
    # skins={"千瓦武器箱":"Kilowatt Case","梦魇武器箱":"Dreams%20%26%20Nightmares%20Case","英勇大行动":"Operation Bravo Case"}
    skins={"千瓦武器箱":"Kilowatt Case","梦魇武器箱":"Dreams%20%26%20Nightmares%20Case","英勇大行动":"Operation Bravo Case"}
    return skins



def get_offer_from_market(limit,title,orderBy):
    market_response = requests.get(rootApiUrl + "/exchange/v1/market/items?gameId=a8db&limit="+limit+"&currency=USD&title="+title+"&orderBy="+orderBy+"&orderDir=desc")
    # market_response = requests.get(rootApiUrl + "/marketplace-api/v1/targets-by-title/a8db/Kilowatt Case")
#     headers = {
#     "X-Api-Key": public_key,
#     "X-Sign-Date": nonce
# }
    # market_response = requests.get(rootApiUrl + "/exchange/v1/offers-by-title?Title=Kilowatt Case&Limit=100",headers=headers)
    # market_response = requests.get(rootApiUrl + "/price-aggregator/v1/aggregated-prices?Titles=Kilowatt Case&Limit=100",headers=headers)
    offers = json.loads(market_response.text)["objects"]
    offers = json.loads(market_response.text)
    f= open("offer.json","w")
    f.write(json.dumps(offers))
    f.close()   
    return offers





def build_target_body_from_offer(offers):
    new_list=set()
    for offer in offers:
        new_list.add( offer['price']['USD'])

    max_price = min(new_list)
    return max_price


nonce = str(round(datetime.now().timestamp()))
# api_url_path = "/exchange/v1/target/create"
# api_url_path = "/exchange/v1/offers-by-title?Title=Kilowatt Case&Limit=100"
method = "GET"

skins=get_skin_title()

all_list=[]

for key,value in skins.items():
    offer_from_market = get_offer_from_market(limit="5",title=value,orderBy="price")
    best_price = int(build_target_body_from_offer(offers=offer_from_market))/100*7.24
    all_list.append({key:best_price})

print(all_list)


# string_to_sign = method + api_url_path + json.dumps(body) + nonce
# signature_prefix = "dmar ed25519 "
# encoded = string_to_sign.encode('utf-8')
# secret_bytes = bytes.fromhex(secret_key)
# signature_bytes = crypto_sign(encoded, bytes.fromhex(secret_key))
# signature = signature_bytes[:64].hex()
# headers = {
#     "X-Api-Key": public_key,
#     "X-Request-Sign": signature_prefix + signature,
#     "X-Sign-Date": nonce
# }

# resp = requests.get(rootApiUrl + api_url_path,  headers=headers)
# print(resp.text)
