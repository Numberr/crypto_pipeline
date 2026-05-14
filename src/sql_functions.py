from src.db import get_conn
from psycopg2.extras import execute_values
from config import SQL_INIT_FILES, SQL_FINAL_CHECK
from src.utils import run_sql_file


def create_tables():
    files = SQL_INIT_FILES
    for file in files:   
        run_sql_file(file)

#  Массово вставляет записи в raw_ohlcv. rows - список кортежей в порядке колонок таблицы
def insert_raw_ohlcv(rows: list[tuple]) -> int:
    if not rows:
        return 0
    
    sql = '''
        insert into raw_ohlcv (
            symbol, open_time, open, high, low, close, volume, close_time,
            number_of_trades, quote_asset_volume
        ) values %s
    '''

    with get_conn() as conn:
        with conn.cursor() as cursor:
            execute_values(cur=cursor, sql=sql, argslist=rows)
            inserted = cursor.rowcount

        conn.commit()
        
    return inserted

# Сбор данных о свечах
def check_last_klines(symbols: list) -> dict:
    last_klines = {}

    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                select 
                    ro.symbol,
                    max(ro.open_time )
                from raw_ohlcv ro 
                where ro.symbol = ANY(%s)
                group by ro.symbol
            ''', (symbols,))

            res_lst = cursor.fetchall()  # вернёт список с кортежем
            # res = cursor.fetchone() # вернёт (75000,)

            for r in res_lst:
                last_klines[r[0]] = r[1]
            
            return last_klines

def final_check():
    res = run_sql_file(SQL_FINAL_CHECK)
    for count, check_name in res:
        if count > 0:
            raise ValueError(f"Quality check failed: {check_name} = {count}")