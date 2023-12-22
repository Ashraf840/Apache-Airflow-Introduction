from airflow.decorators import dag, task
from datetime import datetime, timedelta

# While using taskflow api, we've to use @dag decorator while tasks will be sub functions of the mother function

default_args = {
    'owner': 'Kh. Tanjim Ashraf',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}


@dag(
    dag_id="dag_with_taskflow_api_v1",
    description="Reduce the LOCs using taskflow api instead of PythonOperator/BashOperator. Return & accept multiple values from a single function.",
    default_args=default_args,
    start_date = datetime(2023, 12, 20, 10),    # starts from 20-Dec-2023 at 10am.
    schedule_interval='@daily'
)
def hello_world_etl():
    # Create 3 tasks (sub-functions)

    # # Return single value
    # @task()
    # def get_name():
    #     return 'Tanjim'

    # Return multiple values
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name':'Jerry',
            'last_name':'Fridman',
        }
    
    @task()
    def get_age():
        return 28
    
    # # Taking single valued-return from functions as multiple params
    # @task()
    # def greet(name, age):
    #     print(f"I'm {name} & {age} years old!")
    
    # Taking multi valued-return from functions as multiple params
    @task()
    def greet(first_name, last_name, age):
        print(f"I'm {first_name} {last_name} & {age} years old!")
    

    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'],
          last_name=name_dict['last_name'], 
          age=age)

# Lastly, create an instance of the dag (parent method).
greet_dag = hello_world_etl()


# with DAG(
#     dag_id='dag_withtaskflow_api_v1',
#     description="Reduce the line of code using taskflow api instead of PythonOperator or BashOperator",
#     default_args=default_args,
#     start_date= datetime(2023, 12, 20, 10),  # starts from 20-Dec-2023 at 10am.
#     schedule_interval='@daily',
# ) as dag:
#     pass
