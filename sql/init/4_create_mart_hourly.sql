CREATE TABLE IF NOT EXISTS mart_hourly (
    symbol_id       INT NOT NULL REFERENCES dim_symbol(id),
    trade_hour      TIMESTAMPTZ NOT NULL,
    close           NUMERIC(20, 8) NOT NULL,
    volume          NUMERIC(30, 8) NOT NULL,
    volume_usd      NUMERIC(30, 8),
    hourly_return   NUMERIC(10, 6),
    volatility_12h  NUMERIC(10, 6),
    volatility_24h  NUMERIC(10, 6),
    ma12            NUMERIC(20, 8),
    ma24            NUMERIC(20, 8),
    PRIMARY KEY (symbol_id, trade_hour)
)