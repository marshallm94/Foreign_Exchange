import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import psycopg2
import pyspark as ps
import datetime as dt

def get_rates(currency_code='all'):
    '''
    Returns exchange rate information from the specified currency to USD.

    Parameters
    ----------
    currency_code : (str)
        Exchange rate identifier. Options include 'JPY', 'CHF', 'EUR' and 'GBP'.
        If you would like all returned in one DataFrame, use 'all'.

    Returns
    ----------
    df : (Pandas DataFrame)
        DataFrame containing exchange rate information from the specified
        currency code.
    '''
    connection = psycopg2.connect(host='foreign-exchange.cknsthfbpmik.us-east-1.rds.amazonaws.com',
                         dbname='forex',
                         user='awsuser',
                         port='5432',
                         password='foreignexchange')

    with connection.cursor() as cursor:
        if currency_code == 'all':
            cursor.execute("""
            SELECT *
            FROM public.majors;
            """)
        else:
            cursor.execute("""
            SELECT *
            FROM public.majors
            WHERE from_currency_code = '{}';
            """.format(currency_code))
        df = pd.DataFrame(cursor.fetchall(),
                          columns=['from_currency_code',
                                   'from_currency_name',
                                   'to_currency_code',
                                   'to_currency_name',
                                   'exchange_rate',
                                   'last_refreshed',
                                   'time_zone'])

    connection.commit()
    connection.close()

    df.set_index('last_refreshed', inplace=True)

    return df


def plot_date_range(df, start_date, end_date=False):
    start_mask = df.index >= start_date
    if end_date:
        end_mask = df.index <= end_date
        display_df = df[start_mask & end_mask].copy()
    else:
        display_df = df[start_mask].copy()

    days = mdates.DateLocator()
    fig, ax = plt.subplots(figsize=(12,8))

    ax.plot(display_df.index, display_df['exchange_rate'])
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    # ax.xaxis.set_minor_locator(mdates.HourLocator())
    # ax.yaxis.set_label_coords(-0.115,0.5)

    title = np.unique(display_df['from_currency_code'])[0] + ":" + "USD"
    plt.suptitle(title, fontweight='bold', fontsize=19)
    plt.xlabel('Date', fontweight='bold', fontsize=15)
    plt.ylabel("Rate", fontweight='bold', rotation=0, fontsize=15)

    fig.autofmt_xdate()
    plt.show()


def plot_single_date(date):
    pass


if __name__ == "__main__":

    # master_df = get_rates()

    master_df = pd.read_csv("../data/final_data_10_03_2018.csv")

    master_df.set_index('last_refreshed', inplace=True)

    japan_df = master_df[master_df['from_currency_code'] == 'JPY']
    swiss_df = master_df[master_df['from_currency_code'] == 'CHF']
    euro_df = master_df[master_df['from_currency_code'] == 'EUR']
    british_df = master_df[master_df['from_currency_code'] == 'GBP']

    plot_date_range(japan_df, start_date='2018-09-20', end_date='2018-09-28')
    plot_date_range(swiss_df, start_date='2018-09-20', end_date='2018-09-28')
    plot_date_range(euro_df, start_date='2018-08-20', end_date='2018-08-28')
    plot_date_range(british_df, start_date='2018-08-20', end_date='2018-08-28')

    # spark = ps.sql.SparkSession.builder.master('local[4]').appName('Foreign Exchange').getOrCreate()
    #
    # sc = spark.sparkContext
    #
    # jdbc_url = 'arn:aws:rds:us-east-1:595614743545:db:foreign-exchange'
    #
    # aws = spark.read.jdbc(url=jdbc_url, table='majors')
