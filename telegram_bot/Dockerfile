FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip && \
    pip3 install -r telegram_bot/requirements.txt --no-cache-dir

CMD python3 telegram_bot/index.py
