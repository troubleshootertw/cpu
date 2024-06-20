# Define NULLPCB
NULLPCB = {
    'process_id': 0,
    'arrival_timestamp': 0,
    'total_bursttime': 0,
    'execution_starttime': 0,
    'execution_endtime': 0,
    'remaining_bursttime': 0,
    'process_priority': 0
}

def handle_process_arrival_pp(ready_queue, current_process, new_process, timestamp):
    # If there is no currently running process
    if current_process == NULLPCB:
        # Set execution start time, end time, and remaining burst time for the new process
        new_process['execution_starttime'] = timestamp
        new_process['execution_endtime'] = timestamp + new_process['total_bursttime']
        new_process['remaining_bursttime'] = new_process['total_bursttime']
        return new_process
    else:
        # If there is a currently running process, compare priorities
        if new_process['process_priority'] <= current_process['process_priority']:
            # Add the new process to the ready queue
            ready_queue.append(new_process)
            return current_process
        else:
            # Add the current process to the ready queue and switch to the new process
            ready_queue.append(current_process)
            current_process['execution_endtime'] = 0
            current_process['remaining_bursttime'] -= (timestamp - current_process['execution_starttime'])
            return new_process

def handle_process_completion_pp(ready_queue, timestamp):
    # If the ready queue is empty
    if not ready_queue:
        return NULLPCB
    else:
        # Find the process with the highest priority
        highest_priority_process = min(ready_queue, key=lambda x: x['process_priority'])
        # Remove the process from the ready queue
        ready_queue.remove(highest_priority_process)
        # Update execution start and end times
        highest_priority_process['execution_starttime'] = timestamp
        highest_priority_process['execution_endtime'] = timestamp + highest_priority_process['remaining_bursttime']
        return highest_priority_process

def handle_process_arrival_srtp(ready_queue, current_process, new_process, timestamp):
    # If there is no currently running process
    if current_process == NULLPCB:
        # Set execution start time, end time, and remaining burst time for the new process
        new_process['execution_starttime'] = timestamp
        new_process['execution_endtime'] = timestamp + new_process['total_bursttime']
        new_process['remaining_bursttime'] = new_process['total_bursttime']
        return new_process
    else:
        # If there is a currently running process, compare remaining burst times
        if new_process['total_bursttime'] >= current_process['remaining_bursttime']:
            # Add the new process to the ready queue
            ready_queue.append(new_process)
            return current_process
        else:
            # Add the current process to the ready queue and switch to the new process
            ready_queue.append(current_process)
            current_process['execution_starttime'] = 0
            current_process['execution_endtime'] = 0
            current_process['remaining_bursttime'] -= (timestamp - current_process['execution_starttime'])
            return new_process

def handle_process_completion_srtp(ready_queue, timestamp):
    # If the ready queue is empty
    if not ready_queue:
        return NULLPCB
    else:
        # Find the process with the shortest remaining burst time
        shortest_remaining_time_process = min(ready_queue, key=lambda x: x['remaining_bursttime'])
        # Remove the process from the ready queue
        ready_queue.remove(shortest_remaining_time_process)
        # Update execution start and end times
        shortest_remaining_time_process['execution_starttime'] = timestamp
        shortest_remaining_time_process['execution_endtime'] = timestamp + shortest_remaining_time_process['remaining_bursttime']
        return shortest_remaining_time_process

def handle_process_arrival_rr(ready_queue, current_process, new_process, timestamp, time_quantum):
    # If there is no currently running process
    if current_process == NULLPCB:
        # Set execution start time, end time, and remaining burst time for the new process
        new_process['execution_starttime'] = timestamp
        new_process['execution_endtime'] = timestamp + min(time_quantum, new_process['total_bursttime'])
        new_process['remaining_bursttime'] = new_process['total_bursttime']
        return new_process
    else:
        # If there is a currently running process, add the new process to the ready queue
        ready_queue.append(new_process)
        return current_process

def handle_process_completion_rr(ready_queue, timestamp, time_quantum):
    # If the ready queue is empty
    if not ready_queue:
        return NULLPCB
    else:
        # Get the process with the earliest arrival time from the ready queue
        next_process = ready_queue.pop(0)
        # Update execution start and end times
        next_process['execution_starttime'] = timestamp
        next_process['execution_endtime'] = timestamp + min(time_quantum, next_process['remaining_bursttime'])
        return next_process

# Example usage:
ready_queue = []
current_process = NULLPCB
new_process = {
    'process_id': 2,
    'arrival_timestamp': 2,
    'total_bursttime': 6,
    'execution_starttime': 0,
    'execution_endtime': 0,
    'remaining_bursttime': 6,
    'process_priority': 0
}
timestamp = 2
time_quantum = 6

# Testing Priority-based Preemptive Scheduling
current_process = handle_process_arrival_pp(ready_queue, current_process, new_process, timestamp)
print("Current Process:", current_process)
current_process = handle_process_completion_pp(ready_queue, timestamp)
print("Current Process after completion:", current_process)

# Testing Shortest-Remaining-Time-Next Preemptive Scheduling
current_process = handle_process_arrival_srtp(ready_queue, current_process, new_process, timestamp)
print("Current Process:", current_process)
current_process = handle_process_completion_srtp(ready_queue, timestamp)
print("Current Process after completion:", current_process)

# Testing Round-Robin Scheduling
current_process = handle_process_arrival_rr(ready_queue, current_process, new_process, timestamp, time_quantum)
print("Current Process:", current_process)
current_process = handle_process_completion_rr(ready_queue, timestamp, time_quantum)
print("Current Process after completion:", current_process)
 
