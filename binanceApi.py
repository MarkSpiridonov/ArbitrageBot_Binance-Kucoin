import requests
import json


# упаковали всё в класс
class BinanceClient:
    # Добавили метод для получение всех торгуемых пар
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
                orderBook["buy"] = data["bids"][0][0]
                orderBook["sell"] = data["asks"][0][0]
            else:
                orderBook["check"] = False

            return orderBook
        except:
            print(pair)


BinanceClient.get_all_pair()
