import telebot
import json

# from binanceApi import get_price_btc
from main import Arbitrage

token = "6175000208:AAHLGjU7VoAohJuulesoQtWom8nM"
telBot = telebot.TeleBot(token)


@telBot.message_handler(commands=["start"])
def start(message):
    telBot.send_message(message.chat.id, "Всё работает!")


# Уберем из функционала
# @telBot.message_handler(commands=["send_price_btc"])
# def send_price_btc(message):
#     priceBTC = get_price_btc()
#     telBot.send_message(message.chat.id, f"Текущая цена BTC/USDT = {priceBTC}")


@telBot.message_handler(commands=["run_check"])
def check_btc(message):
    telBot.send_message(message.chat.id, "Скрипт запущен!")
    with open("json/listCoin.json") as f:
        listCoin = json.load(f)
    arbitrage.check_pair(listCoin, telBot, message.chat.id)


arbitrage = Arbitrage()
telBot.infinity_polling()
