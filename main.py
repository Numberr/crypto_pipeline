import logging
from src.load_raw import fetch_and_load_raw
from config import FETCH_AND_LOAD_RAW_KLINES, CREATE_TABLES, RUN_TRANSFORMS
from src.sql_functions import create_tables
from src.transform import transform_to_mart


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger(__name__)

def main():
    try:

        if CREATE_TABLES:
            create_tables()

        if FETCH_AND_LOAD_RAW_KLINES:
            fetch_and_load_raw()
        
        if RUN_TRANSFORMS:
            transform_to_mart()

    except Exception as err:
        log.exception(f'Error: {err}')

if __name__=='__main__':
    main()