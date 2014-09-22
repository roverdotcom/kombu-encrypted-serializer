import os

from celery import Celery
from kombu_encrypted_serializer import setup_encrypted_serializer

TEST_KEY = 'WgFNqB8eokKER0aFxEmfnK7qyZmGhGmxxOqccW3oZoM='
os.environ['KOMBU_ENCRYPTED_SERIALIZER_KEY'] = TEST_KEY

serializer_name = setup_encrypted_serializer(serializer='pickle')

app = Celery('tasks', broker='redis://', backend='redis://')
app.conf.update(
    CELERY_TASK_SERIALIZER=serializer_name,
    CELERY_RESULT_SERIALIZER=serializer_name,
    CELERY_ACCEPT_CONTENT=[serializer_name],
)


@app.task
def add(x, y):
    return x + y


@app.task
def give_it_back(data):
    return data
