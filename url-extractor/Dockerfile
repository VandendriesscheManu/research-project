FROM python:3.11-slim

# Install docker CLI (needed to read logs from other containers)
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_url.py .

RUN chmod +x extract_url.py

# Disable Python output buffering for real-time logs
ENV PYTHONUNBUFFERED=1

CMD ["python", "extract_url.py"]
