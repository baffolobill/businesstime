import copy
import datetime
try:
    import cPickle as pickle
except ImportError:
    import pickle

from holidays import Holidays
from days import Days
from time_cls import Time
from util import next_weekday


class Business(object):
    CLOSEST_LAST = 0
    CLOSEST_NEXT = 1

    def __init__(self, days, holidays=None, timezone=None):
        if isinstance(holidays, (list, tuple)):
            holidays = Holidays(holidays)
        elif not holidays:
            holidays = Holidays()
        elif isinstance(holidays, Holidays):
            raise ValueError('The holidays parameter must be an array of \DateTime objects, an instance of Business\Holidays or null.')

        self.set_days(days)
        self.holidays = holidays
        self.timezone = timezone

    def closest(self, date, mode=CLOSEST_NEXT):
        tmp_date = copy.copy(date)
        if self.CLOSEST_LAST == mode:
            return self.get_closest_date_before(tmp_date)
        return self.get_closest_date_after(tmp_date)

    def within(self, date):
        tmp_date = copy.copy(date)
        if self.holidays.is_holiday(tmp_date):
            day = self.get_day(tmp_date.isoweekday())
            if day is not None:
                return day.is_time_within_opening_hours(Time.fromDate(tmp_date), tmp_date)
        return False

    def timeline(self, start, end, interval):
        if start >= end:
            raise ValueError('The start date must be before the end date.')
        tmp_start = copy.copy(start)
        tmp_end = copy.copy(end)
        dates = []
        last_date = tmp_start
        while True:
            date = self.get_closest_date_after(last_date)
            if date > tmp_end:
                break
            dates.append(date)
            last_date += datetime.timedelta(days=interval)
        return dates

    def timedelta(self, start, end):
        """
        Returns a datetime.timedelta with the number of full business days
        and business time between d1 and d2
        """
        time = datetime.timedelta()
        if start >= end:
            return time

        # within the same day
        if start.date() == end.date():
            if self.holidays.is_holiday(start):
                return time

            day_of_week = start.isoweekday()
            day = self.get_day(day_of_week)
            # we doesn't work at `start` date (may be it's Sat or Sun)
            if day is None:
                return time
            start_time = Time.fromDate(start)
            end_time = Time.fromDate(end)
            time = day.timedelta(start_time, end_time)
        else:
            dates = []
            if end.date() - start.date() == datetime.timedelta(days=1):
                start_day = self.get_day(start.isoweekday())
                end_day = self.get_day(end.isoweekday())
                dates = [
                    [start, Time.fromDate(start), start_day.get_closing_time(start)],
                    [end, end_day.get_opening_time(end), Time.fromDate(end)],
                ]
            else:
                start_day = self.get_day(start.isoweekday())
                end_day = self.get_day(end.isoweekday())
                dates = [
                    [start, Time.fromDate(start), start_day.get_closing_time(start)],
                    [end, end_day.get_opening_time(end), Time.fromDate(end)],
                ]
                last_date = start
                while True:
                    date = self.get_closest_date_after(last_date)
                    if date.date() >= end.date():
                        break
                    day = self.get_day(date.isoweekday())
                    dates.append([date, day.get_opening_time(date), day.get_closing_time(date)])
                    last_date += datetime.timedelta(days=1)

            for date, start_time, end_time in dates:
                if self.holidays.is_holiday(date):
                    continue
                day_of_week = date.isoweekday()
                day = self.get_day(day_of_week)
                # we doesn't work at `date` day (may be it's Sat or Sun)
                if day is None:
                    continue
                time += day.timedelta(start_time, end_time)

        return time

    def serialize(self):
        return pickle.dumps([self.days, self.holidays, self.timezone], 2)

    def unserialize(self, serialized):
        data = pickle.loads(serialized)
        self.days = data[0]
        self.holidays = data[1]
        self.timezone = data[2]

    def get_closest_date_before(self, date):
        tmp_date = copy.copy(date)
        day_of_week = tmp_date.isoweekday()
        time = Time.fromDate(tmp_date)
        if self.holidays.is_holiday(tmp_date):
            day = self.get_day(day_of_week)
            if day is not None:
                closest_time = day.get_closest_opening_time_before(time, tmp_date)
                if closest_time is not None:
                    return tmp_date.replace(hour=closest_time.get_hours(), minute=closest_time.get_minutes())
        tmp_date = self.get_date_before(tmp_date)
        while self.holidays.is_holiday(tmp_date):
            tmp_date = self.get_date_before(tmp_date)
        closest_day = self.get_closest_day_before(tmp_date.isoweekday())
        closing_time = closest_day.get_closing_time(tmp_date)
        return tmp_date.replace(hour=closing_time.get_hours(), minute=closing_time.get_minutes())

    def get_date_before(self, date):
        tmp_date = copy.copy(date)
        tmp_date -= datetime.timedelta(days=1)
        day_of_week = tmp_date.isoweekday()
        closest_day = self.get_closest_day_before(day_of_week)
        if closest_day.get_day_of_week() != day_of_week:
            #php: $tmpDate->modify(sprintf('last %s', Days::toString($closestDay->getDayOfWeek())));
            tmp_date = prev_weekday(tmp_date, closest_day.get_day_of_week())
        return tmp_date

    def get_closest_date_after(self, date):
        tmp_date = copy.copy(date)
        day_of_week = tmp_date.isoweekday()
        time = Time.fromDate(tmp_date)
        if self.holidays.is_holiday(tmp_date):
            day = self.get_day(day_of_week)
            if day is not None:
                closest_time = day.get_closest_opening_time_after(time, tmp_date)
                if closest_time is not None:
                    return tmp_date.replace(hour=closest_time.get_hours(), minute=closest_time.get_minutes())
        tmp_date = self.get_date_after(tmp_date)
        while self.holidays.is_holiday(tmp_date):
            tmp_date = self.get_date_after(tmp_date)
        closest_day = self.get_closest_day_before(tmp_date.isoweekday())
        closing_time = closest_day.get_opening_time(tmp_date)
        return tmp_date.replace(hour=closing_time.get_hours(), minute=closing_time.get_minutes())

    def get_date_after(self, date):
        tmp_date = copy.copy(date)
        tmp_date += datetime.timedelta(days=1)
        day_of_week = tmp_date.isoweekday()
        closest_day = self.get_closest_day_after(day_of_week)
        if closest_day.get_day_of_week() != day_of_week:
            #php: $tmpDate->modify(sprintf('next %s', Days::toString($closestDay->getDayOfWeek())));
            tmp_date = next_weekday(tmp_date, closest_day.get_day_of_week())
        return tmp_date

    def get_closest_day_before(self, day_number):
        day = self.get_day(day_number)
        if day is not None:
            return day
        return self.get_day_before(day_number)

    def get_closest_day_after(self, day_number):
        day = self.get_day(day_number)
        if day is not None:
            return day
        return self.get_day_after(day_number)

    def get_day_before(self, day_number):
        tmp_day_number = day_number
        for i in xrange(0, 6):
            if tmp_day_number == Days.MONDAY:
                tmp_day_number = Days.SUNDAY
            else:
                tmp_day_number -= 1
            day = self.get_day(tmp_day_number)
            if day is not None:
                return day
        return self.get_day(day_number)

    def get_day_after(self, day_number):
        tmp_day_number = day_number
        for i in xrange(0, 6):
            if Days.SUNDAY == tmp_day_number:
                tmp_day_number = Days.MONDAY
            else:
                tmp_day_number += 1
            day = self.get_day(tmp_day_number)
            if day is not None:
                return day
        return self.get_day(day_number)

    def get_day(self, day_number):
        return self.days.get(day_number)

    def add_day(self, day):
        self.days[day.get_day_of_week()] = day

    def set_days(self, days):
        self.days = {}
        for day in days:
            self.add_day(day)
