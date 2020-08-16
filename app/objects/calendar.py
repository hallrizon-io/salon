from datetime import date, timedelta, datetime
from calendar import monthrange


class Calendar:
    @staticmethod
    def get_week_dates(year, week):
        week_start = datetime.strptime(f'{year}-W{week}' + '-1', "%G-W%V-%u")
        week_end = week_start + timedelta(days=6)
        return [week_start, week_end]

    @staticmethod
    def get_month_dates(year, month):
        num_days = monthrange(year, month)[1]
        first_day = date(year, month, 1)
        last_day = date(year, month, num_days)
        return [first_day, last_day]
