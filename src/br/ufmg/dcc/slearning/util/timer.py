import time

class Timer:    
    def start(self):
        self.start = time.clock()
        return self

    def end(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start