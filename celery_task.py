from app import celery, db_session
from models import *
from main import book_slot
import time
import datetime
from format import DATE_FORMAT, TIME_FORMAT


@celery.task
def book_slots():
	print("[~] Task started...")

	min_delay = 1
	max_delay = 5
	delay = random.randint(60*min_delay, 60*max_delay)
	print(f"[~] Delaying for {delay} seconds...")
	# time.sleep(delay)

	print("[~] Starting bookings...")
	for user in db_session.query(User).all():
		target_date = datetime.datetime.today() + datetime.timedelta(days=3)
		schedule = db_session.query(Schedule).filter_by(weekday=target_date.weekday()).first()
		if schedule is not None:
			target_date = target_date.strftime(DATE_FORMAT)
			target_time = schedule.target_time.strftime(TIME_FORMAT)

			print(f"[~] Booking for {user.username} at {target_time} {target_date}")
			#book_slot(user.username, user.password, target_date, target_time)