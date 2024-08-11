import json
from datetime import datetime

from nacl.bindings import crypto_sign
import requests

import config
public_key = config.dmarket_public_key
secret_key = config.dmarket_secret_key

# change url to prod
rootApiUrl = "https://api.dmarket.com"


def get_offer_from_market():
    market_response = requests.get(rootApiUrl + "/exchange/v1/market/items?gameId=a8db&limit=50&currency=USD&title=Kilowatt Case&orderBy=best_discount&orderDir=desc")
    offers = json.loads(market_response.text)["objects"]
    return offers


def build_target_body_from_offer(offer):
    return {"targets": [
        {"amount": 1, "gameId": offer["gameId"], "price": {"amount": "2", "currency": "USD"},
         "attributes": {"gameId": offer["gameId"],
                        "categoryPath": offer["extra"]["categoryPath"],
                        "title": offer["title"],
                        "name": offer["title"],
                        "image": offer["image"],
                        "ownerGets": {"amount": "1", "currency": "USD"}}}
    ]}


nonce = str(round(datetime.now().timestamp()))
api_url_path = "/exchange/v1/target/create"
method = "POST"
offer_from_market = get_offer_from_market()
# body = build_target_body_from_offer(offer_from_market)
print(offer_from_market)


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

# resp = requests.post(rootApiUrl + api_url_path, json=body, headers=headers)
# print(resp.text)
