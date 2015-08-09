try:
    import cPickle as pickle
except ImportError:
    import pickle

from abstract_day import AbstractDay


class SpecialDay(AbstractDay):

    def __init__(self, day_of_week, opening_intervals_evaluator):
        self.set_day_of_week(day_of_week)
        self.opening_intervals_evaluator = opening_intervals_evaluator

    def get_closest_opening_time_before(self, time, context):
        self.evaluate_opening_intervals(context)
        return super(SpecialDay, self).get_closest_opening_time_before(time, context)

    def get_closest_opening_time_after(self, time, context):
        self.evaluate_opening_intervals(context)
        return super(SpecialDay, self).get_closest_opening_time_after(time, context)

    def is_time_within_opening_hours(self, time, context):
        self.evaluate_opening_intervals(context)
        return super(SpecialDay, self).is_time_within_opening_hours(time, context)

    def get_opening_time(self, context):
        self.evaluate_opening_intervals(context)
        return super(SpecialDay, self).get_opening_time(context)

    def get_closing_time(self, context):
        self.evaluate_opening_intervals(context)
        return super(SpecialDay, self).get_closing_time(context)

    def evaluate_opening_intervals(self, context):
        pass

    def serialize(self):
        data = [
            self.day_of_week,
            self.opening_intervals_cache,
            self.opening_intervals_evaluator,
        ]
        return pickle.dumps(data, 2)

    def unserialize(self, serialized):
        data = pickle.loads(serialized)
        self.day_of_week = data[0]
        self.opening_intervals_cache = data[1]
        self.opening_intervals_evaluator = data[2]
