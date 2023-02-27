from binanceApi import BinanceClient
from kucoinApi import KucoinClient
from time import sleep
import json


class Arbitrage:
    def __init__(self):
        self.binanceClient = BinanceClient()
        self.kucoinClient = KucoinClient()

    def check_pair(self, listCoin, telBot, chatId):
        while True:
            for coin in listCoin:  # Добавили новые монеты
                pair = coin["binance"] + "USDT"
                priceBinance = self.binanceClient.get_order_book_binance(
                    pair=pair, limit=1
                )
                pair = coin["kucoin"] + "-USDT"
                priceKucoin = self.kucoinClient.get_order_book_kucoin(pair=pair)

                if priceBinance["check"] and priceKucoin["check"]:
                    buy = float(priceKucoin["buy"])
                    sell = float(priceBinance["sell"])
                    spread = (buy / sell - 1) * 100

                    if spread > 1:
                        message = f"Спред: {round(spread, 2)}%\n{coin['binance']}\nBinance цена: {priceBinance['sell']}\nКукоин цена: {priceKucoin['sell']}"
                        telBot.send_message(chatId, message)

                    # добавил вторую проверку
                    buy = float(priceBinance["buy"])
                    sell = float(priceKucoin["sell"])
                    spread = (buy / sell - 1) * 100

                    if spread > 1:
                        message = f"Спред: {round(spread, 2)}%\n{coin['binance']}\nКукоин цена: {priceKucoin['sell']}\nBinance цена: {priceBinance['sell']}"
                        telBot.send_message(chatId, message)

    @staticmethod
    def compare_and_save():
        binance_symbols = BinanceClient.get_all_pair()
        [kucoin_symbols, kucoin_dict] = KucoinClient.get_all_pair()

        common_symbols = list(set(binance_symbols).intersection(set(kucoin_symbols)))

        with open("json/listPair.json", "w") as f:
            json.dump(list(common_symbols), f, indent=4)

        exchange_coins = []

        for pair in common_symbols:
            exchange_coins.append(
                {
                    "binance": pair.split("/")[0],
                    "kucoin": kucoin_dict[pair],
                }
            )

        with open("json/listCoin.json", "w") as f:
            json.dump(exchange_coins, f, indent=4)


Arbitrage.compare_and_save()
