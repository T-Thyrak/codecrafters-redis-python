import time

class ExpDict:
    def __init__(self):
        self._dict = {}
        
    def set(self, key, value, px=None):
        self._dict[key] = (value, px / 1000 + round(time.time(), 3) if px is not None else None)
        print(self._dict[key])
        
    def get(self, key):
        thing = self._dict.get(key)
        if thing is None:
            return None

        if thing[1] is None:
            return thing[0]
        
        if thing[1] > round(time.time(), 3):
            print(thing[1] - round(time.time(), 3))
            return thing[0]
        
        del self._dict[key]
        return None
        
        