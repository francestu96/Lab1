import numpy as np  

def processData(arrivals, completions, server_queue_length, LAMBDA):
    spent_time = 0
    for id in completions:
        spent_time += completions[id] - arrivals[id]

    w_actual = spent_time / len(completions)
    w_attended = 1 / (1 - LAMBDA)

    l_actual = 0
    for queue_length in server_queue_length:
        l_actual += np.sum(queue_length) / len(queue_length)
    l_actual /= len(server_queue_length)
    l_attended = LAMBDA / (1 - LAMBDA)
    
    return [w_actual, w_attended, l_actual, l_attended]

def plotQueueLength(idx, ax, queue_length, server_queue_length, lambda_value, server_no):
    queue_fractions = []
    for length in queue_length:
        value = 0
        for queue in server_queue_length:
            value += len([x for x in queue if x > length]) / len(queue)
        queue_fractions.append(value / len(server_queue_length))
    
    x = int("{:02b}".format(idx)[0])
    y = int("{:02b}".format(idx)[1])
    ax[x][y].plot(queue_length, queue_fractions, label="λ = " + str(lambda_value))
    ax[x][y].title.set_text(str(server_no) + " choise/s")
    ax[x][y].set_xlim(0, 14)
    ax[x][y].set_xlim(0, 14)
    ax[x][y].grid()
    ax[x][y].legend()  

def plotTheoricalData(ax, w_actual, w_attended, l_actual, l_attended, lambda_values):
    ax[0].title.set_text('Avarage Time Spent')
    ax[0].plot(lambda_values, w_actual, label="Actual W")
    ax[0].plot(lambda_values, w_attended, label="Theorical W")
    ax[0].set_xlim(0.5, 1.0)
    ax[0].grid()
    ax[0].legend()
    ax[1].title.set_text('Avarage Queue Length')
    ax[1].plot(lambda_values, l_actual, label="Actual L")
    ax[1].plot(lambda_values, l_attended, label="Theorical L")
    ax[1].set_xlim(0.5, 1.0)
    ax[1].grid()
    ax[1].legend()    