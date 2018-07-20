CREATE DATABASE foreign_exchange_application OWNER postgres;
\c foreign_exchange_application
CREATE TABLE public.foreign_exchange (
    from_currency_code CHAR(3),
    from_currency_name TEXT,
    to_currency_code CHAR(3),
    to_currency_name TEXT,
    exchange_rate NUMERIC,
    last_refreshed TIMESTAMP,
    time_zone CHAR(3)
);
