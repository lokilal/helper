FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir && \
    python3 manage.py collectstatic --noinput

CMD python3 manage.py migrate --noinput && \
    gunicorn backend.wsgi:application --bind 0.0.0.0:8000
