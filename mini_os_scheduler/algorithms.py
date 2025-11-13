"""
CPU scheduling algorithm implementations.
"""

from typing import List, Tuple
from mini_os_scheduler.models import Process, ProcessResult


def fcfs(processes: List[Process]) -> List[ProcessResult]:
    """
    First-Come, First-Serve (FCFS) scheduling algorithm.
    
    Processes are executed in the order of their arrival time.
    
    Args:
        processes: List of processes to schedule
        
    Returns:
        List of ProcessResult objects with scheduling metrics
    """
    # Sort by arrival time
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    
    results: List[ProcessResult] = []
    current_time = 0
    
    for process in sorted_processes:
        # If process arrives after current time, wait for it
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        start_time = current_time
        finish_time = current_time + process.burst_time
        waiting_time = start_time - process.arrival_time
        turnaround_time = finish_time - process.arrival_time
        
        results.append(ProcessResult(
            pid=process.pid,
            arrival_time=process.arrival_time,
            burst_time=process.burst_time,
            priority=process.priority,
            start_time=start_time,
            finish_time=finish_time,
            waiting_time=waiting_time,
            turnaround_time=turnaround_time
        ))
        
        current_time = finish_time
    
    return results


def sjf(processes: List[Process]) -> List[ProcessResult]:
    """
    Shortest Job First (SJF) - non-preemptive scheduling algorithm.
    
    Among all available processes (arrived and not yet executed),
    the one with the shortest burst time is selected.
    
    Args:
        processes: List of processes to schedule
        
    Returns:
        List of ProcessResult objects with scheduling metrics
    """
    results: List[ProcessResult] = []
    remaining_processes = processes.copy()
    current_time = 0
    
    while remaining_processes:
        # Find all processes that have arrived by current_time
        available = [p for p in remaining_processes 
                    if p.arrival_time <= current_time]
        
        if not available:
            # No process available, jump to next arrival time
            next_arrival = min(p.arrival_time for p in remaining_processes)
            current_time = next_arrival
            continue
        
        # Select process with shortest burst time
        selected = min(available, key=lambda p: p.burst_time)
        remaining_processes.remove(selected)
        
        start_time = current_time
        finish_time = current_time + selected.burst_time
        waiting_time = start_time - selected.arrival_time
        turnaround_time = finish_time - selected.arrival_time
        
        results.append(ProcessResult(
            pid=selected.pid,
            arrival_time=selected.arrival_time,
            burst_time=selected.burst_time,
            priority=selected.priority,
            start_time=start_time,
            finish_time=finish_time,
            waiting_time=waiting_time,
            turnaround_time=turnaround_time
        ))
        
        current_time = finish_time
    
    return results


def priority_scheduling(processes: List[Process]) -> List[ProcessResult]:
    """
    Priority Scheduling - non-preemptive algorithm.
    
    Among all available processes, the one with the highest priority
    (lowest priority number) is selected.
    
    Args:
        processes: List of processes to schedule
        
    Returns:
        List of ProcessResult objects with scheduling metrics
    """
    results: List[ProcessResult] = []
    remaining_processes = processes.copy()
    current_time = 0
    
    while remaining_processes:
        # Find all processes that have arrived by current_time
        available = [p for p in remaining_processes 
                    if p.arrival_time <= current_time]
        
        if not available:
            # No process available, jump to next arrival time
            next_arrival = min(p.arrival_time for p in remaining_processes)
            current_time = next_arrival
            continue
        
        # Select process with highest priority (lowest priority number)
        # In case of tie, use FCFS (lower arrival time, then lower PID)
        selected = min(available, key=lambda p: (p.priority, p.arrival_time, p.pid))
        remaining_processes.remove(selected)
        
        start_time = current_time
        finish_time = current_time + selected.burst_time
        waiting_time = start_time - selected.arrival_time
        turnaround_time = finish_time - selected.arrival_time
        
        results.append(ProcessResult(
            pid=selected.pid,
            arrival_time=selected.arrival_time,
            burst_time=selected.burst_time,
            priority=selected.priority,
            start_time=start_time,
            finish_time=finish_time,
            waiting_time=waiting_time,
            turnaround_time=turnaround_time
        ))
        
        current_time = finish_time
    
    return results


def round_robin(processes: List[Process], time_quantum: int) -> List[ProcessResult]:
    """
    Round Robin (RR) - preemptive scheduling algorithm.
    
    Each process gets a time slice (quantum) to execute. If it doesn't
    finish, it's moved to the back of the queue.
    
    Args:
        processes: List of processes to schedule
        time_quantum: Time slice allocated to each process
        
    Returns:
        List of ProcessResult objects with scheduling metrics
    """
    if time_quantum <= 0:
        raise ValueError("Time quantum must be positive")
    
    # Initialize remaining burst times and metadata
    remaining_burst = {p.pid: p.burst_time for p in processes}
    arrival_times = {p.pid: p.arrival_time for p in processes}
    priorities = {p.pid: p.priority for p in processes}
    original_burst = {p.pid: p.burst_time for p in processes}
    
    # Track first start time for each process
    first_start = {}
    
    results: List[ProcessResult] = []
    queue: List[int] = []  # Queue of process IDs
    current_time = 0
    completed = set()
    added_to_queue = set()  # Track processes that have been added to queue at least once
    
    # Sort processes by arrival time for initial queue population
    sorted_by_arrival = sorted(processes, key=lambda p: p.arrival_time)
    
    while len(completed) < len(processes):
        # Add processes that have arrived to the queue (only once per arrival)
        for process in sorted_by_arrival:
            if (process.pid not in completed and 
                process.arrival_time <= current_time and
                process.pid not in added_to_queue):
                queue.append(process.pid)
                added_to_queue.add(process.pid)
        
        if not queue:
            # No process in queue, jump to next arrival
            next_arrival = min(p.arrival_time for p in sorted_by_arrival 
                             if p.pid not in completed)
            current_time = next_arrival
            continue
        
        # Get next process from queue
        current_pid = queue.pop(0)
        
        # Record first start time
        if current_pid not in first_start:
            first_start[current_pid] = current_time
        
        # Execute for time quantum or until completion
        execution_time = min(time_quantum, remaining_burst[current_pid])
        current_time += execution_time
        remaining_burst[current_pid] -= execution_time
        
        # Check for newly arrived processes (that haven't been added yet)
        for process in sorted_by_arrival:
            if (process.pid not in completed and 
                process.arrival_time <= current_time and
                process.pid not in added_to_queue):
                queue.append(process.pid)
                added_to_queue.add(process.pid)
        
        # If process is not finished, add it back to queue
        if remaining_burst[current_pid] > 0:
            queue.append(current_pid)
        else:
            # Process completed - add to results only once
            if current_pid not in completed:
                completed.add(current_pid)
                finish_time = current_time
                start_time = first_start[current_pid]
                arrival = arrival_times[current_pid]
                burst = original_burst[current_pid]
                
                results.append(ProcessResult(
                    pid=current_pid,
                    arrival_time=arrival,
                    burst_time=burst,
                    priority=priorities[current_pid],
                    start_time=start_time,
                    finish_time=finish_time,
                    waiting_time=finish_time - arrival - burst,
                    turnaround_time=finish_time - arrival
                ))
    
    # Sort results by PID for consistent output
    results.sort(key=lambda r: r.pid)
    return results

