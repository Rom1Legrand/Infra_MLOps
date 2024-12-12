# MLOps Infrastructure with Airflow, MLflow, Jenkins & Streamlit

A complete MLOps infrastructure for managing ML model lifecycle with orchestration, experiment tracking, CI/CD, and visualization.

## 📋 Prerequisites

- Docker and Docker Compose
- Git
- AWS account and S3 bucket
- Gmail account (with 2FA authentication enabled)
- NeonDB account (only if choosing NeonDB option for MLflow)

## 🏗️ Architecture and Options

This infrastructure offers two possible configurations for MLflow:

### 1. Local PostgreSQL (Default Configuration)
- MLflow metadata stored in a local PostgreSQL container
- Simple configuration for development and testing
- No external database dependencies
- Ideal for getting started or local development

### 2. NeonDB (Cloud Configuration)
- MLflow metadata stored in a NeonDB database
- Better option for production
- Enables team collaboration
- Requires a NeonDB account

## 🗂️ Project Structure

```
.
├── docker-compose.yml          # Services configuration
├── .env                       # Non-sensitive variables
├── .secrets                   # Sensitive variables (not versioned)
├── Dockerfile                # Main Dockerfile (Airflow)
├── Dockerfile.jenkins        # Jenkins configuration
├── Dockerfile.mlflow         # MLflow configuration
├── Dockerfile.streamlit      # Streamlit configuration
├── requirements.txt          # Airflow requirements
├── requirements.mlflow.txt   # MLflow requirements
├── requirements.streamlit.txt # Streamlit requirements
├── jenkins-requirements-optimized.txt  # Jenkins requirements
├── dags/                     # Airflow DAGs
├── logs/                     # Airflow logs
├── plugins/                  # Airflow plugins
└── streamlit/
    └── app.py               # Streamlit application
```

## ⚙️ Initial Configuration

### 1. S3 Configuration
1. Create an S3 bucket on AWS
2. Create the following folders in the bucket:
   - `mlflow/`: For MLflow artifacts
   - `data/`: For pipeline data
   - `models/`: For deployed models

### 2. Gmail SMTP Configuration
1. Enable two-factor authentication on your Gmail account
2. Generate an app password:
   - Go to Account Settings > Security
   - Select "App passwords"
   - Generate a new password
   - Use this password in EMAIL_PASSWORD in the .secrets file

### 3. Database Configuration

Choose one of the following options:

#### Option 1: Local PostgreSQL (Default)
- No additional configuration required
- In `.env`, ensure option 1 is uncommented:
  ```plaintext
  # Option 1: Local PostgreSQL
  MLFLOW_DB_URL=postgresql://mlflow:mlflow@mlflow-postgres:5432/mlflow
  ```
- In `docker-compose.yml`, ensure:
  - The `mlflow-postgres` service is uncommented
  - The default MLflow configuration is used

#### Option 2: NeonDB
1. Create a NeonDB account
2. Create a new database
3. In `.env`, configure:
   ```plaintext
   # Comment out local PostgreSQL option
   # MLFLOW_DB_URL=postgresql://mlflow:mlflow@mlflow-postgres:5432/mlflow
   
   # Option 2: NeonDB
   NEON_DATABASE_URL=postgresql://user:password@your-neon-db-url/dbname?sslmode=require
   ```
4. In `docker-compose.yml`:
   - Comment out the `mlflow-postgres` service
   - Comment out the default MLflow configuration
   - Uncomment the NeonDB MLflow configuration

## 🔐 Environment Variables Configuration

The project uses two configuration files:

### .env (Non-sensitive variables)
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

# PostgreSQL local (default option1, will be commented out if option 2)
MLFLOW_DB_URL=postgresql://mlflow:mlflow@mlflow-postgres:5432/mlflow

# Database Credentials (used by streamlit and option 2)
NEON_DATABASE_URL=your_neondb_url
```

### .secrets (Sensitive variables - do not version)
```bash
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

## 🚀 Installation and Startup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [your-repo-name]
```

2. Configure environment variables:
```bash
cp .env.example .env
cp .secrets.example .secrets
```

3. Modify `.env` and `.secrets` according to your chosen configuration

4. Start the infrastructure:
```bash
docker-compose build
docker-compose up -d
```

5. Verify all services are operational:
```bash
docker-compose ps
```

## 🌐 Service Access

- Airflow: http://localhost:8080
  - Login: defined in .env/.secrets
- MLflow: http://localhost:5000
  - Login: defined in .env/.secrets
- Jenkins: http://localhost:8088
  - Login: defined in .env/.secrets
- Streamlit: http://localhost:8501

## 🔧 Service Architecture

### Main Services
- **Airflow** (port 8080)
  - ML pipeline orchestration
  - NeonDB and S3 connection
  - SMTP email configuration
  - DAG management
  - Environment variables in .env and .secrets

- **MLflow** (port 5000)
  - Experiment tracking
  - Metric storage in local PostgreSQL or NeonDB depending on configuration
  - Artifact storage in S3
  - Web interface

- **Jenkins** (port 8088)
  - CI/CD for ML models
  - Built-in Python support
  - Preconfigured plugins
  - Drift monitoring

- **Streamlit** (port 8501)
  - Simple user interface
  - Data visualization
  - Single app.py file
  - NeonDB connection

### Auxiliary Services (Airflow)
> Note: These services are part of the standard Airflow configuration and are maintained for potential future use.
- Redis: Message broker for Celery
- Flower (port 5555): Celery monitoring
- Airflow Worker: Celery executor
- Airflow Triggerer: Trigger management

## 📧 Email Configuration

The service uses Gmail SMTP for sending emails:
- Configuration in .env: SMTP_SERVER, SMTP_PORT
- Credentials in .secrets: EMAIL_USER, EMAIL_PASSWORD
- Requires 2FA and Gmail app password

## 🛠️ Maintenance

- Airflow logs in `./logs`
- Jenkins data in `jenkins_home` volume
- Automatic NeonDB backup
- Artifacts on S3
- All services use independent containers with their own requirements

## ⚠️ Important Notes

1. Security:
   - Never commit the .secrets file
   - Change default passwords in production
   - Use secrets manager in production
   - Enable SSL for all connections

2. Dependencies:
   - Requirements are maintained separately for each service
   - Do not modify dependency versions (touchy!) if everything is working
