import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CB_ACCESS_KEY")
API_SECRET = os.getenv("CB_ACCESS_SIGN")
API_PASS = os.getenv("CB_ACCESS_PASSPHRASE")

api_url = "https://api.pro.coinbase.com/"

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()
        # signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

# Get accounts
request = requests.get(api_url + 'accounts', auth=auth)
json_req = request.json()
parsed_json = json.dumps(json_req, indent=4, sort_keys=True)

print(parsed_json)
f = open("accounts.json", "w")
f.write(parsed_json)
f.close()

# f = open("myfile.txt", "r")
# print(f.read())

# [{"id": "a1b2c3d4", "balance":...

# # Place an order
# order = {
#     'size': 1.0,
#     'price': 1.0,
#     'side': 'buy',
#     'product_id': 'BTC-USD',
# }
# r = requests.post(api_url + 'orders', json=order, auth=auth)

# print(r.json())
# # {"id": "0428b97b-bec1-429e-a94c-59992926778d"}
