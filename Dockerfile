# FROM --platform=linux/amd64 python:3.11-slim-bookworm
FROM --platform=linux/amd64 python:3.12-slim as build_amd64

ENV PIP_DEFAULT_TIMEOUT=100 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1

RUN mkdir /asteroidmining
WORKDIR /asteroidmining
COPY requirements.txt /asteroidmining

RUN set -ex \
    # Create a non-root user
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    # Upgrade the package index and install security upgrades
    && apt-get update -y \
    && apt-get upgrade -y \
    # Install dependencies
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*  
      

# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
COPY main.py /asteroidmining
COPY imagegen.py /asteroidmining
COPY /templates /asteroidmining/templates/
COPY /static/favicon.ico /asteroidmining/static/favicon.ico
EXPOSE 8000
ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000"]
# CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000