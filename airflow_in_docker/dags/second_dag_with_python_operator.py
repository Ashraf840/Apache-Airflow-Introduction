from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


# Airflow DAG using PythonOperator

# Initially using 'op_kwrags' to pass values between tasks. Then shifted to XCOMS for this purpose.
# But one IMPORTANT thing to keep in mind: XCOM can hold upto 48kib of data only.


default_args = {
    'owner': 'Kh. Tanjim Ashraf',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


# def greet(name, age):
#     print(f"Hello world!My name is {name} & I'm {age} years old!")

# # Pull a single value from a task 'greet
# def greet(ti, age):     # ti = task instance
#     name = ti.xcom_pull(task_ids='get_name')
#     print(f"Hello world!My name is {name} & I'm {age} years old!")

# # Return & store a single to XCOMS via returning a value from this 'greet' function.
# def get_name():
#     return 'Jerry'

# Strore multiple values to XCOMS using a single function.
def get_name(ti):
    ti.xcom_push(key="first_name", value="Jerry")
    ti.xcom_push(key='last_name', value='Fridman')

def get_age(ti):
    ti.xcom_push(key='age', value=28)

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Hello world!My name is {first_name} {last_name} & I'm {age} years old!")


with DAG(
    dag_id="dag_with_python_operator_v6",
    description="Our first dag using python operator! Python function takes parameters via XCOMS! Push & pull mutliple values through XCOMS! Mitigating the usecase of 'op_kwargs' param!",
    default_args=default_args,
    start_date=datetime(2023, 12, 20, 8),    # from 8am of 20-Dec-2023, so the first execution would be at 21-Dec-2023 at 8am.
    schedule_interval='@daily',
) as dag:
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet,
        # op_kwargs={'name':'Tanjim Ashraf', 'age': 30},    # Pass a dictionary which will be passes into the python function. Not required now, pulling values (single & mutliple) from XCOMS
        # op_kwargs={'age': 30},    # Pass a dictionary which will be passes into the python function. Not required now, pulling values (single & mutliple) from XCOMS
    )

    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name,
    )

    task3 = PythonOperator(
        task_id="get_age",
        python_callable=get_age,
    )
    
    # task1
    # task2 >> task1

    # BitShift Operator for defining task-dependencies
    [task2, task3] >> task1

