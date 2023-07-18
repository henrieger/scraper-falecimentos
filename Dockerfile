FROM python:3.11-alpine

WORKDIR /app
COPY . .

# RUN apk add --no-cache cron

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PROMETHEUS_PUSHGATEWAY=0.0.0.0:9091
ENV APP_NAME=scraper-falecimentos
ENV CRONTAB_FREQUENCY='0 17 * * *'

RUN crontab -l | { cat; echo "${CRONTAB_FREQUENCY} /app/run.sh"; }| crontab -

CMD crond -f
