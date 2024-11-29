from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def test_jenkins_connection():
    jenkins_url = "http://jenkins:8080"
    jenkins_user = "xxxx"  # Remplacez par votre utilisateur Jenkins
    jenkins_password = "xxxx"  # Remplacez par votre mot de passe Jenkins
    
    try:
        # Test basique de connexion
        response = requests.get(
            f"{jenkins_url}/api/json",
            auth=HTTPBasicAuth(jenkins_user, jenkins_password),
            verify=False
        )
        
        if response.status_code == 200:
            print("Connexion à Jenkins réussie!")
            jenkins_info = response.json()
            print(f"Version de Jenkins: {jenkins_info.get('version', 'Non disponible')}")
            print(f"Nombre de jobs: {len(jenkins_info.get('jobs', []))}")
            return "Connexion Jenkins réussie"
        else:
            print(f"Erreur de connexion: {response.status_code}")
            print(f"Réponse: {response.text}")
            raise Exception(f"Échec de la connexion à Jenkins: {response.status_code}")
            
    except Exception as e:
        print(f"Erreur lors de la connexion à Jenkins: {str(e)}")
        raise

dag = DAG(
    'test_jenkins_connection',
    default_args=default_args,
    description='Test DAG pour la connexion Jenkins',
    schedule_interval=None,
)

test_task = PythonOperator(
    task_id='test_jenkins_connection',
    python_callable=test_jenkins_connection,
    dag=dag,
)
