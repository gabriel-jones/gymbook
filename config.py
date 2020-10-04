import os
import datetime
from decouple import config
from celery.schedules import crontab


class Config(object):
	BOOKING_LIVE = config('BOOKING_LIVE', cast=bool, default=False)

	REDIS_URL = config('REDIS_URL')
	CELERY_BROKER_URL = REDIS_URL
	CELERY_RESULT_BACKEND = REDIS_URL

	SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')

	CELERYBEAT_SCHEDULE = {
		'book-slots': {
			'task': 'celery_task.book_slots',
			'schedule': crontab(minute=9, hour=8)
		}
	}

	TIMEZONE = config('TZ', default='Europe/London')
	CELERY_TIMEZONE = TIMEZONE
