import argparse
from queue import LifoQueue, PriorityQueue, Queue
import threading
from random import choice, randint
from time import sleep
from itertools import zip_longest

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel

QUEUE_TYPES = {
    "fifo" : Queue,
    "lifo" : LifoQueue,
    "heap" : PriorityQueue
}

def main(args):
    buffer = QUEUE_TYPES[args.queue]()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("q", "--queue", choices = QUEUE_TYPES, default = "fifo")
    parser.add_argument("-p", "--producers", type = int, default = 3)
    parser.add_argument("-c", "--consumers", type = int, default = 2)
    parser.add_argument("-ps", "--producers-speed", type = int, default = 1)
    parser.add_argument("-cs", "--consumers-speed", type = int, default = 1) 
    return parser.parse_args()

if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt:
        pass

PRODUCTS = (
    ":balloon:",
    ":cookie:",
    ":crystal_ball:",
    ":diving_mask:",
    ":flashlight:",
    ":gem:",
    ":gift:",
    ":kite:",
    ":party_popper:",
    ":postal_horn:",
    ":ribbon:",
    ":rocket:",
    ":teddy_bear:",
    ":thread:",
    ":yo-yo:",
)

class Worker(threading.Thread):
    def __init__(self, speed, buffer):
        super().__init__(daemon=True)
        self.speed = speed
        self.buffer = buffer
        self.product = None
        self.working = False
        self.progress = 0
    
    @property
    def state(self):
        if self.working:
            return f"{self.product} ({self.progress}%)"
    
    def simulateidle(self):
        self.product = None
        self.working = False
        self.progress = 0
        sleep(randint(1,3))
    
    def simulatework(self):
        self.working = True
        self. progress = 0
        delay = randint(1,  1 + 15 // self.speed)
        for _ in range(100):
            sleep(delay / 100)
            self.progress += 1

class View:
    def __init__(self, buffer, producers, consumers):
        self.buffer = buffer
        self.producers = producers
        self.consumers = consumers

    def animate(self):
        with Live(
            self.render(), screen = True, refresh_per_second=10
        ) as live:
            while True:
                live.update(self.render())

    def render(self):
        match self.buffer:
            case PriorityQueue():
                title = "Priority Queue"
                products = map(str, reversed(list(self.buffer.queue)))
            case LifoQueue():
                title = "Stack"
                products = list(self.buffer.queue)
            case Queue():
                title = "Queue"
                products = reversed(list(self.buffer.queue))

class Producer(Worker):
    def __init__(self, speed, buffer, products):
        super().__init__(speed, buffer)
        self.products = products
    
    def run(self):
        self.product = choice(self.products)
        self.simulatework()
        self.buffer.put(self.product)
        self.simulateidle()
class Consumer(Worker):
    def run(self):
        while True:
            self.product = self.buffer.get()
            self.simulatework()
            self.buffer.task_done()
            self.simulateidle()