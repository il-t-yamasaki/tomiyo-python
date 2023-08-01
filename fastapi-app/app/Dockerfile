FROM python:3.10.10-slim-buster

WORKDIR /app
RUN mkdir src

COPY requirements.txt .

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y git

RUN pip install -r requirements.txt
RUN pip install mysql-connector-python

#EXPOSE 80
#CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "80"]