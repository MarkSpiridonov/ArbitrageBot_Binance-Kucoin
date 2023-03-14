import requests
import time
import json

def get_info_coin_exchange(exchange: str, coinTarget: str = "USDT") -> dict:
    url = f"https://api.coingecko.com/api/v3/exchanges/{exchange}/tickers"
    tickerList = []

    while True:
        response = requests.get(url)
        if (response.status_code == 429):
            time.sleep(30)
            response = requests.get(url)
            
        data = response.json()
        for t in data["tickers"]:
            if t["target"] == coinTarget and not t["is_stale"]:    
                tickers = {}
                tickers['id'] = t["coin_id"]
                tickers['ticker'] = t["base"]
                tickerList.append(tickers)

        if "next" not in response.links:
            break
        url = response.links["next"]["url"]
        time.sleep(2)
        
    with open(f"json/listCoinCG{exchange}.json", "w") as f:
            json.dump(tickerList, f, indent=4)
    
    return tickerList

def get_list_coin():
    
    with open("json/listCoinCGkucoin.json") as f:
        listCoinKucoin = json.load(f)
        
    with open("json/listCoinCGbinance.json") as f:
        listCoinBinance = json.load(f)

    res = compare_dicts(listCoinKucoin, listCoinBinance)
    
    with open(f"json/listCoinCG.json", "w") as f:
        json.dump(res, f, indent=4)

def compare_dicts(dicts1, dicts2):
    ids = set()
    duplicates = []

    for d in dicts1:
        if d['id'] not in ids:
            ids.add(d['id'])

    with open("json/ignoreCoin.json", "r") as f:
        ignoreList = json.load(f)
                
    for d in dicts2:
        if d['id'] in ids and d['ticker'] not in ignoreList:
            res = {}
            res['id'] = d['id']
            res['binance'] = d['ticker']
            res['kucoin'] = next((item["ticker"] for item in dicts1 if item["id"] == d['id']))
            duplicates.append(res)

    return duplicates

get_list_coin()