from events import Arrival, Completion, QueueCount, State
from heapq import heappop
import matplotlib.pyplot as plt
import sys, getopt
import math
import utils

MAXT = 100000
LAMBDA_VALUES = [0.5, 0.7, 0.9, 0.95, 0.99]
SERVER_NO = [1, 2, 5, 10]
QUEUE_LENGTH = range(0, 15)

def main(argv):
    is_overload = True
    is_supermarket = True
    is_sjf = True
    opts, _ = getopt.getopt(argv, "h", ["supermarket=","overload=","sjf=","help"])
    for opt, arg in opts:
        if opt == "-h" or opt == "--help":
            print("usage: queue_simulator.py --supermarket=True(Default) --overload=True(Default) --sjf=True(Default)")
            print("Supermarket decide if the new arrivals choose the shortest or a random queue")
            print("Overload scales the work demand based on the number of queues")
            print("SJF (Shortest Job First) set if the queue is SJF or FIFO")
            sys.exit()
        elif opt == ("--supermarket"):
            is_supermarket = arg == "True"
        elif opt in ("--overload"):
            is_overload = arg == "True"
        elif opt in ("--sjf"):
            is_sjf = arg == "True"

    fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(9,4.5))
    fig.text(0.5, 0.04, 'LAMBDA', ha='center')
    fig.text(0.04, 0.5, 'Value', va='center', rotation='vertical')
    fig2, ax2 = plt.subplots(math.ceil(len(SERVER_NO) / 2), math.ceil(len(SERVER_NO) / 2), sharex=True, sharey=True, figsize=(9,9))
    fig2.text(0.5, 0.04, 'Queue length', ha='center')
    fig2.text(0.04, 0.5, 'Fraction of queues with at least that size', va='center', rotation='vertical')
    for idx_server, server_no in enumerate(SERVER_NO):
        w_actual = []
        w_theorical = []
        l_actual = []
        l_theorical = []

        for LAMBDA in LAMBDA_VALUES:
            state = State(LAMBDA * server_no if is_overload else LAMBDA, server_no, is_supermarket, is_sjf)
            events = state.events

            while events:
                t, event = heappop(events)
                if t > MAXT:
                    break
                state.t = t
                event.process(state)

            w, x, y, z = utils.processData(state.arrivals, state.completions, state.server_queue_length, LAMBDA)
            w_actual.append(w)
            w_theorical.append(x)        
            l_actual.append(y)
            l_theorical.append(z)

            utils.plotQueueLength(idx_server, ax2, QUEUE_LENGTH, state.server_queue_length, LAMBDA, server_no)
        
        if server_no == 1:
            utils.plotTheoricalData(ax, w_actual, w_theorical, l_actual, l_theorical, LAMBDA_VALUES)

    plt.show()

if __name__ == "__main__":
   main(sys.argv[1:])