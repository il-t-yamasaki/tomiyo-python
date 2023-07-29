FROM python:3.10.10-slim-buster

WORKDIR /app
RUN mkdir src

COPY requirements.txt .
COPY app.py .
COPY src/ src/
COPY templates templates/

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y git

RUN pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn app:app -b 0.0.0.0:8080