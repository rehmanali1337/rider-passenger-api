from datetime import datetime as dt
from random import randint
from app.db import MongoDB


db = MongoDB()


def get_timestamp():
    return dt.now().timestamp()


def get_new_user_id():
    while True:
        new_id = randint(1111111111, 9999999999)
        if not db.get_user_with_id(new_id):
            return new_id


def get_new_ride_id():
    while True:
        new_id = randint(111111111111, 999999999999)
        if not db.get_ride_with_id(new_id):
            return new_id


def string_to_timestamp(time):
    assert isinstance(time, str)
    time_data = time.split('T')[1]
    hour = int(time_data.split(':')[0])
    minute = int(time_data.split(':')[1])
    date_data = time.split('T')[0]
    year = int(date_data.split('-')[0])
    month = int(date_data.split('-')[1])
    day = int(date_data.split('-')[2])
    date_time = dt(year=year, month=month, day=day, hour=hour, minute=minute)
    return int(str(date_time.timestamp()).split('.')[0])
