from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Kh. Tanjim Ashraf',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


def greet(name, age):
    print(f"Hello world!My name is {name} & I'm {age} years old!")


with DAG(
    dag_id="dag_with_python_operator_v2",
    description="Our first dag using python operator! Python function takes parameters!",
    default_args=default_args,
    start_date=datetime(2023, 12, 20, 8),    # from 8am of 20-Dec-2023, so the first execution would be at 21-Dec-2023 at 8am.
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet,
        op_kwargs={'name': 'Tanjim', 'age': 30},    # Pass a dictionary which will be passes into the python function
    )
    
    task1

