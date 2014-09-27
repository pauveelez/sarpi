# Broker

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_RESULT_DBURI = 'redis://:password@hostname:port/db_number'
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}


# Schedule

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'every-5-minute': {
        'task': 'tasks.schedule_feed',
        'schedule': crontab(minute='*/5'),
    },
    'every-30-minutes': {
        'task': 'tasks.schedule_fail',
        'schedule': crontab(minute='*/30',),
    },
}

# Cambiar a la zona horaria q necesites
CELERY_TIMEZONE = 'America/Bogota'

