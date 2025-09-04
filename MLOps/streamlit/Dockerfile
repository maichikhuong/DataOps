# Use Python 3.11 base image
FROM python:3.11-slim

# Set working directory
WORKDIR /streamlit

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application code
COPY . .

# Expose the application port
EXPOSE 8501

# Command to start Streamlit application
CMD ["streamlit", "run", "streamlit_mlmodel.py", "--server.port=8501", "--server.enableCORS=false"]
