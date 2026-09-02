from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="ecommerce_warehouse_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["ecommerce", "dbt", "warehouse"],
) as dag:
    generate_source_data = BashOperator(
        task_id="generate_source_data",
        bash_command="python /opt/data-generator/generate_data.py",
    )
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/dbt && dbt run --profiles-dir .",
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/dbt && dbt test --profiles-dir .",
    )
    log_pipeline_summary = BashOperator(
        task_id="log_pipeline_summary",
        bash_command="echo 'E-commerce warehouse pipeline completed successfully.'",
    )
    generate_source_data >> dbt_run >> dbt_test >> log_pipeline_summary
