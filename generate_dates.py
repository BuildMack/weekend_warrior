"""
generate_weekends.py

Generates a list of weekend date pairs (Friday to Monday) for a specified number of weeks.
Useful for scheduling or batch-processing flight search queries across future weekends.

Example:
    get_weekend_dates(num_weeks=52)  # Returns 52 (depart, return) date pairs in YYMMDD format
"""

from datetime import datetime, timedelta

def get_weekend_dates(num_weeks=4, today=None):
    if today is None:
        today = datetime.today()
    weekends = []

    for i in range(num_weeks):
        base_day = today + timedelta(weeks=i)
        friday = base_day + timedelta(days=(4 - base_day.weekday()) % 7)
        monday = friday + timedelta(days=3)

        depart = friday.strftime('%y%m%d')
        return_ = monday.strftime('%y%m%d')

        weekends.append((depart, return_))


    return weekends

if __name__ == "__main__":
    get_weekend_dates(num_weeks=52)
