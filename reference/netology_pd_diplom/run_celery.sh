#!/bin/sh
celery -A netology_pd_diplom worker --loglevel=info --concurrency 1 -E

#celery -A netology_pd_diplom worker -c 1 --loglevel=info --logfile=logs/celery.log