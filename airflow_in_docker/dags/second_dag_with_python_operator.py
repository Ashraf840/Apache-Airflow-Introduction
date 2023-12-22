from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Kh. Tanjim Ashraf',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


# def greet(name, age):
#     print(f"Hello world!My name is {name} & I'm {age} years old!")

def greet(ti, age):
    name = ti.xcom_pull(task_ids='get_name')
    print(f"Hello world!My name is {name} & I'm {age} years old!")

def get_name():
    return 'Jerry'

with DAG(
    dag_id="dag_with_python_operator_v4",
    description="Our first dag using python operator! Python function takes parameters via XCOMS! Push mutliple values through XCOMS!",
    default_args=default_args,
    start_date=datetime(2023, 12, 20, 8),    # from 8am of 20-Dec-2023, so the first execution would be at 21-Dec-2023 at 8am.
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet,
        op_kwargs={'age': 30},    # Pass a dictionary which will be passes into the python function
    )

    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name
    )
    
    # task1
    task2 >> task1

