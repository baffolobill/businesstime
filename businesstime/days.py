class Days(object):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    strings = {
        MONDAY: 'Monday',
        TUESDAY: 'Tuesday',
        WEDNESDAY: 'Wednesday',
        THURSDAY: 'Thursday',
        FRIDAY: 'Friday',
        SATURDAY: 'Saturday',
        SUNDAY: 'Sunday'
    }

    @classmethod
    def toString(cls, day_of_week):
        return cls.strings.get(day_of_week)

    @classmethod
    def toArray(cls):
        return [cls.MONDAY, cls.TUESDAY, cls.WEDNESDAY, cls.THURSDAY, cls.FRIDAY, cls.SATURDAY, cls.SUNDAY]
