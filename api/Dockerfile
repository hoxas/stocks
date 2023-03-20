FROM python:3.11-slim

WORKDIR /app

COPY ./api .

COPY ./common .

RUN pip3 install -r requirements.txt

CMD python3 -u main.py