from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    dag_id='tweet_data_pipeline',
    default_args=default_args,
    schedule_interval='@hourly',  # You can change this
    catchup=False
)

DATA_PATH = '/opt/airflow/data/streamed_tweets.csv'  # Mount this later

def ingest():
    df = pd.read_csv(DATA_PATH)
    df.to_csv('/opt/airflow/data/ingested.csv', index=False)

def clean():
    df = pd.read_csv('/opt/airflow/data/ingested.csv')

    # Drop missing values
    df.dropna(inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Remove outlier (fake date)
    df = df[df['created_at'] != '9999-99-99T99:99:99']

    df.to_csv('/opt/airflow/data/cleaned.csv', index=False)

def aggregate():
    df = pd.read_csv('/opt/airflow/data/cleaned.csv')
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    daily_count = df.groupby(df['created_at'].dt.date).size().reset_index(name='tweet_count')
    daily_count.to_csv('/opt/airflow/data/daily_summary.csv', index=False)

def feature_engineering():
    df = pd.read_csv('/opt/airflow/data/cleaned.csv')
    df['tweet_length'] = df['text'].apply(len)
    df['word_count'] = df['text'].apply(lambda x: len(x.split()))
    df.to_csv('/opt/airflow/data/featured.csv', index=False)

t1 = PythonOperator(task_id='ingest', python_callable=ingest, dag=dag)
t2 = PythonOperator(task_id='clean', python_callable=clean, dag=dag)
t3 = PythonOperator(task_id='aggregate', python_callable=aggregate, dag=dag)
t4 = PythonOperator(task_id='feature_engineering', python_callable=feature_engineering, dag=dag)

t1 >> t2 >> t3 >> t4
