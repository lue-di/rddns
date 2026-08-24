FROM python:3.12.6-slim
LABEL maintainer="luedi <wallisluedi@gmail.com>"

ARG VERSION=unknown

WORKDIR /rddns

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install dependencies in a cacheable layer and avoid .pyc files.
COPY requirements.txt ./
RUN pip install --no-compile -r requirements.txt

# Copy only runtime code. production.json must be mounted at runtime.
COPY main.py logger.py ./
RUN printf '%s\n' "$VERSION" > VERSION

EXPOSE 8181
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8181"]
