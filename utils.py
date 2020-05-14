import time

class Timer:
    def __init__(self):
        self.start = time.time()

    def reset(self):
        self.start = time.time()

    def measure(self):
        return time.time() - self.start

    def print_elapsed(self):
        print(f'time elapsed = {self.measure()}')