import time
import hmac
import hashlib
import base64
import requests
import json
import os


class KucoinClient:
    def __init__(self) -> None:
        self.apiKey = os.getenv("api_key_kucoin")
        self.apiSecret = os.getenv("api_secret_kucoin")
        self.apiPassphrase = os.getenv("api_passphrase_kucoin")

    @staticmethod
    def get_all_pair():
        url = "https://api.kucoin.com/api/v2/symbols"
        response = requests.get(url)

        if response.status_code == 200:
            symbols_info = response.json()
            pairs = {}

            for symbol in symbols_info["data"]:
                if symbol["quoteCurrency"] == "USDT":
                    pair_name = symbol["name"].replace("-", "/")
                    pairs[pair_name] = symbol["baseCurrency"]

            with open("json/pairKucoin.json", "w") as f:
                json.dump(pairs, f, indent=4)

            return [list(pairs.keys()), pairs]

    def get_order_book_kucoin(self, pair):
        orderBook = {}

        url = "https://api.kucoin.com/api/v1/market/orderbook/level2_20"

        params = {"symbol": pair}

        response = requests.get(url, params=params)

        try:
            if response.status_code == 200:
                data = response.json()
                orderBook["check"] = True
                orderBook["bid"] = data["data"]["bids"][0][0]
                orderBook["ask"] = data["data"]["asks"][0][0]
            else:
                orderBook["check"] = False
        except Exception as exc:
            print(exc)

        return orderBook

    def check_withdrawal(self, coin: str):
        url = f"https://api.kucoin.com/api/v1/withdrawals/quotas?currency={coin}"

        now = int(time.time() * 1000)
        str_to_sign = str(now) + "GET" + f"/api/v1/withdrawals/quotas?currency={coin}"
        signature = base64.b64encode(
            hmac.new(
                self.apiSecret.encode("utf-8"),
                str_to_sign.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        )
        passphrase = base64.b64encode(
            hmac.new(
                self.apiSecret.encode("utf-8"),
                self.apiPassphrase.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        )
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.apiKey,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
        }
        response = requests.request("get", url, headers=headers)
        return response.json()["isWithdrawEnabled"]

    def check_deposit(self, coin: str):
        url = "https://api.kucoin.com/api/v1/deposit-addresses"
        data = {"currency": coin}
        data_json = json.dumps(data)

        now = int(time.time() * 1000)
        str_to_sign = str(now) + "POST" + "/api/v1/deposit-addresses" + data_json
        signature = base64.b64encode(
            hmac.new(
                self.apiSecret.encode("utf-8"),
                str_to_sign.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        )
        passphrase = base64.b64encode(
            hmac.new(
                self.apiSecret.encode("utf-8"),
                self.apiPassphrase.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        )
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.apiKey,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json",
        }
        response = requests.request("post", url, headers=headers, data=data_json)
        return response.json()["code"] != "260200"
