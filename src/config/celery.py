from celery import Celery
from config.settings.base import ENV_PATH
from dotenv import load_dotenv

load_dotenv(ENV_PATH)

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
