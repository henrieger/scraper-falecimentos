import scraper
from os import getenv
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway

registry = CollectorRegistry()
gateway = getenv('PROMETHEUS_PUSHGATEWAY', 'localhost:9091')
job_name = getenv('APP_NAME', 'scraper-falecimentos')

last_success = Gauge('job_last_success_unixtime', 'Last time a job successfully finished', registry=registry)
time_elapsed = Gauge('job_main_time_elapsed', 'Total amount of time elapsed in the main function', registry=registry)
http_status = Counter('job_requests_http_status', 'Counts of status request in job', ['endpoint', 'status'], registry=registry)

if __name__ == '__main__':
    with time_elapsed.time():
        status_code = scraper.main()
    http_status.labels('https://obituarios.curitiba.pr.gov.br/publico/falecimentos.aspx', status_code).inc()
    last_success.set_to_current_time()
    push_to_gateway(gateway, job=job_name, registry=registry)
