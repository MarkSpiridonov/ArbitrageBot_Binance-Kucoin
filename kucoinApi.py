import requests
import json


# упаковали всё в класс
class KucoinClient:
    # Добавили метод для получение всех торгуемых пар
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

        if response.status_code == 200:
            data = response.json()
            orderBook["check"] = True
            orderBook["buy"] = data["data"]["bids"][0][0]
            orderBook["sell"] = data["data"]["asks"][0][0]
        else:
            orderBook["check"] = False

        return orderBook
