import datetime

from time_interval import TimeInterval


class AbstractDay(object):

    def __init__(self, day_of_week, opening_intervals):
        """
        ** Parameters **
            day_of_week (integer)
                The day of week
            opening_intervals (list)
                The opening intervals
        """
        self.set_day_of_week(day_of_week)
        self.set_opening_intervals(opening_intervals)

    def get_day_of_week(self):
        return self.day_of_week

    def timedelta(self, start_time, end_time):
        time = datetime.timedelta()
        st_int = start_time.toInteger()
        en_int = end_time.toInteger()
        for opening_interval in self.opening_intervals:
            i_start = opening_interval.getStart().toInteger()
            i_end = opening_interval.getEnd().toInteger()

            # both values in the same interval
            # |---*---*---|
            #     \+++/
            if st_int >= i_start and st_int <= i_end and \
               en_int >= i_start and en_int <= i_end:
                time = datetime.timedelta(minutes=en_int - st_int)
                break

            # start_time in the interval, not end_time
            # |---*---|  #########
            #     \+++|
            elif st_int >= i_start and st_int <= i_end:
                time += datetime.timedelta(minutes=i_end - st_int)

            # end_time in the interval, not start_time
            # #########  |---*---|
            #            |+++/
            elif en_int >= i_start and en_int <= i_end:
                time += datetime.timedelta(minutes=en_int - i_start)

            # entire interval between start_time and end_time
            # |---*---|  |------|  |---*---|
            #     \+++|  |++++++|  |+++/
            elif st_int <= i_start and i_end <= en_int:
                time += datetime.timedelta(minutes=i_end - i_start)

            else:
                # Another cases:
                # 1) ->  -*--|-------|  <- start_time before first interval
                # 2) ->  |-------|--*--|-------|  <- start_time/end_time between intervals
                # 3) ->  |-------|-*-*-|-------|  <- start_time and end_time between intervals
                # 4) ->  |-------|--*-  <- end_time after intervals
                # 5) ->  |-------|-*-*-  <- start_time and end_time after intervals
                # 6) ->  -*--|-----|  |-----|--*-  <- start_time before first interval and end_time after last interval
                #raise Exception('Unsolved case.')
                continue
        return time

    def get_closest_opening_time_before(self, time, context):
        for opening_interval in self.opening_intervals:
            if opening_interval.contains(time):
                return time
        closest_time = None
        for interval in reversed(self.opening_intervals):
            distance = time.toInteger() - interval.getEnd().toInteger()
            if distance < 0:
                continue
            if closest_time is None:
                closest_time = interval.getEnd()
            if distance < time.toInteger() - closest_time.toInteger():
                closest_time = interval.getEnd()
        return closest_time

    def get_closest_opening_time_after(self, time, context):
        for opening_interval in self.opening_intervals:
            if opening_interval.contains(time):
                return time
        closest_time = None
        for interval in self.opening_intervals:
            distance = interval.getStart().toInteger() - time.toInteger()
            if distance < 0:
                continue
            if closest_time is None:
                closest_time = interval.getStart()
            if distance < closest_time.toInteger() - time.toInteger():
                closest_time = interval.getStart()
        return closest_time

    def is_time_within_opening_hours(self, time, context):
        for interval in self.opening_intervals:
            if interval.contains(time):
                return True
        return False

    def get_opening_time(self, context):
        return self.opening_intervals[0].getStart()

    def get_closing_time(self, context):
        return self.opening_intervals[-1].getEnd()

    def set_day_of_week(self, day_of_week):
        self.day_of_week = day_of_week

    def set_opening_intervals(self, opening_intervals):
        if not opening_intervals:
            raise ValueError('The day must have at least one opening interval.')
        self.opening_intervals = []
        for opening_interval in opening_intervals:
            if not isinstance(opening_interval, (list, tuple)):
                raise ValueError('Interval must be a list.')
            if len(opening_interval) != 2:
                raise ValueError('Each interval must be an array containing opening and closing times.')
            self.opening_intervals.append(TimeInterval.fromString(opening_interval[0], opening_interval[1]))
        sorted(self.opening_intervals, key=lambda interval: interval.getStart())
