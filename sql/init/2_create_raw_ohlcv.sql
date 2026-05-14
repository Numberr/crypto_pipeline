CREATE TABLE IF NOT EXISTS raw_ohlcv (
    id                  bigserial PRIMARY KEY,
    symbol              text NOT NULL,
    open_time           bigint NOT NULL,
    open                numeric(20,8) NOT NULL,
    high                numeric(20,8) NOT NULL,
    low                 numeric(20,8) NOT NULL,
    close               numeric(20,8) NOT NULL,
    volume              numeric(20,8) NOT NULL,
    close_time          bigint NOT NULL,
    number_of_trades    int,
    quote_asset_volume  numeric(30,8) NOT NULL,
    loaded_at           timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_raw_ohlcv_symbol_time
    ON raw_ohlcv (symbol, open_time)