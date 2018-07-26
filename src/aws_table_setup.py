import psycopg2

connection = psycopg2.connect(host='foreign-exchange.cknsthfbpmik.us-east-1.rds.amazonaws.com',
                     dbname='forex',
                     user='awsuser',
                     port='5432',
                     password='foreignexchange')

with connection.cursor() as cursor:
    cursor.execute("""
    CREATE TABLE public.majors (
        from_currency_code CHAR(3),
        from_currency_name TEXT,
        to_currency_code CHAR(3),
        to_currency_name TEXT,
        exchange_rate NUMERIC,
        last_refreshed TIMESTAMP,
        time_zone CHAR(3)
    );
    """)

connection.commit()
connection.close()
