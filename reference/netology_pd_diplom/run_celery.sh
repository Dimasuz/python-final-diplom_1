#!/bin/sh
celery -A netology_pd_diplom worker --loglevel=info --concurrency 1 -E --logfile=logs/celery.log
