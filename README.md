# Apache Airflow Installation Guide (VM Deployment)

This repository documents the installation and configuration of **Apache Airflow** on a Linux VM environment without Docker.

The setup uses:

- PostgreSQL as metadata database
- Redis as Celery broker
- CeleryExecutor for distributed task execution
- systemd for service management

### Install System Dependencies
```
sudo apt update
sudo apt install python3-pip python3-venv redis-server postgresql
```

### Create Airflow Home Directory
```
mkdir -p /home/ddi/airflow
echo 'export AIRFLOW_HOME=/home/ddi/airflow' >> ~/.bashrc
source ~/.bashrc
```
### Install Apache Airflow (Using Constraints)
```
export AIRFLOW_VERSION=2.9.3
export PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
```
```
pip install "apache-airflow[celery,postgres,redis]==${AIRFLOW_VERSION}" \
--constraint "${CONSTRAINT_URL}"
```
### config Airflow.cfg
```
[core]

dags_folder = /home/ddi/airflow/dags
executor = CeleryExecutor
load_examples = False
default_timezone = Asia/Jakarta

[database]

sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost:5432/airflow
load_default_connections = True

[celery]

broker_url = redis://127.0.0.1:6379/0
result_backend = db+postgresql://airflow:airflow@localhost:5432/airflow
worker_concurrency = 8
task_acks_late = True
worker_prefetch_multiplier = 1
```
