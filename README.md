# Infrastructure MLOps avec Airflow, MLflow, Jenkins & Streamlit

Une infrastructure MLOps complète permettant de gérer le cycle de vie des modèles ML avec orchestration, tracking des expériences, CI/CD et visualisation.

## 📋 Prérequis

- Docker et Docker Compose
- Compte NeonDB (base de données PostgreSQL managée)
- Compte AWS et bucket S3
- Compte Gmail pour l'envoi d'emails (avec authentification 2FA activée)
- Git

## 🏗️ Structure du Projet

```
.
├── docker-compose.yml
├── .env                     # Variables non-sensibles
├── .secrets                 # Variables sensibles (non versionné)
├── Dockerfile              # Dockerfile principal (Airflow)
├── Dockerfile.jenkins
├── Dockerfile.mlflow
├── Dockerfile.streamlit
├── requirements.txt           # Requirements Airflow
├── requirements.mlflow.txt
├── requirements.streamlit.txt
├── jenkins-requirements-optimized.txt
├── dags/                     # Dossier pour les DAGs Airflow
├── logs/                     # Logs Airflow
├── plugins/                  # Plugins Airflow
└── streamlit/
    └── app.py               # Application Streamlit (obligatoire)
```

## ⚙️ Configuration Initiale

### 1. Création de Répertoires et fichiers (voir chap Installation et Démarrage)
```bash
répértoire à créer : \dags \logs \plugins \streamlit
fichier ç créer :  app.py
```

### 2. Configuration S3
1. Créer un bucket S3 sur AWS
2. Créer les dossiers suivants dans le bucket:
   - `mlflow/` : Pour les artifacts MLflow
   - `data/` : Pour les données des pipelines
   - `models/` : Pour les modèles déployés

### 3. Configuration Gmail pour SMTP
1. Activer l'authentification 2 facteurs sur votre compte Gmail
2. Générer un mot de passe d'application:
   - Aller dans Paramètres du compte > Sécurité
   - Sélectionner "Mots de passe des applications"
   - Générer un nouveau mot de passe
   - Utiliser ce mot de passe dans EMAIL_PASSWORD du fichier .secrets

### 4. Configuration NeonDB
1. Créer un compte sur NeonDB
2. Créer une nouvelle base de données
3. Récupérer l'URL de connexion pour le fichier .secrets

## 🔐 Configuration des Variables d'Environnement

Le projet utilise deux fichiers de configuration :

### .env (Variables non-sensibles)
```bash
# System Configuration
AIRFLOW_UID=50000

# Service URLs & Ports
AIRFLOW_API_URL=http://airflow-webserver:8080
MLFLOW_TRACKING_URI=http://mlflow:5000
JENKINS_URL=http://jenkins:8080
JENKINS_OPTS="--prefix=/jenkins"
JENKINS_HOME=/var/jenkins_home

# Email Server Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# S3 Configuration
S3_BUCKET=your_bucket_name

# Service Default Users
AIRFLOW_USERNAME=admin
JENKINS_ADMIN_ID=admin
MLFLOW_TRACKING_USERNAME=admin

# MLflow Configuration
MLFLOW_DEFAULT_ARTIFACT_ROOT=s3://${S3_BUCKET}/mlflow/
```

### .secrets (Variables sensibles - ne pas versionner)
```bash
# Database Credentials
NEON_DATABASE_URL=your_neondb_url

# AWS Credentials
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# Email Credentials
EMAIL_USER=your.email@gmail.com
EMAIL_PASSWORD=your_app_password

# Service Passwords
AIRFLOW_PASSWORD=your_password
MLFLOW_TRACKING_PASSWORD=your_password
JENKINS_ADMIN_PASSWORD=your_password
```

## 🚀 Installation et Démarrage

1. Cloner le repository :
```bash
git clone [your-repo-url]
cd [your-repo-name]
```

2. Créer les répertoires et fichiers nécessaires :
```bash
mkdir -p dags logs plugins streamlit
touch streamlit/app.py
```

3. Configurer les variables d'environnement :
- Copier `.env.example` vers `.env` et remplir les valeurs
- Copier `.secrets.example` vers `.secrets` et remplir les valeurs sensibles
- S'assurer que `.secrets` est dans `.gitignore`

4. Construire et démarrer les services :
```bash
docker-compose build
docker-compose up -d
```

## 🌐 Accès aux Services

- Airflow : http://localhost:8080
  - Login : défini dans .env/.secrets
- MLflow : http://localhost:5000
  - Login : défini dans .env/.secrets
- Jenkins : http://localhost:8088
  - Login : défini dans .env/.secrets
- Streamlit : http://localhost:8501

## 🔧 Architecture des Services

### Services Principaux
- **Airflow** (port 8080)
  - Orchestration des pipelines ML
  - Connexion à NeonDB et S3
  - Configuration email SMTP
  - Gestion des DAGs
  - Variables d'environnement dans .env et .secrets

- **MLflow** (port 5000)
  - Tracking des expériences
  - Stockage des métriques dans NeonDB
  - Stockage des artifacts dans S3
  - Interface web sécurisée

- **Jenkins** (port 8088)
  - CI/CD pour les modèles ML
  - Support Python intégré
  - Plugins préconfigurés
  - Monitoring des drifts

- **Streamlit** (port 8501)
  - Interface utilisateur simple
  - Un seul fichier app.py
  - Connexion à NeonDB

### Services Auxiliaires (Airflow)
> Note : Ces services font partie de la configuration standard d'Airflow et sont maintenus pour une potentielle utilisation future.
- Redis : Message broker pour Celery
- Flower (port 5555) : Monitoring Celery
- Airflow Worker : Exécuteur Celery
- Airflow Triggerer : Gestion des déclencheurs

## 📧 Configuration Email

Le service utilise Gmail SMTP pour l'envoi d'emails :
- Configuration dans .env : SMTP_SERVER, SMTP_PORT
- Credentials dans .secrets : EMAIL_USER, EMAIL_PASSWORD
- Nécessite l'authentification 2FA et un mot de passe d'application Gmail

## 🛠️ Maintenance

- Logs Airflow dans `./logs`
- Données Jenkins dans volume `jenkins_home`
- Backup automatique NeonDB
- Artifacts sur S3
- Tous les services utilisent des conteneurs indépendants avec leurs propres requirements

## ⚠️ Notes Importantes

1. Sécurité :
   - Ne jamais commiter le fichier .secrets
   - Changer les mots de passe par défaut en production
   - Utiliser des secrets manager en production
   - Activer SSL pour toutes les connexions

2. Dépendances :
   - Les requirements sont maintenus séparément pour chaque service
   - Ne pas modifier les versions des dépendances (touchy!) si tout fonctionne
