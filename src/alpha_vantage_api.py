import requests
import json
import pandas as pd
import psycopg2


if __name__ == "__main__":
    with open("/Users/marsh/api_keys/alpha_vantage_api.json", 'r') as f:
        data = json.load(f)
        api_key = data['api']

    link = "https://www.alphavantage.co/query"

    results_dict = {
        "from_currency_code": [],
        "from_currency_name": [],
        "to_currency_code": [],
        "to_currency_name": [],
        "exchange_rate": [],
        "last_refreshed": [],
        "time_zone": []
    }

    currencies = set(['EUR','JPY','GBP','CHF'])

    for currency in currencies:
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "to_currency": "USD",
            "apikey": api_key
        }
        params['from_currency'] = currency
        response = requests.get(link, params)
        print(response.json())
        result = response.json()['Realtime Currency Exchange Rate']
        results_dict['from_currency_code'].append(result['1. From_Currency Code'])
        results_dict['from_currency_name'].append(result['2. From_Currency Name'])
        results_dict['to_currency_code'].append(result['3. To_Currency Code'])
        results_dict['to_currency_name'].append(result['4. To_Currency Name'])
        results_dict['exchange_rate'].append(float(result['5. Exchange Rate']))
        results_dict['last_refreshed'].append(result['6. Last Refreshed'])
        results_dict['time_zone'].append(result['7. Time Zone'])

    df = pd.DataFrame(results_dict, index=list(range(4)))

    connection = psycopg2.connect(dbname='foreign_exchange', user='admin')
    cursor = connection.cursor()

    cursor.execture("""
    CREATE TABLE IF NOT EXISTS foreign_exchange


    """)

    connection.commit()
    cursor.close()
    connection.clost()
