from generate_dates import get_weekend_dates
from datetime import datetime, timedelta
import random

def get_random_date_for_weekday(weekday, year=2025):
    while True:
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # keep it simple
        try:
            candidate = datetime(year, month, day)
            if candidate.weekday() == weekday:
                return candidate
        except:
            continue

def test_weekday(weekday_name, weekday_index):
    test_date = get_random_date_for_weekday(weekday_index)
    weekends = get_weekend_dates(1, today=test_date)
    depart_str, return_str = weekends[0]

    depart = datetime.strptime(depart_str, '%y%m%d')
    return_ = datetime.strptime(return_str, '%y%m%d')

    print(f"Test Starting Date ({weekday_name}): {test_date.strftime('%Y-%m-%d (%A)')}")
    print(f"Depart: {depart.strftime('%Y-%m-%d (%A)')}")
    print(f"Return: {return_.strftime('%Y-%m-%d (%A)')}")

    assert depart.weekday() in [3, 4], f"Departure is not Thu/Fri"
    assert return_.weekday() == 0, f"Return is not Monday"
    print(f"{weekday_name} test passed!\n")

def test_monday():    test_weekday("Monday", 0)
def test_tuesday():   test_weekday("Tuesday", 1)
def test_wednesday(): test_weekday("Wednesday", 2)
def test_thursday():  test_weekday("Thursday", 3)
def test_friday():    test_weekday("Friday", 4)
def test_saturday():  test_weekday("Saturday", 5)
def test_sunday():    test_weekday("Sunday", 6)
