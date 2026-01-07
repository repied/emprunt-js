# Simple devcontainer for the Emprunt project
FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.11

# Create a non-root user and workdir are already handled by the base image
WORKDIR /workspace

# Install project requirements
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

# Install Google Cloud CLI
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg curl && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && apt-get install -y google-cloud-cli

# Optional: keep image small by cleaning cache
RUN pip cache purge || true && apt-get clean && rm -rf /var/lib/apt/lists/*
