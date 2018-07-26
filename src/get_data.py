import psycopg2
import pandas as pd

connection = psycopg2.connect(host='foreign-exchange.cknsthfbpmik.us-east-1.rds.amazonaws.com',
                     dbname='forex',
                     user='awsuser',
                     port='5432',
                     password='foreignexchange')

with connection.cursor() as cursor:
    cursor.execute("""
    SELECT * FROM public.majors;
    """)
    df = pd.DataFrame(cursor.fetchall(), columns=['from_currency_code',
                                                  'from_currency_name',
                                                  'to_currency_code',
                                                  'to_currency_name',
                                                  'exchange_rate',
                                                  'last_refreshed',
                                                  'time_zone'])
    print(df)

connection.commit()
connection.close()
