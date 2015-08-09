class DateTimeStorage(object):

    def __init__(self):
        self._cache = {}

    def attach(self, item):
        self.items[self.get_hash(item)] = item

    def get_hash(self, obj):
        return obj.strftime('%Y-%m-%d')

    def contains(self, value):
        key = self.get_hash(value)
        return key in self._cache
