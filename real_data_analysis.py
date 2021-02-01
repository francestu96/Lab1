from collections import deque
from heapq import heappush, heappop
import matplotlib.pyplot as plt
from random import expovariate, randint
import csv
from datetime import datetime

QUEUE_LENGTH = range(0, 15)

class Arrival:
    def __init__(self, id):
        self.id = id
    def __lt__(self, other):
        return True

    def process(self, state):
        state.arrivals[self.id] = state.t  
        state.server_queue.append(self.id)

class Completion:
    def __lt__(self, other):
        return True

    def process(self, state):
        if state.server_queue:
            val = state.server_queue.popleft()
            state.completions[val] = state.t

class QueueCount:
    def __lt__(self, other):
        return True

    def process(self, state):
        state.server_queue_length.append(len(state.server_queue))
        if len(state.events) > 3:
            heappush(state.events, (state.t + 50, QueueCount()))

class State: 
    def __init__(self, start_time, end_time):
        self.t = start_time
        self.server_queue = deque()
        self.server_queue_length = []
        self.arrivals = {}
        self.completions = {} 
        self.events = [(start_time, Arrival(0)), (end_time, Completion()), (start_time + 50, QueueCount())]


state = None

with open('real_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for i, row in enumerate(reader):
        if row[0]:
            start_time = datetime.strptime('-'.join(row[0].split('-')[:-1]), '%Y-%m-%d %H:%M:%S').timestamp()
            end_time = datetime.strptime('-'.join(row[1].split('-')[:-1]), '%Y-%m-%d %H:%M:%S').timestamp()
            if not state:
                state = State(start_time, end_time)
            else:
                heappush(state.events, (start_time, Arrival(i)))
                heappush(state.events, (end_time, Completion()))


while state.events:
    t, event = heappop(state.events)
    state.t = t
    event.process(state)

spent_time = 0
for id in state.completions:
    spent_time += state.completions[id] - state.arrivals[id]

expected_lambda = len(state.completions) / spent_time

queue_fractions = []
for length in QUEUE_LENGTH:
    value = 0
    value += len([x for x in state.server_queue_length if x > length]) / len(state.server_queue_length)
    queue_fractions.append(value / len(state.server_queue_length))

plt.plot(QUEUE_LENGTH, queue_fractions, label="Expected λ = {:.5f}".format(expected_lambda))

plt.xlim(0, 14)
plt.xlabel('Queue Length')
plt.ylabel('Fraction of queues with at least that size')
plt.grid()
plt.legend()  
plt.show()