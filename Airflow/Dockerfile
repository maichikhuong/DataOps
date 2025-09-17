# Use Airflow 2.8.4
FROM apache/airflow:2.10.0-python3.11

# Set working directory
WORKDIR /opt/airflow

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt