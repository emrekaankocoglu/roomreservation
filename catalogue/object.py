from threading import Lock, Condition
import pickle

class Object:
    def __init__(self):
        self.lock = Lock()
        self.updated = Condition()
    
    def critical(func):
        def wrapper(self, *args, **kwargs):
            with self.lock:
                return func(self, *args, **kwargs)
        return wrapper
    
    def notify(func):
        def wrapper(self, *args, **kwargs):
            with self.updated:
                func(self, *args, **kwargs)
                self.updated.notify_all()
        return wrapper

    def save(self):
        with open(self.__class__.__name__ + ".pickle", "wb") as f:
            pickle.dump(self, f)
    
    @staticmethod        
    def load(file):
        with open(file, "rb") as f:
            return pickle.load(f)
        
    def __str__(self) -> str:
        d = self.__dict__.copy()
        del d["lock"]
        del d["updated"]
        return self.__class__.__name__ + ": " + str(d)
    def __repr__(self) -> str:
        d = self.__dict__.copy()
        del d["lock"]
        del d["updated"]
        return self.__class__.__name__ + ": " + str(d)
    def __getstate__(self):
        state = self.__dict__.copy()
        del state["lock"]
        del state["updated"]
        return state
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = Lock()
        self.updated = Condition()
    