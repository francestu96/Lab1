from collections import deque
from queue import PriorityQueue
from heapq import heappush, heappop
from random import expovariate
import matplotlib.pyplot as plt
import numpy as np  

MAXT = 100000
LAMBDA_values = [0.5, 0.7, 0.9, 0.99]
queue_length = range(0, 15)
w_actual = []
w_attended = []
l_actual = []
l_attended = []

class Arrival:
    def __init__(self, id, LAMBDA):
        self.id = id
        self.LAMBDA = LAMBDA
        self.duration = expovariate(1)

    def process(self, state):
        # * save job arrival time in state.arrivals
        state.arrivals[self.id] = state.t
        # * push the new job arrival in the event queue
        #   (the new event will happen at time t + expovariate(LAMBDA))
        heappush(state.events, (state.t + expovariate(self.LAMBDA), Arrival(self.id + 1, self.LAMBDA)))
        # * if the server FIFO queue is empty, add this job termination
        #   (termination will happen at time t + expovariate(1))
        if state.fifo.qsize() == 0:
            heappush(state.events, (state.t + self.duration, Completion()))
        
        state.fifo.put((self.duration, self.id))

class Completion:
    def process(self, state):
        # remove the first job from the FIFO queue
        _, val = state.fifo.get()
        # update its completion time in state.completions
        state.completions[val] = state.t

        if state.fifo.qsize() > 0:
            heappush(state.events, (state.t + expovariate(1), Completion()))

class QueueCount:
    def process(self, state):
        state.fifo_length.append(state.fifo.qsize())
        heappush(state.events, (state.t + 10, QueueCount()))

class State: 
    def __init__(self, LAMBDA):
        self.t = 0 # current time in simulation
        self.events = [(0, Arrival(0, LAMBDA))] # queue of events to simulate
        self.fifo = PriorityQueue() # queue at the server
        self.fifo_length = [] # queue length at the server
        self.arrivals = {} # jobid -> arrival time mapping
        self.completions = {} # jobid -> completition time mapping

plt.figure(0)
for LAMBDA in LAMBDA_values:
    queue_fractions = []
    state = State(LAMBDA)
    events = state.events

    while events:
        t, event = heappop(events)
        if t > MAXT:
            break
        state.t = t
        event.process(state)

    # process state.arrivals and state.completions, find avarage time spent
    # in the system, and compare it with the theorical value of 1 / (1 - LAMBDA)
    spent_time = 0
    for id in state.completions:
        spent_time += state.completions[id] - state.arrivals[id]

    w_actual.append(spent_time / len(state.completions))
    w_attended.append(1 / (1 - LAMBDA))

    l_actual.append(np.sum(state.fifo_length) / len(state.fifo_length))
    l_attended.append(LAMBDA / (1 - LAMBDA))

    for length in queue_length:
        queue_fractions.append(len([x for x in state.fifo_length if x > length]) / len(state.fifo_length))
    plt.plot(queue_length, queue_fractions, label="λ = " + str(LAMBDA))

plt.xlim(0, 14)
plt.ylim(0, 1.0)
plt.xlabel('Queue length')
plt.ylabel('Fraction of queues with at least that size')
plt.grid()
plt.legend(loc=3, framealpha=0.3)
plt.figure(1)
plt.plot(LAMBDA_values, w_actual, label="Actual W")
plt.plot(LAMBDA_values, w_attended, label="Attended W")
plt.xlabel('LAMBDA')
plt.grid()
plt.legend()
plt.figure(2)
plt.plot(LAMBDA_values, l_actual, label="Actual L")
plt.plot(LAMBDA_values, l_attended, label="Attended L")
plt.xlabel('LAMBDA')
plt.legend()
plt.grid()
plt.plot()
plt.show()