import requests
import json


if __name__ == "__main__":
    with open("/Users/marsh/api_keys/alpha_vantage_api.json", 'r') as f:
        data = json.load(f)
        api_key = data['api']

    link = "https://www.alphavantage.co/query"

    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "EUR",
        "to_currency": "USD",
        "apikey": api_key
    }

    response = requests.get(link, params)
    data = response.json()['Realtime Currency Exchange Rate']
    for key, value in data.items():
        new_key = key[3:].lower().replace(" ", "_")
        print(new_key, ":", value)
