import logging
from src.utils import run_sql_file
from config import SQL_STG_TO_MART, SQL_RAW_TO_STG


log = logging.getLogger(__name__)

def transform_to_mart():

    log.info('Running raw to stg...')
    run_sql_file(SQL_RAW_TO_STG)
    # Добавить что то чтоб успех отследить?

    log.info('Running stg to mart...')
    run_sql_file(SQL_STG_TO_MART)