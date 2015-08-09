try:
    import cPickle as pickle
except ImportError:
    import pickle

from abstract_day import AbstractDay


class Day(AbstractDay):

    def serialize(self):
        return pickle.dumps([self.day_of_week, self.opening_intervals], 2)

    def unserialize(self, serialized):
        data = pickle.loads(serialized)
        self.day_of_week = data[0]
        self.opening_intervals = data[1]
