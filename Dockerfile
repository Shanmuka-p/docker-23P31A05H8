FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .


RUN echo "* * * * * cd /app && /usr/local/bin/python3 scripts/log_2fa_cron.py >> /cron/last_code.txt 2>&1" > /etc/cron.d/2fa-cron && chmod 0644 /etc/cron.d/2fa-cron
RUN crontab /etc/cron.d/2fa-cron
RUN mkdir -p /cron && chmod 755 /cron
RUN mkdir -p /data && chmod 755 /data

ENV SEED_PATH=/data/seed.txt
EXPOSE 8080
CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080