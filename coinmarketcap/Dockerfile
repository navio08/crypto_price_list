FROM python:3.11-slim-buster

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV WEB_HOS=0.0.0.0 WEB_PORT=8081 DEBUG=0
EXPOSE 8081
ENV SERVICE_NAME=coinmarketcap

ENTRYPOINT [ "python3", "main.py" ]