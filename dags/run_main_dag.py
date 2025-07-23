from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

from airflow.models.xcom_arg import XComArg
import logging

from scripts import download, transform, load

default_args = {
    "owner": "airflow",
    "retries": 1,
}

def notify_telegram_on_failure(context):
    logging.error("Failure notification placeholder")

with DAG(
    dag_id="weather_etl_pipeline",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    on_failure_callback=notify_telegram_on_failure,
) as dag:

    t1 = PythonOperator(
        task_id="download_weather",
        python_callable=download.download_weather_date,
        do_xcom_push=True
    )

    t2 = PythonOperator(
        task_id="transform_data",
        python_callable=transform.transform_data,
        op_args=[XComArg(t1)],
    )

    t3 = PythonOperator(
        task_id="load_to_db",
        python_callable=load.load_to_db,
        op_args=[XComArg(t2)],
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    t1 >> t2 >> t3
