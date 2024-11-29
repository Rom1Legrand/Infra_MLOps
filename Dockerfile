# Dockerfile
FROM apache/airflow:2.10.2

# Commencer par root pour les installations système
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Revenir à l'utilisateur airflow pour les installations Python
USER airflow

# Installation des dépendances Python
COPY --chown=airflow:root requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
