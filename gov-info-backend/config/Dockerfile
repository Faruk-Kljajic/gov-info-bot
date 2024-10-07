# Python-Image
FROM python:3.9-slim

# Set Workdirectory in Container
WORKDIR /app

# Copy requirements
COPY ../requirements/requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy Code in to WORKDIR
COPY .. .

# Expose Port 8000 for Uvicorn
EXPOSE 8000

# Start FastAPI-App with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
