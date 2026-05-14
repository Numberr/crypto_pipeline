import requests
from decimal import Decimal
from config import BINANCE_BASE_URL, KLINES_INTERVAL, KLINES_LIMIT


def fetch_klines(symbol: str, start_time: int | None) -> list[list]:
    url = BINANCE_BASE_URL + '/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': KLINES_INTERVAL,
        'limit':    KLINES_LIMIT,
    }

    if start_time:
        params['startTime'] = start_time

    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()

    return resp.json()

# Приводим к кортежу (тк immutable); строки в нужный формат
def normalize_kline(kline: list, symbol: str):

    return (
        symbol,
        kline[0],               # Kline open time
        Decimal(kline[1]),      # Open price
        Decimal(kline[2]),      # High price
        Decimal(kline[3]),      # Low price
        Decimal(kline[4]),      # Close price
        Decimal(kline[5]),      # Volume
        kline[6],               # Kline Close time
        kline[8],               # Number of trades
        Decimal(kline[7])       # Quote asset volume
    )