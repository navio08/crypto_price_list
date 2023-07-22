FROM python:3.11-slim-buster

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV WEB_HOS=0.0.0.0 WEB_PORT=8080 DEBUG=0
EXPOSE 8080
ENV SERVICE_NAME=fortrisapp

ENTRYPOINT [ "python3", "main.py" ]