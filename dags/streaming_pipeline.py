from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta
import json
import os
import snowflake.connector

from scripts import load_log_to_snowflake

STREAM_PATH = "/opt/airflow/data/streaming_logs"
SNOWFLAKE_CONFIG = {
    'user': 'YOUR_USER',
    'password': 'YOUR_PASSWORD',
    'account': 'YOUR_ACCOUNT',
    'warehouse': 'YOUR_WAREHOUSE',
    'database': 'YOUR_DATABASE',
    'schema': 'YOUR_SCHEMA'
}

# Load new log file to Snowflake
def load_log_to_snowflake(filename):
    filepath = os.path.join(STREAM_PATH, filename)
    with open(filepath, 'r') as f:
        logs = json.load(f)
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()
    for log in logs:
        cursor.execute("""
            INSERT INTO raw_events (user_id, event_type, event_time)
            VALUES (%s, %s, %s)
        """, (log['user_id'], log['event_type'], log['event_time']))
    cursor.close()
    conn.close()

# DAG definition
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    dag_id='streaming_pipeline',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@hourly',
    catchup=False
)

file_sensor = FileSensor(
    task_id='wait_for_log_file',
    filepath='data/streaming_logs/log1.json',
    fs_conn_id='fs_default',
    poke_interval=30,
    timeout=300,
    mode='poke',
    dag=dag
)

load_task = PythonOperator(
    task_id='load_log_to_snowflake',
    python_callable=load_log_to_snowflake,
    op_args=['log1.json'],
    dag=dag
)

transform_events = SnowflakeOperator(
    task_id='transform_streaming_data',
    sql="include/sql/create_fact_user_activity.sql",
    snowflake_conn_id="snowflake_default",
    dag=dag
)

file_sensor >> load_task >> transform_events
