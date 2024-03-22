import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')

# Create a Celery instance.
app = Celery('diplom')

# Configure Celery using the settings from Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app modules.
app.autodiscover_tasks()