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
