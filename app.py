from config import Config
from redis import Redis
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print("[~] Creating database session...")
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
db_session = Session()
print("[*] Database session created")

print("[~] Creating celery worker and redis instance...")
redis = Redis.from_url(Config.REDIS_URL) if Config.REDIS_URL else None
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
celery.config_from_object(Config)
print("[*] Celery and redis setup")

from models import *
from celery_task import *