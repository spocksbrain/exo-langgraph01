# Dockerfile for the exo multi-agent system

# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade npm
RUN npm install -g npm@latest

# Copy requirements file
COPY exo/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the exo package
COPY exo/ exo/
COPY prompts/ prompts/
COPY run.py .
COPY .env.example .

# Create necessary directories
RUN mkdir -p data/vector_db data/neo4j logs

# Install the exo package
RUN pip install -e .

# Create a non-root user
RUN useradd -m exouser
RUN chown -R exouser:exouser /app
USER exouser

# Copy the .env.example to .env if .env doesn't exist
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Expose ports
EXPOSE 8000 8001 3000

# Set entrypoint
ENTRYPOINT ["python", "run.py"]

# Set default command
CMD ["--interface", "all"]
