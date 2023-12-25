from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Kh. Tanjim Ashraf',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id = 'dag_with_cron_expression_v6',
    default_args = default_args,
    description = 'Dag with custom cron expression instead of airflow preset cron expression',
    start_date = datetime(2023, 11, 30, 8),
    # schedule_interval = '0 0 * * *',    # Instead of '@daily' using the cron expression of daily execution
    # schedule_interval = '0 3 * * Sun',    # Cron expression: run weekly on Sunday at 3am
    # schedule_interval = '0 3 * * Fri,Sun',    # Cron expression: run weekly on Friday & Sunday at 3am
    schedule_interval = '0 3 * * Wed-Fri',    # Cron expression: run weekly from Wednesday to Friday at 3am; after passing the 29-12-2023 the due dags of 20,21,22 dates will be executed.
    # NB: Use the following URL to get a visual way of setting up a cron expression
    # URL: https://crontab.guru/#0_0_*_*_*
) as dag:
    task1 = BashOperator(
        task_id = 'task1',
        bash_command = 'echo Dag with cron expression!'
    )
