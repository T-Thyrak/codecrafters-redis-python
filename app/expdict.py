class ExpDict:
    def __init__(self):
        self._dict = {}
        
    def set(self, key, value):
        self._dict[key] = value
        
    def get(self, key):
        return self._dict.get(key, None)