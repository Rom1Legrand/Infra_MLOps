from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mlflow

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def test_mlflow_connection():
    mlflow.set_tracking_uri("http://mlflow:5000")
    
    with mlflow.start_run(experiment_id="0") as run:
        mlflow.log_param("source", "airflow_test")
        mlflow.log_metric("test_value", 100)
        print(f"MLflow run ID: {run.info.run_id}")
        
    return "MLflow connection test successful"

dag = DAG(
    'test_mlflow_connection',
    default_args=default_args,
    description='Test DAG for MLflow connection',
    schedule_interval=None,
)

test_task = PythonOperator(
    task_id='test_mlflow_connection',
    python_callable=test_mlflow_connection,
    dag=dag,
)
