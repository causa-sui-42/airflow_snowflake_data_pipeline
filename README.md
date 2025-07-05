# Airflow + Snowflake data pipeline
**The Goal of the project**: Extract data from a public API or CSV, load it into Snowflake (a staging table), transform it (into a fact/dim model), and validate with Airflow DAGs.

Tools:

 -  Airflow: Orchestration
  
 -  Snowflake: Data warehouse
  
 -  Python: Scripts
  
 -  Docker
  
 -  dbt: (for transformation layer)


**Pipeline architecture**:

             +----------------------+
             |   External Source    |
             |  (CSV/API/Postgres)  |
             +----------+-----------+
                        |
                        v
               (Airflow: Extract Task)
                        |
                        v
             +----------------------+
             |   Staging Table in   |
             |     Snowflake        |
             +----------+-----------+
                        |
                        v
            (Airflow or dbt: Transform)
                        |
                        v
         +------------------------------+
         | Transformed Tables (Facts/Dim)|
         +------------------------------+
                        |
                        v
          (Airflow: Data Quality Check)


**Project structure**:
```

project_root/
├── dags/
│   ├── airflow_snowflake_pipeline.py  # Main DAG: extract users, load to Snowflake, transform
│   └── streaming_pipeline.py          # Streaming DAG: monitor new files, load logs to Snowflake
├── include/
│   └── sql/
│       ├── transform_users.sql             # Clean and format raw user data
│       ├── create_fact_user_activity.sql  # Create fact table from logs
│       └── data_quality_checks.sql        # Null/format checks on key columns
├── plugins/
├── data/
│   ├── users.json                          # Extracted user data from public API
│   └── streaming_logs/
│       ├── log1.json                       # Simulated streaming logs
│       └── log2.json
├── docker-compose.yaml                    # Sets up Airflow locally
├── requirements.txt                       # Includes snowflake-connector-python, pandas, etc.
├── README.md                              # Project overview, architecture diagram, setup instructions
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/
│       │   ├── stg_users.sql               # Load raw users
│       │   └── stg_events.sql              # Load raw events
│       ├── marts/
│       │   ├── dim_users.sql               # Dimension table
│       │   ├── fact_user_activity.sql      # Fact table with user activity counts
│       │   └── user_event_metrics.sql      # Metrics: daily active users, event breakdown
│       └── seeds/
│           └── user_activity.csv           # Optional seed data for testing
└── scripts/
    ├── extract_users.py                   # Extract user data from API
    ├── stream_simulator.py                # Append fake logs to simulate streaming
    └── snowflake_loader.py                # Load JSON/CSV to Snowflake using connector

```

#### Main Airflow DAG (airflow_snowflake_pipeline.py):
- Extract user data from public API
- Save to local file or S3 (for more realism)
- Load into Snowflake staging table
- Run SQL transform into cleaned user model
- Run data quality checks (e.g., no NULL emails)

#### Streaming DAG (streaming_pipeline.py):
- Sensor watches `data/streaming_logs` folder
- Loads new log JSON files to Snowflake
- Transforms logs into fact_user_activity
- Optionally runs dbt models or custom SQL metrics

#### SQL Transforms:
transform_users.sql → uppercases names, removes nulls
create_fact_user_activity.sql → parses streaming logs into rows with user_id, event_type, timestamp
user_event_metrics.sql → counts daily events per type

#### Simulated Stream:
stream_simulator.py appends a JSON log every 30 seconds to `data/streaming_logs/`

#### Snowflake Integration:
- Uses Python scripts to connect and load data
- Or Airflow's `SnowflakeOperator` for SQL
- Credentials stored in Airflow connection UI or in `.env` file

#### dbt:
- Clean transforms as modular models
- Enables documentation and lineage
- dbt can be triggered from Airflow or CLI
