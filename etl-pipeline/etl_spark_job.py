#filename=my_spark_job.py
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

#Создали таблицу в ClickHouse
#create table taxi_payment_summary
#(
#    payment_type   String,
#    n_of_rides     UInt64,
#    avg_fare       Float64,
#    avg_tips       Float64,
#    total_income   Float64
#)
#engine = MergeTree()
#order by payment_type;

#Создаем спарк-сессию
spark = (
SparkSession.builder.appName("myAggregateTest")
.config("fs.s3a.endpoint", "storage.yandexcloud.net")
.config("spark.dynamicAllocation.enabled", "false")
.config("spark.executor.instances", "1")
.config("spark.executor.cores", "1")
.config("spark.executor.memory", "1g")
.config("spark.driver.memory", "1g")
.getOrCreate()
)

#Читаем parquet-файл
df = spark.read.parquet('s3a://<bucket-name>/project_04/taxi_data.parquet')

#Создаем витрину данных
data_warehouse_df = df.groupBy('payment_type').agg(
    F.count('*').alias('n_of_rides'),
    F.avg('fare').alias('avg_fare'),
    F.avg('tips').alias('avg_tips'),
    F.sum('trip_total').alias('total_income')
)

#Записываем данные
#Данные подключения к ClickHouse берем из переменных окружения —
#так код безопасно публикуется в репозитории без хардкода секретов
jdbc_host = os.environ['CLICKHOUSE_HOST']
jdbc_user = {
    'user': os.environ['CLICKHOUSE_USER'],
    'password': os.environ['CLICKHOUSE_PASSWORD'],
    'driver': 'com.clickhouse.jdbc.ClickHouseDriver'
}

data_warehouse_df.write.mode('append') \
    .jdbc(url=jdbc_host, table='taxi_payment_summary', properties=jdbc_user)

spark.stop()
