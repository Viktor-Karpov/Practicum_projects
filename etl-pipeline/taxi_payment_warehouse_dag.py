from datetime import datetime
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.yandex.operators.dataproc import DataprocCreatePysparkJobOperator

#Задаем переменные
cluster_id = '<cluster-id>'
bucket_name = '<bucket-name>'
bucket_key = 'project_04/taxi_data.parquet'
main_python_file_uri = 's3a://<bucket-name>/<user>/jobs/my_spark_job.py'

#Создадим DAG. За стартовую дату возьмем начало года
with DAG(
    dag_id='taxi_payment_warehouse',
    start_date=datetime(2026, 1, 1),
    schedule='@daily',
    catchup=True
) as dag:
    #Создадим сенсор, который будет проверять создан ли файл раз в 5 минут
    wait_for_file = S3KeySensor(
        task_id='wait_for_taxi',
        bucket_name=bucket_name,
        bucket_key=bucket_key,
        aws_conn_id='s3',
        poke_interval=60 * 5,
        timeout=60**2,
        mode='poke'
    )
    #Запустим spark-скрипт
    run_script = DataprocCreatePysparkJobOperator(
        task_id='run_taxi_warehouse',
        cluster_id=cluster_id,
        main_python_file_uri=main_python_file_uri
    )
    wait_for_file >> run_script
