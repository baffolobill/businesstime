from time_cls import Time


class TimeInterval(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        if start.is_after_or_equal(end):
            raise AttributeError('The opening time "{}" must be before the closing time "{}".'.format(start.toString(), end.toString()))

    @classmethod
    def fromString(cls, start_time, end_time):
        return cls(Time.fromString(start_time), Time.fromString(end_time))

    def contains(self, time):
        return self.start.is_before_or_equal(time) \
            and self.end.is_after_or_equal(time)

    def getEnd(self):
        return self.end

    def getStart(self):
        return self.start
