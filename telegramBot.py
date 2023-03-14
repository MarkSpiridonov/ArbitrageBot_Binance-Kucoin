import telebot
import json
from main import Arbitrage
from dotenv import load_dotenv
import os

load_dotenv()  # подгрузить env

token = os.getenv("api_telegram_token")
telBot = telebot.TeleBot(token)


@telBot.message_handler(commands=["start"])
def start(message):
    telBot.send_message(message.chat.id, "Всё работает!")


@telBot.message_handler(commands=["run_check"])
def check_btc(message):
    telBot.send_message(message.chat.id, "Скрипт запущен!")
    with open("json/listCoinCG.json") as f:
        listCoin = json.load(f)
    arbitrage.check_pair(listCoin, telBot, message.chat.id)


arbitrage = Arbitrage()
telBot.infinity_polling()
