from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Kh. Tanjim Ashraf',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id = 'dag_with_catchup_backfill_v2',
    default_args = default_args,
    description = 'Dag to learn catchup & backfill',
    start_date =datetime(2023, 12, 1, 10),
    schedule_interval ='@daily',
    # catchup = True,     # Although it's default value is set to True, we explicitly set it to True
    catchup = False,     # The dag won't execute the dag from the start_date (1-12-2023), instead it'll only execute the last date's dag of the current date
    # NB: To execute the due dags of the previous dates, we need to manually go inside the dag-webserver container. Inside the container it's required to run the following CMD to execute the due dags using backfill feature
    # CMD Skeleton: airflow dags backfill -s [desired_start_date(YY-M-D)] -e [desired_end_date(YY-M-D)] specified_dag_id
    # Original CMD: airflow dags backfill -s 2023-12-1 -e 2023-12-23 dag_with_catchup_backfill_v2
) as dag:
    task1 = BashOperator(
        task_id ='task1',
        bash_command = "echo This is a simple bash command!",
    )
