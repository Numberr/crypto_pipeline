
# Список монет для сбора
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "TONUSDT",
]

# SQL
SQL_INIT_FILES = [
        'sql/init/1_create_dim_symbol.sql',
        'sql/init/2_create_raw_ohlcv.sql',
        'sql/init/3_create_stg_ohlcv.sql',
        'sql/init/4_create_mart_hourly.sql'
        ]
SQL_RAW_TO_STG = 'sql/transforms/raw_to_stg.sql'
SQL_STG_TO_MART = 'sql/transforms/stg_to_mart.sql'
SQL_FINAL_CHECK = 'sql/check/final_check.sql'

# Binance
BINANCE_BASE_URL = "https://api.binance.com"
KLINES_INTERVAL = "1h"
KLINES_LIMIT = 24       # сколько последних свечей брать

# ДЛЯ main
CREATE_TABLES = False
FETCH_AND_LOAD_RAW_KLINES = True
RUN_TRANSFORMS = True