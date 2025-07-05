# scripts/stream_simulator.py
import json
import time
import random
import os
from datetime import datetime

STREAM_DIR = "data/streaming_logs"
USERS = [1, 2, 3, 4, 5]
EVENTS = ["login", "logout", "purchase", "click"]

os.makedirs(STREAM_DIR, exist_ok=True)

def generate_log():
    logs = []
    for _ in range(5):
        logs.append({
            "user_id": random.choice(USERS),
            "event_type": random.choice(EVENTS),
            "event_time": datetime.utcnow().isoformat()
        })
    return logs

if __name__ == "__main__":
    for i in range(1, 4):
        log_file = os.path.join(STREAM_DIR, f"log{i}.json")
        with open(log_file, 'w') as f:
            json.dump(generate_log(), f, indent=2)
        print(f"Generated {log_file}")
        time.sleep(30)  # simulate delay
