# Load users data to Snowflake raw_users table
import snowflake.connector
from airflow.models import Variable
import json

DATA_PATH = "/data/users.json"
SNOWFLAKE_CONFIG = {
    'user': Variable.get('YOUR_USER'),
    'password': Variable.get('YOUR_PASSWORD'),
    'account': Variable.get('YOUR_ACCOUNT'),
    'warehouse': Variable.get('YOUR_WAREHOUSE'),
    'database': Variable.get('YOUR_DATABASE'),
    'schema': Variable.get('YOUR_SCHEMA')
}


def load_users_to_snowflake():
    with open(DATA_PATH, 'r') as f:
        users = json.load(f)
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()
    for user in users:
        cursor.execute("""
            INSERT INTO raw_users (id, name, email, created_at)
            VALUES (%s, %s, %s, current_timestamp)
        """, (user['id'], user['name'], user['email']))
    cursor.close()
    conn.close()
