import logging
from src.db import get_conn


def run_sql_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchall() if cur.description is not None else []
        
        conn.commit()

        return res
    
def on_check_failure(context):
    task_id = context['task_instance'].task_id
    error = context['exception']
    log = logging.getLogger(__name__)
    log.error(f"task_id: {task_id}; error: {error}")
    # еще что то...