# Imagen base de Python
FROM python:3.8-slim-buster

# Configuración de variables de entorno
ENV AIRFLOW_HOME=/airflow
ENV PYTHONPATH=/airflow

# Instalación de dependencias
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    python3-dev \
    python3-pip && \
    pip install --upgrade pip setuptools wheel && \
    pip install apache-airflow==2.1.4 psycopg2-binary && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configuración de la base de datos
RUN airflow db init

# Exposición del puerto
EXPOSE 8080

# Comando para iniciar Apache Airflow
CMD ["airflow", "webserver"]
