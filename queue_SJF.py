from heapq import heappush, heappop
import matplotlib.pyplot as plt
from random import expovariate, randint

MAXT = 1000000
LAMBDA_VALUES = [0.5, 0.7, 0.9, 0.95, 0.99]
QUEUE_LENGTH = range(0, 15)

class Arrival:
    def __init__(self, id, LAMBDA):
        self.id = id
        self.LAMBDA = LAMBDA
        self.duration = expovariate(1)

    def process(self, state):
        state.arrivals[self.id] = state.t
        heappush(state.events, (state.t + expovariate(self.LAMBDA), Arrival(self.id + 1, LAMBDA)))

        if len(state.server_queue) == 0:
            heappush(state.events, (state.t + self.duration, Completion()))
        
        heappush(state.server_queue, (self.duration, self.id))

class Completion:
    def process(self, state):
        state.serving_event += 1
        event = state.serving_event
        state.completions[event] = state.t
        state.server_queue = [x for x in state.server_queue if x[1] != event]

        if len(state.server_queue) > 0:
            heappush(state.events, (state.t + expovariate(1), Completion()))

class QueueCount:
    def process(self, state):
        state.server_queue_length.append(len(state.server_queue))
        heappush(state.events, (state.t + 10, QueueCount()))

class State: 
    def __init__(self, LAMBDA):
        self.t = 0
        self.server_queue = []
        self.server_queue_length = []
        self.serving_event = -1
        self.arrivals = {}
        self.completions = {} 

        self.events = [(0, Arrival(0, LAMBDA)), (10, QueueCount())]

for LAMBDA in LAMBDA_VALUES:
    state = State(LAMBDA)
    events = state.events
    
    while events:
        t, event = heappop(events)
        if t > MAXT:
            break
        state.t = t
        event.process(state)
        
    queue_fractions = []
    for length in QUEUE_LENGTH:
        value = 0
        value += len([x for x in state.server_queue_length if x > length])
        queue_fractions.append(value / len(state.server_queue_length))

    plt.plot(QUEUE_LENGTH, queue_fractions, label="λ = " + str(LAMBDA))

plt.xlim(0, 14)
plt.ylim(0, 1)
plt.xlabel('Queue Length')
plt.ylabel('Fraction of queues with at least that size')
plt.grid()
plt.legend()  
plt.show()