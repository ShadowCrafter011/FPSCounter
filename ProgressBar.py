from multiprocessing import Value, Process
from time import sleep
import sys

green = "\033[92m"
blue = "\033[94m"
bold = "\033[1m"
normal = "\033[0m"


class PBar:
    @classmethod
    def new(cls, length, total, refresh_rate=5):
        shared_value = Value("i", 0)
        progress_bar = PBar(length, total, refresh_rate, shared_value)
        return shared_value, progress_bar

    def __init__(self, length, total, refresh, shared_value):
        self.length = length
        self.total = total
        self.progress = shared_value
        self.completed = False
        self.refresh = refresh
        self.update()

        Process(target=self.update_loop).start()

    def update_loop(self):
        while self.progress.value <= self.total and not self.completed:
            self.update()
            sleep(self.refresh)

    def update(self):
        done = int(self.progress.value / self.total * self.length)
        p_bar = f"{blue}[{green}{'=' * done}{blue}{'-' * (self.length - done)}]"
        percentage = str(round(self.progress.value / self.total * 100, 2))
        sys.stdout.write(f"\r{p_bar} {bold}{percentage}%{normal}")

        if self.progress.value == self.total:
            self.completed = True
            self.progress.value = -1
            print(f"\n{green}Done!{normal}")

    def wait_complete(self):
        while not self.progress.value == -1:
            sleep(.1)
