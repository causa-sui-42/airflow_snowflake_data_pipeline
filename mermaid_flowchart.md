flowchart TD
    %% Data Extraction Branch
    subgraph Extraction["Data Extraction Pipeline"]
        API["Public API (users)"] -->|Python| Extract["Airflow Extract Task"]
        Extract -->|JSON| File["users.json"]
        File -->|SnowflakeOperator| Load["Load to Snowflake"]
        Load -->|raw_users| SnowflakeRawDB[("raw_users")]
    end

    %% Transformation Branch
    subgraph Transformation["Transformation Layer"]
        SnowflakeRawDB -->|SQL| Transform["Transform Tables"]
        Transform -->|dbt/models| CleanDB[("clean_users")]
        CleanDB -->|dbt/marts| FactDB[("fact_user_activity")]
    end

    %% Streaming Branch
    subgraph Streaming["Streaming Pipeline"]
        StreamSim["stream_simulator.py"] -->|Append| LogFile["streaming_logs/*.json"]
        LogFile -->|FileSensor| StreamLoad["Streaming DAG"]
        StreamLoad -->|Snowflake| StreamDB[("raw_events")]
    end

    %% Metrics & Downstream
    subgraph Metrics["Metrics Layer"]
        FactDB -->|dbt/marts| MetricsDB["user_event_metrics"]
        StreamDB -->|JOIN| FactDB
    end

    %% Connections Between Subgraphs
    Extraction --> Transformation
    Streaming --> Metrics
    