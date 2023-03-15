import requests
import json
import hashlib
import hmac
import time
import os


class BinanceClient:
    
    def __init__(self) -> None:
        self.apiKey = os.getenv("api_key_binance")
        self.secretKey = os.getenv("api_secret_binance")

    @staticmethod
    def get_all_pair():
        url = "https://api.binance.com/api/v3/exchangeInfo"

        response = requests.get(url)

        if response.status_code == 200:
            symbols_info = response.json()

            data = [
                f"{symbol['baseAsset']}/{symbol['quoteAsset']}"
                for symbol in symbols_info["symbols"]
                if symbol["quoteAsset"] == "USDT" and symbol["status"] == "TRADING"
            ]

            with open("json/pairBinance.json", "w") as f:
                json.dump(data, f, indent=4)
        return data

    def get_order_book_binance(self, pair, limit):
        try:
            orderBook = {}

            url = "https://api.binance.com/api/v3/depth"

            params = {"symbol": pair, "limit": limit}

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                orderBook["check"] = True
                orderBook["bid"] = data["bids"][0][0]
                orderBook["ask"] = data["asks"][0][0]
            else:
                orderBook["check"] = False

            return orderBook
        except:
            print(pair)

    def check_deposit(self, coin):
        endpoint = "/sapi/v1/capital/config/getall"
        params = {"timestamp": int(time.time() * 1000), "recvWindow": 5000}

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.secretKey.encode(), query_string.encode(), hashlib.sha256
        ).hexdigest()

        params["signature"] = signature

        headers = {"X-MBX-APIKEY": self.apiKey}

        response = requests.get(
            f"https://api.binance.com{endpoint}", params=params, headers=headers
        )

        if (response.status_code == 200):
            for item in response.json():
                if item["coin"] == coin:
                    return item["depositAllEnable"]
        else:
            raise (Exception(response.text))


