#!/bin/sh
FILENAME=/results/$(date '+%Y-%m-%d_%H-%M').txt
python /app/main.py > $FILENAME
echo "Arquivo $FILENAME criado com sucesso!" >> /logs/scraper.log
