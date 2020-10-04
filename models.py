from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from format import TIME_FORMAT
import calendar


Base = declarative_base()


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False, index=False, unique=True)
	password = Column(String, nullable=False, index=False, unique=True)

	name = Column(String, nullable=False, index=False, unique=False)
	schedules = relationship('Schedule', back_populates='user')

	def __str__(self):
		return f"<User #{self.id} {self.username} for {self.name}>"


class Schedule(Base):
	__tablename__ = 'schedules'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	user = relationship('User', back_populates='schedules')

	weekday = Column(Integer, nullable=False, index=True, unique=False)
	target_time = Column(Time, nullable=False, index=False, unique=False)

	def __str__(self):
		return f"<Schedule #{self.id} user {self.user} day {calendar.day_name[self.weekday]} at {self.target_time.strftime(TIME_FORMAT)}>"
