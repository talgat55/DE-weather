from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

from scripts import download, transform, load

from airflow.models import Variable
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowFailException
from airflow.models.xcom_arg import XComArg

import logging
import telegram

default_args = {
    "owner": "airflow",
    "retries": 1,
}

def notify_telegram_on_failure(context):
    try:
        bot_token = Variable.get("telegram_bot_token")
        chat_id = Variable.get("telegram_chat_id")
        bot = telegram.Bot(token=bot_token)
        dag_id = context["dag"].dag_id
        task_id = context["task"].task_id
        bot.send_message(chat_id=chat_id, text=f"DAG {dag_id} failed at task {task_id}")

    except Exception as e:
        logging.error(f"Telegram notification failed: {e}")

with DAG(
    dag_id="weather_etl_pipline",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    on_failure_callback=notify_telegram_on_failure,
) as dag:
    t1 = PythonOperator(
        task_id="download_weather",
        python_callback=download.download_weather_date,
        do_xcom_push=True
    )

    t2 = PythonOperator(
        dag_id="transform",
        python_callback=transform.transform_data,
        op_args=[XComArg(t1)],
    )

    t3 = PythonOperator(
        dag_id="load",
        python_callback=load.load_to_db,
        op_args=[XComArg(t2)],
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    t1 >> t2 >> t3