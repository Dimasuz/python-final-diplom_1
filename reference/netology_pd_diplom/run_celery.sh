#!/bin/sh

celery --app=netology_pd_diplom worker --loglevel=DEBUG --concurrency=2 -E --logfile=logs/celery.log

exec "$@"
