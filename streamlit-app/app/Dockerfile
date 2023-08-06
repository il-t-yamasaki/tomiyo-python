FROM python:3.10.10-slim-buster

WORKDIR /app

COPY requirements.txt .
#COPY main.py .
#COPY src/ src/

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y git

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

EXPOSE 8080
CMD streamlit run main.py \
    --browser.serverAddress="0.0.0.0" \
    --server.port="8080"