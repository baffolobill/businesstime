import datetime
import copy


class DateTimePeriod(object):

    def __init__(self, start_date, end_date):
        c_end_date = copy.copy(end_date)
        c_end_date += datetime.timedelta(days=1)
        if start_date > c_end_date:
            raise ValueError('Start date must be earlier than end date.')
        self.current_date = copy.copy(start_date)
        self.end_date = c_end_date

    def __iter__(self):
        return self

    def next(self):
        if self.current_date < self.end_date:
            curr = copy.copy(self.current_date)
            self.current_date += datetime.timedelta(days=1)
            return curr
        else:
            raise StopIteration()
