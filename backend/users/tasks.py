from django.shortcuts import get_object_or_404

from backend.celery import app

@app.task
def set_test_coast():
    print('dsa')
