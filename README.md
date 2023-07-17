# Scraper do Obituário de Curitiba

> Certifique-se de ter alguma versão instalada do Python 3 na sua máquina!

Para instalar os pacotes necessários, navegue até o diretório do repositório e rode
```sh
./init.sh
```

Para executar o software, execute
```sh
python3 scraper.py
```
ou
```sh
./run.sh
```
para executar em ambiente virtual com arquivo de saída definido.

É possível gerar um cronjob diário, executado às 17h, com o seguinte formato:
```cron
0 17 * * *
```
