import requests
import json
import os

# extract user data from a public API, this could be loaded to S3 or GCS
DATA_PATH = "/data/users.json"
def extract_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    users = response.json()
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w') as f:
        json.dump(users, f)
