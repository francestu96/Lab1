from collections import deque
from heapq import heappush, heappop
from random import expovariate, randint

class Arrival:
    def __init__(self, id, LAMBDA, queue_index, is_supermarket, is_sjf):
        self.LAMBDA = LAMBDA
        self.queue_index = queue_index
        self.id = id
        self.is_supermarket = is_supermarket
        self.is_sjf = is_sjf
        self.duration = expovariate(1)

    def process(self, state):
        state.arrivals[self.id] = state.t

        queue_index = [len(x) for x in state.server_queue].index(min([len(x) for x in state.server_queue])) if self.is_supermarket else randint(0, len(state.server_queue) - 1)
        heappush(state.events, (state.t + expovariate(self.LAMBDA), Arrival(self.id + 1, self.LAMBDA, queue_index, self.is_supermarket, self.is_sjf)))

        if not state.server_queue[self.queue_index]:
            heappush(state.events, (state.t + self.duration, Completion(self.queue_index)))
            
        heappush(state.server_queue[self.queue_index], (self.duration, self.id)) if self.is_sjf else state.server_queue[self.queue_index].append(self.id)

class Completion:
    def __init__(self, queue_index):
        self.queue_index = queue_index

    def process(self, state):
        state.serving_event[self.queue_index] += 1
        event = state.serving_event[self.queue_index]
        state.completions[event] = state.t
        if type(state.server_queue[self.queue_index]) is deque:
            state.server_queue[self.queue_index] = deque([x for x in state.server_queue[self.queue_index] if x != event])
        else:
            state.server_queue[self.queue_index] = [x for x in state.server_queue[self.queue_index] if x[1] != event]

        if len(state.server_queue[self.queue_index]) > 0:
            heappush(state.events, (state.t + expovariate(1), Completion(self.queue_index)))

class QueueCount:
    def process(self, state):
        for i in range(len(state.server_queue)):
            state.server_queue_length[i].append(len(state.server_queue[i]))
        heappush(state.events, (state.t + 10, QueueCount()))

class State: 
    def __init__(self, LAMBDA, server_no, is_supermarket, is_sjf):
        self.t = 0
        self.server_queue = [([] if is_sjf else deque()) for x in range(server_no)]
        self.server_queue_length = [[] for x in range(server_no)]
        self.serving_event = [-1 for x in range(server_no)]
        self.arrivals = {}
        self.completions = {} 

        self.events = [(0, Arrival(0, LAMBDA, 0, is_supermarket, is_sjf)), (10, QueueCount())] # queue of events to simulate
