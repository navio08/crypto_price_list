FROM python:3.11-slim-buster

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV WEB_PORT=8080 DEBUG=0
ENV HOST_COINMARKET=coinmarketcap HOST_CRYPTORANK=crytporank
EXPOSE 8080
ENV WEB_HOST=fortrisapp

ENTRYPOINT [ "opentelemetry-instrument", "python3", "main.py" ]