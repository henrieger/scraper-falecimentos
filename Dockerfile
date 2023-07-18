FROM python:3.11-alpine

WORKDIR /app
COPY . .

# RUN apk add --no-cache cron

RUN pip install -r requirements.txt

RUN crontab -l | { cat; echo "0 17 * * * python /app/scraper.py > /results/$(date '+%Y-%m-%d').txt"; }| crontab -

CMD crond -f
