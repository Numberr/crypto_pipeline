CREATE TABLE IF NOT EXISTS stg_ohlcv (
    id                  bigserial PRIMARY KEY,
    symbol_id           int NOT NULL REFERENCES dim_symbol(id),
    trade_date          timestamptz NOT NULL,
    open                numeric(20,8) NOT NULL,
    high                numeric(20,8) NOT NULL,
    low                 numeric(20,8) NOT NULL,
    close               numeric(20,8) NOT NULL,
    volume              numeric(20,8) NOT NULL,
    quote_volume        numeric(20,8) NOT NULL,
    trades_count        int,

    CONSTRAINT uq_stg_symbol_date   UNIQUE (symbol_id, trade_date),
    CONSTRAINT check_stg_high_low   CHECK (high >= low),
    CONSTRAINT check_stg_volume     CHECK (volume >=0),
    CONSTRAINT check_stg_price_pos  CHECK (open > 0 AND high > 0 AND low > 0 AND close > 0)

)