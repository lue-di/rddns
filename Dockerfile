FROM python:3.12.6-slim
LABEL maintainer="luedi <wallisluedi@gmail.com>"

ARG VERSION=unknown

WORKDIR /rddns
COPY ./ /rddns/

RUN echo "$VERSION" > /rddns/VERSION && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8181
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8181"]