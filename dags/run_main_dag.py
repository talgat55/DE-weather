from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts import main


with DAG(
    dag_id="run_main_script_dag",
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    catchup=False,
) as dag:
    run_main= PythonOperator(
        task_id="run_main_script_dag",
        python_callable=main.run_main
    )