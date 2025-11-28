# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install local python dependencies
COPY ./models ./models/
RUN pip install --no-cache-dir -e ./models/

# Install other python dependencies
COPY ./master_server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./master_server ./master_server/

# install curl for healthchecks
RUN apt update && apt install -y curl

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "master_server.master_api:app"]
CMD ["fastapi", "run", "--port", "8000", "master_server/master_api.py"]
