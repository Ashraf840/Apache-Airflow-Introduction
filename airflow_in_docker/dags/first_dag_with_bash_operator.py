from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator


# Airflow DAG with BashOperator


default_args = {
    'Owner': 'Kh Tanjim Ashra',
    'retires': 5,   # Max retry
    'retry_delay': timedelta(minutes=2)     # Wait for 2 mins before every retry
}


with DAG(
    dag_id="out_first_dag_V4",     # Unique DAG id
    description="This is my first dag!",
    default_args=default_args,
    start_date=datetime(2023, 12, 20, 13),  # Starting date of the date; at 13 or 1pm
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello world! This is the first task!"
    )

    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo this is the second task!"
    )

    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo this is the third task, it will be running after task1 and at the same time as task2!"
    )


    # Task2 & task3 are the downstream version of task1
    # Task dependency method-1
    task1.set_downstream(task2)
    task1.set_downstream(task3)

    # Task dependency method-2 (Bit-shift operator)
    # task1 >> task2
    # task1 >> task3

    # Task dependency method-3 
    task1 >> [task2, task3]

