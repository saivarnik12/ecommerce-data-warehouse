FROM apache/airflow:2.10.5-python3.12

USER airflow

COPY data-generator/requirements.txt /tmp/data-requirements.txt
COPY data-generator /opt/airflow/data_generator

RUN pip install --no-cache-dir dbt-core==1.12.3 dbt-postgres==1.11.0 -r /tmp/data-requirements.txt
