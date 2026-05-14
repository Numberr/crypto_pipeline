import logging
import time

from src.binance_client import fetch_klines, normalize_kline
from src.sql_functions import insert_raw_ohlcv, check_last_klines
from config import SYMBOLS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger(__name__)


def load_symbol(symbol: str, start_time: int | None) -> int:
    log.info(f'Fetching {symbol}')

    raw_klines = fetch_klines(symbol=symbol, start_time=start_time)
    log.info(f'Got {len(raw_klines)} klines for {symbol}')

    n_raw_klines = [normalize_kline(kline=kline, symbol=symbol) for kline in raw_klines]

    inserted = insert_raw_ohlcv(n_raw_klines)
    log.info(f'Inserted {inserted} lines')

    return inserted

def fetch_and_load_raw():
    log.info(f'Starting load for {len(SYMBOLS)} symbols')
    total_inserted = 0

    last_klines = check_last_klines(SYMBOLS)

    for symbol in SYMBOLS:
        try:
            start_time = last_klines.get(symbol)
            inserted = load_symbol(symbol=symbol,start_time=start_time)

            if inserted:
                total_inserted += inserted
                
        except Exception:
            log.exception(f"Failed to load {symbol}")

        time.sleep(1)
    
    log.info(f"Done. Total inserted: {total_inserted} rows")