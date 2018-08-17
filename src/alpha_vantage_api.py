import requests
import json
import psycopg2
import time
import pandas as pd


def format_api_response(from_curr_code, to_curr_code='USD', link="https://www.alphavantage.co/query"):
    '''
    Formats the response from the Alpha Vantage API.

    Parameters:
    ----------
    from_curr_code : (str)
        The currency code of the currency for which the exchange rate
        should be retrieved (relative to USD)
    to_curr_code : (str)
        The currency code of the currency for which from_curr_code should
        be compared to
    link : (str)
        API link (default is Alpha Vantage API)

    Returns:
    ----------
    results_dict : (dictionary)
        Dictionary formatted with exchange rate information for the inputted
        currency codes
    '''
    results_dict = {}

    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "to_currency": "USD",
        "apikey": api_key
    }
    params['from_currency'] = from_curr_code

    response = requests.get(link, params)

    result = response.json().get('Realtime Currency Exchange Rate', 'API Call Frequency Exceeded')
    results_dict['from_currency_code'] = result['1. From_Currency Code']
    results_dict['from_currency_name'] = result['2. From_Currency Name']
    results_dict['to_currency_code'] = result['3. To_Currency Code']
    results_dict['to_currency_name'] = result['4. To_Currency Name']
    results_dict['exchange_rate'] = float(result['5. Exchange Rate'])
    results_dict['last_refreshed'] = result['6. Last Refreshed']
    results_dict['time_zone'] = result['7. Time Zone']

    return results_dict


if __name__ == "__main__":
    # if on local:
    with open("/Users/marsh/api_keys/alpha_vantage_api.json", 'r') as f:
        data = json.load(f)
        api_key = data['api']

    # if on VM:
    # with open("/home/hadoop/Foreign_Exchange/src/alpha_vantage_api.json", 'r') as f:
    #     data = json.load(f)
    #     api_key = data['api']

    connection = psycopg2.connect(host='foreign-exchange.cknsthfbpmik.us-east-1.rds.amazonaws.com',
                         dbname='forex',
                         user='awsuser',
                         port='5432',
                         password='foreignexchange')

    currencies = set(['EUR','JPY','GBP','CHF'])
    for curr in currencies:
        results_dict = format_api_response(curr)
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO public.majors
                (from_currency_code,
                from_currency_name,
                to_currency_code,
                to_currency_name,
                exchange_rate,
                last_refreshed,
                time_zone) VALUES
                ('{}',
                 '{}',
                 '{}',
                 '{}',
                 '{}',
                 '{}',
                 '{}');
            """.format(results_dict["from_currency_code"],
                       results_dict["from_currency_name"],
                       results_dict["to_currency_code"],
                       results_dict["to_currency_name"],
                       results_dict["exchange_rate"],
                       results_dict["last_refreshed"],
                       results_dict["time_zone"]))
        time.sleep(30)

    connection.commit()
    connection.close()
