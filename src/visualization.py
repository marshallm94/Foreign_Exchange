import pyspark as ps
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

def get_rates(currency_code='all'):
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
        df = pd.DataFrame(cursor.fetchall(), columns=['from_currency_code',
                                                      'from_currency_name',
                                                      'to_currency_code',
                                                      'to_currency_name',
                                                      'exchange_rate',
                                                      'last_refreshed',
                                                      'time_zone'])

    connection.commit()
    connection.close()

    return df


if __name__ == "__main__":

    japan_df = get_rates('JPY')
    swiss_df = get_rate('CHF')
    euro_df = get_rates('EUR')
    german_df = get_rates('GBP')
    
    # spark = ps.sql.SparkSession.builder.master('local[4]').appName('Foreign Exchange').getOrCreate()
    #
    # sc = spark.sparkContext
    #
    # jdbc_url = 'arn:aws:rds:us-east-1:595614743545:db:foreign-exchange'
    #
    # aws = spark.read.jdbc(url=jdbc_url, table='majors')
