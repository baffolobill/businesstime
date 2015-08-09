try:
    import cPickle as pickle
except ImportError:
    import pickle

from datetime_storage import DateTimeStorage
from datetime_period import DateTimePeriod


class Holidays(object):

    def __init__(self, holidays=None):
        self.holidays = DateTimeStorage()
        self.add_holidays(holidays or [])

    def is_holiday(self, date):
        return self.holidays.contains(date)

    def serialize(self):
        return pickle.dumps(self.holidays, 2)

    def unserialize(self, serialized):
        self.holidays = pickle.loads(serialized)

    def add_holiday(self, holiday):
        self.holidays[holiday.strftime('%Y-%m-%d')] = holiday

    def add_holidays(self, holidays):
        for holiday in holidays:
            if isinstance(holiday, DateTimePeriod):
                self.add_holidays(holiday)
                continue
            self.holidays.attach(holiday)
