FROM python:3.11-slim

WORKDIR /app

COPY ./fetcher/requirements.txt .

COPY ./fetcher/__init__.py .

COPY ./fetcher/main.py .

COPY ./common .

RUN pip3 install -r requirements.txt

CMD python3 -u main.py