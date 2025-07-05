# Load new log file to Snowflake
from airflow.models import Variable
import json
import os
import snowflake.connector


STREAM_PATH = "/data/streaming_logs"
SNOWFLAKE_CONFIG = {
    'user': Variable.get('YOUR_USER'),
    'password': Variable.get('YOUR_PASSWORD'),
    'account': Variable.get('YOUR_ACCOUNT'),
    'warehouse': Variable.get('YOUR_WAREHOUSE'),
    'database': Variable.get('YOUR_DATABASE'),
    'schema': Variable.get('YOUR_SCHEMA')
}


def load_log_to_snowflake(file_path, table_name):
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT INTO {table_name} ({', '.join(df.columns)})
            VALUES ({', '.join(['%s'] * len(df.columns))})
        """, tuple(row))
    cursor.close()
    conn.close()
    print(f"Loaded {file_path} into {table_name}")

if __name__ == "__main__":
    load_log_to_snowflake("data/sample.csv", "your_table")