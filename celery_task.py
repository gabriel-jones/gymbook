from app import celery, db_session
from models import *
from main import book_slot
import time
import datetime
import random
from config import Config
from format import DATE_FORMAT, TIME_FORMAT
from sqlalchemy.sql.expression import func


@celery.task
def book_slots():
	print("[~] Starting bookings...")
	for user in db_session.query(User).order_by(func.random()).all():
		min_delay = 0
		max_delay = 2
		delay = random.randint(60*min_delay, 60*max_delay)
		print(f"[~] Delaying for {delay} seconds...")
		time.sleep(delay)
		print("[~] Delay finished")
		target_date = datetime.datetime.today() + datetime.timedelta(days=3)
		schedules = db_session.query(Schedule).filter_by(weekday=target_date.weekday())
		print(f"[~] Booking {schedules.count()} slots...")
		for schedule in schedules.all():
			target_date = target_date.strftime(DATE_FORMAT)
			target_time = schedule.target_time.strftime(TIME_FORMAT)

			print(f"[~] Booking for {user.username} at {target_time} {target_date}")
			if Config.BOOKING_LIVE:
				book_slot(user.username, user.password, target_date, target_time)
				reservation = Reservation()
				reservation.schedule = schedule
				db_session.add(reservation)
				db_session.commit()