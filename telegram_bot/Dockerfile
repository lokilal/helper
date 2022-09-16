FROM python:3.7-slim

WORKDIR /app

COPY telegram_bot/. .

RUN python3 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir

CMD python3 index.py
