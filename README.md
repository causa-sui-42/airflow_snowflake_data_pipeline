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
