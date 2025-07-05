from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta

from scripts import extract_users, load_users_to_snowflake


# Default arguments for DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='airflow_snowflake_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False
)

extract_task = PythonOperator(
    task_id='extract_users',
    python_callable=extract_users,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_users_to_snowflake',
    python_callable=load_users_to_snowflake,
    dag=dag
)

transform_task = SnowflakeOperator(
    task_id='transform_users',
    sql="include/sql/transform_users.sql",
    snowflake_conn_id="snowflake_default",
    dag=dag
)

data_quality_task = SnowflakeOperator(
    task_id='run_data_quality_checks',
    sql="include/sql/data_quality_checks.sql",
    snowflake_conn_id="snowflake_default",
    dag=dag
)

extract_task >> load_task >> transform_task >> data_quality_task
