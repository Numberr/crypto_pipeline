CREATE TABLE IF NOT EXISTS dim_symbol (
    id          serial PRIMARY KEY,
    symbol      text NOT NULL UNIQUE,
    base_asset  text NOT NULL,
    quote_asset text NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);

INSERT INTO dim_symbol (symbol, base_asset, quote_asset) VALUES
    ('BTCUSDT',  'BTC',  'USDT'),
    ('ETHUSDT',  'ETH',  'USDT'),
    ('SOLUSDT',  'SOL',  'USDT'),
    ('BNBUSDT',  'BNB',  'USDT'),
    ('XRPUSDT',  'XRP',  'USDT'),
    ('ADAUSDT',  'ADA',  'USDT'),
    ('DOGEUSDT', 'DOGE', 'USDT'),
    ('AVAXUSDT', 'AVAX', 'USDT'),
    ('LINKUSDT', 'LINK', 'USDT'),
    ('TONUSDT',  'TON',  'USDT')
ON CONFLICT (symbol) DO NOTHING;