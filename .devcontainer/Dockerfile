FROM python:3.10-slim

# Tools & Dependencies für Dev
RUN apt-get update && apt-get install -y \
    curl iputils-ping git vim less \
    && apt-get clean

# Arbeitsverzeichnis
WORKDIR /workspace

# Optional: vorab requirements kopieren (für Caching)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files for development
COPY app/ ./app/