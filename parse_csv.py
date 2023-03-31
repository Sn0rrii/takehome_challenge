import csv
import re
from datetime import datetime
from app import crud, database, models

DAYS_OF_WEEK = ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

MINUTES_IN_DAY = 1440
MINUTES_IN_WEEK = 10080


def parse_csv(csv_file):

    db = next(database.get_db())

    with open(csv_file, 'r') as f:

        reader = csv.reader(f)

        next(reader)

        # Create a restaurant and operating time records for each row
        for row in reader:
            db_restaurant = crud.create_restaurant(db, row[0], row[1])

            operating_time_ranges = get_operating_minute_ranges(db_restaurant.id, row[1])

            crud.create_operating_time_ranges(db, operating_time_ranges)


def get_operating_minute_ranges(restaurant_id, op_hours):

    times = []

    for op_hours_range in op_hours.split(' / '):

        time_ranges = to_minute_range(restaurant_id, op_hours_range)

        times.extend(time_ranges)

    return times


def to_minute_range(restaurant_id, op_hours):

    day_string, time_string = split_days_and_time_range(op_hours)

    days = get_days_as_integer_list(day_string)

    start, end = parse_start_and_end_time(time_string)

    spans_next_day = start > end

    open_ranges = []

    for day in days:
        operating_time = models.OperatingTime(restaurant_id=restaurant_id)

        # Get startng minute
        operating_time.start_min = day * MINUTES_IN_DAY + (start.hour * 60) + start.minute

        # Get ending minute
        if not spans_next_day:
            end_time = day * MINUTES_IN_DAY + (end.hour * 60) + end.minute
        else:
            end_time = (day + 1) * MINUTES_IN_DAY + (end.hour * 60) + end.minute

            if end_time > MINUTES_IN_WEEK:
                addl_entry_end_time = end_time - MINUTES_IN_WEEK
                open_ranges.append(
                    models.OperatingTime(
                        restaurant_id=restaurant_id,
                        start_min=0,
                        end_min=addl_entry_end_time
                    )
                )
                end_time = MINUTES_IN_WEEK
        operating_time.end_min = end_time

        open_ranges.append(operating_time)

    return open_ranges


def parse_start_and_end_time(time_range_string):
    time_strings = time_range_string.split(' - ')
    times = []
    for time in time_strings:
        time = time.strip()
        try:
            time_obj = datetime.strptime(time, '%I:%M %p')
        except ValueError:
            time_obj = datetime.strptime(time, '%I %p')
        times.append(time_obj)

    return times


def split_days_and_time_range(op_hours):
    m = re.search(r'\d+', op_hours)
    time_idx = m.start()
    days_string = op_hours[:time_idx]
    hours_string = op_hours[time_idx:]

    return days_string, hours_string


def get_days_as_integer_list(days_string):
    days = days_string.split(',')

    day_integers = set()

    for d in days:
        if '-' in d:
            day_integers.update(enumerate_day_range(d))
        else:
            day_integers.add(DAYS_OF_WEEK.index(d.strip()))

    return day_integers


def enumerate_day_range(day_string_range):
    start, end = day_string_range.split('-')
    return list(
        range(
            DAYS_OF_WEEK.index(start.strip()),
            DAYS_OF_WEEK.index(end.strip()) + 1
        )
    )


if __name__ == "__main__":
    parse_csv('challenge/restaurants.csv')
