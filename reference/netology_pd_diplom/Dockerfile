FROM python:3.9

COPY . /usr/src/app

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip

RUN python -m pip install --no-cache-dir -r requirements.txt

ENTRYPOINT bash run.sh
