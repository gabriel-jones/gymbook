import argparse
from app import db_session
from models import *
from format import TIME_FORMAT
from datetime import datetime, time
from celery_task import book_slots


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title="commands", dest="command")
	
parser_db = subparsers.add_parser('db_create')

parser_book = subparsers.add_parser('book')

parser_add_user = subparsers.add_parser("add_user")
parser_add_user.add_argument('-u', '--username', dest='_username')
parser_add_user.add_argument('-p', '--password', dest='_password')
parser_add_user.add_argument('-n', '--name', dest='_name')

parser_schedule = subparsers.add_parser("schedule")
parser_schedule.add_argument('-i', '--uid', dest='_uid')
parser_schedule.add_argument('-w', '--weekday', dest='_weekday')
parser_schedule.add_argument('-t', '--time', dest='_time')

args = parser.parse_args()

if args.command == 'db_create':
	from models import Base
	from app import engine
	print("[~] Creating database...")
	Base.metadata.create_all(engine)
	print("[*] Database created")
if args.command == 'book':
	print("[~] Manual booking start...")
	book_slots.delay()
elif args.command == 'add_user':
	user = User()
	user.username = args._username
	user.password = args._password
	user.name = args._name

	print("[~] Creating user...")
	db_session.add(user)
	db_session.commit()
	print(f"[*] Added user {user}")
elif args.command == 'schedule':
	schedule = Schedule()
	schedule.user_id = args._uid
	schedule.weekday = args._weekday
	schedule.target_time = datetime.strptime(args._time, '%I:%M %p').time()

	print("[~] Creating schedule...")
	db_session.add(schedule)
	db_session.commit()
	print(f"[*] Added schedule {schedule}")
