import logging
import requests
import os
from src.db import get_conn


log = logging.getLogger(__name__)

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
    send_telegram_message(f"Task was failed! task_id: {task_id}; error: {error}")
    log.error(f"task_id: {task_id}; error: {error}")

def send_telegram_message(msg):

    tg_token = os.getenv("TG_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")

    url = f"https://api.telegram.org/bot{tg_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": msg,
        "disable_web_page_preview": True
    }
    try:
        
        resp = requests.post(url=url, json=payload)
        if resp.status_code == 200:
            log.info(f"Message was sent")

        else:
            error = resp.text
            log.error(f"Error while sending message: {error}")

    except Exception as e:
        log.error(f"Error: {e}")