from datetime import datetime as dt


def string_to_timestamp(time):
    time = '2021-07-23T17:36'
    time_data = time.split('T')[1]
    hour = int(time_data.split(':')[0])
    minute = int(time_data.split(':')[1])
    date_data = time.split('T')[0]
    year = int(date_data.split('-')[0])
    month = int(date_data.split('-')[1])
    day = int(date_data.split('-')[2])
    date_time = dt(year=year, month=month, day=day, hour=hour, minute=minute)
    return int(str(date_time.timestamp()).split('.')[0])


print(string_to_timestamp(''))
