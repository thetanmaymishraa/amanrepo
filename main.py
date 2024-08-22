import streamlit as st
import pandas as pd

class Process:
    def __init__(self, id, burst_time, arrival_time, priority=0):
        self.id = id
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        self.response_time = -1
        self.remaining_time = burst_time
        self.is_completed = False

def fcfs(processes):
    current_time = 0
    for process in sorted(processes, key=lambda x: x.arrival_time):
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        process.waiting_time = current_time - process.arrival_time
        process.completion_time = current_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.response_time = process.waiting_time
        current_time = process.completion_time
    return processes

def sjf(processes):
    current_time = 0
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    completed = 0
    while completed != len(processes):
        ready_queue = [p for p in processes if p.arrival_time <= current_time and not p.is_completed]
        if ready_queue:
            process = min(ready_queue, key=lambda x: x.burst_time)
            process.waiting_time = current_time - process.arrival_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.response_time = process.waiting_time
            current_time = process.completion_time
            process.is_completed = True
            completed += 1
        else:
            current_time += 1
    return processes

def priority_scheduling(processes):
    current_time = 0
    completed = 0
    while completed != len(processes):
        ready_queue = [p for p in processes if p.arrival_time <= current_time and not p.is_completed]
        if ready_queue:
            process = min(ready_queue, key=lambda x: x.priority)
            process.waiting_time = current_time - process.arrival_time
            process.completion_time = current_time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.response_time = process.waiting_time
            current_time = process.completion_time
            process.is_completed = True
            completed += 1
        else:
            current_time += 1
    return processes

def round_robin(processes, quantum):
    current_time = 0
    ready_queue = []
    for process in processes:
        if process.arrival_time <= current_time:
            ready_queue.append(process)
    while ready_queue:
        process = ready_queue.pop(0)
        if process.response_time == -1:
            process.response_time = current_time - process.arrival_time
        if process.remaining_time > quantum:
            process.remaining_time -= quantum
            current_time += quantum
            ready_queue.extend([p for p in processes if p.arrival_time <= current_time and p not in ready_queue and not p.is_completed])
            ready_queue.append(process)
        else:
            current_time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            process.is_completed = True
    return processes

def srtf(processes):
    current_time = 0
    completed = 0
    while completed != len(processes):
        ready_queue = [p for p in processes if p.arrival_time <= current_time and not p.is_completed]
        if ready_queue:
            process = min(ready_queue, key=lambda x: x.remaining_time)
            if process.response_time == -1:
                process.response_time = current_time - process.arrival_time
            process.remaining_time -= 1
            current_time += 1
            if process.remaining_time == 0:
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                process.is_completed = True
                completed += 1
        else:
            current_time += 1
    return processes

st.title("CPU Scheduling Algorithms")

st.sidebar.header("Process Input")
num_processes = st.sidebar.number_input("Number of Processes", min_value=1, max_value=10, value=5)

process_data = []
for i in range(num_processes):
    burst_time = st.sidebar.number_input(f"Burst Time of P{i+1}", min_value=1)
    arrival_time = st.sidebar.number_input(f"Arrival Time of P{i+1}", min_value=0)
    priority = st.sidebar.number_input(f"Priority of P{i+1} (only for Priority Scheduling)", min_value=0)
    process_data.append(Process(id=i+1, burst_time=burst_time, arrival_time=arrival_time, priority=priority))

algorithm = st.selectbox("Select Scheduling Algorithm", ["FCFS", "SJF", "Priority Scheduling", "Round Robin", "SRTF"])
quantum = 0
if algorithm == "Round Robin":
    quantum = st.number_input("Time Quantum", min_value=1)

if st.button("Calculate"):
    if algorithm == "FCFS":
        results = fcfs(process_data)
    elif algorithm == "SJF":
        results = sjf(process_data)
    elif algorithm == "Priority Scheduling":
        results = priority_scheduling(process_data)
    elif algorithm == "Round Robin":
        results = round_robin(process_data, quantum)
    elif algorithm == "SRTF":
        results = srtf(process_data)

    df = pd.DataFrame([vars(p) for p in results])
    df = df[["id", "burst_time", "arrival_time", "priority", "waiting_time", "turnaround_time", "completion_time", "response_time"]]
    st.write("### Scheduling Results")
    st.dataframe(df)

    avg_waiting_time = df["waiting_time"].mean()
    avg_turnaround_time = df["turnaround_time"].mean()

    st.write(f"**Average Waiting Time:** {avg_waiting_time:.2f} ms")
    st.write(f"**Average Turnaround Time:** {avg_turnaround_time:.2f} ms")
