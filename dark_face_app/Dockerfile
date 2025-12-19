# Base image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN pip install uv

WORKDIR /app

# Copy requirements first to leverage cache
COPY requirements.txt .

# Install dependencies using uv
# --system installs into the system python environment (no venv needed in container)
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY . .

# Expose Gradio port
# Expose Gradio port (dev mode uses 7861 by default in dev.py logic, but typically 7860/7861)
# Checking dev.py/mcp_interface.py defaults: dev.py kills 7861. mcp_interface launches on 7861.
EXPOSE 7861

# Command to run the app in dev mode
CMD ["python", "dev.py"]
