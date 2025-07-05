import os
from pathlib import Path

# Project structure definition - taken from README 
# Customizable
structure = {
    "dags": ["airflow_snowflake_pipeline.py", "streaming_pipeline.py"],
    "include/sql": [
        "transform_users.sql",
        "create_fact_user_activity.sql",
        "data_quality_checks.sql",
    ],
    "plugins": [],
    "data": ["users.json", "streaming_logs/log1.json", "streaming_logs/log2.json"],
    "dbt_project/models": [
        "staging/stg_users.sql",
        "staging/stg_events.sql",
        "marts/dim_users.sql",
        "marts/fact_user_activity.sql",
        "marts/user_event_metrics.sql",
        "seeds/user_activity.csv",
    ],
    "dbt_project": ["dbt_project.yml", "profiles.yml"],
    "scripts": [
        "extract_users.py",
        "stream_simulator.py",
        "snowflake_loader.py",
    ],
}

# Create files and directories
for path, files in structure.items():
    Path(path).mkdir(parents=True, exist_ok=True)
    for file in files:
        file_path = Path(path) / file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()  
# Create other root files
root_files = ["docker-compose.yaml", "requirements.txt", "README.md"]
for file in root_files:
    Path(file).touch()

print("✅ Airflow project structure generated!")
