import time as time_m


class Time(object):

    def __init__(self, hours, minutes):
        """
        ** Parameters **
            hours (string)
            minutes (string)
        """
        self.hours = hours
        self.minutes = minutes

    @classmethod
    def fromString(cls, time_str):
        """
        Creates a new tiem from string.
        ** Parameters **
            time (string)
        """
        try:
            date = time_m.strptime(time_str, '%H:%M')
        except Exception as exc:
            raise AttributeError('Invalid time "{}": {}'.format(time_str, exc))
        return cls.fromDate(date)

    @classmethod
    def fromDate(cls, date):
        if hasattr(date, 'time'):
            return cls(date.hour, date.minute)
        return cls(date.tm_hour, date.tm_min)

    def is_before_or_equal(self, other):
        "Checks if this time is before or equal to an other time."
        return self.toInteger() <= other.toInteger()

    def is_after_or_equal(self, other):
        "Checks if this time is after or equal to an other time."
        return self.toInteger() >= other.toInteger()

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def toInteger(self):
        return self.hours * 60 + self.minutes

    def toString(self):
        return "{}:{}".format(self.hours, self.minutes)
