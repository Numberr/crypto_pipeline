from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from src.load_raw import fetch_and_load_raw
from src.sql_functions import create_tables, final_check
from src.transform import transform_to_mart
from src.utils import on_check_failure


with DAG(
    dag_id="crypto_pipe",
    start_date=datetime(2025, 5, 1),
    schedule="1 * * * *",
    catchup=False,
) as dag:

    init  = PythonOperator(
        task_id="create_tables",
        python_callable=create_tables,
    )

    fetch_raw = PythonOperator(
        task_id="fetch_raw",
        python_callable=fetch_and_load_raw,
    )

    to_mart = PythonOperator(
        task_id="transform_to_mart",
        python_callable=transform_to_mart,
    )

    check = PythonOperator(
        task_id="final_check_nulls_and_duplicates",
        python_callable=final_check,
        on_failure_callback=on_check_failure
    )

    init >> fetch_raw >> to_mart >> check