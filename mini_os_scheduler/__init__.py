"""
Mini OS CPU Scheduler - A comprehensive CPU scheduling simulator.

This package implements four fundamental CPU scheduling algorithms:
- First-Come, First-Serve (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Round Robin (RR)

Each algorithm calculates detailed metrics including start time, finish time,
waiting time, and turnaround time for each process.
"""

__version__ = "0.1.0"
__author__ = "Binod Karki"

from mini_os_scheduler.models import Process, ProcessResult
from mini_os_scheduler.algorithms import (
    fcfs,
    sjf,
    priority_scheduling,
    round_robin
)
from mini_os_scheduler.simulator import (
    SchedulingResult,
    run_fcfs,
    run_sjf,
    run_priority,
    run_round_robin,
    compare_algorithms
)

__all__ = [
    "Process",
    "ProcessResult",
    "fcfs",
    "sjf",
    "priority_scheduling",
    "round_robin",
    "SchedulingResult",
    "run_fcfs",
    "run_sjf",
    "run_priority",
    "run_round_robin",
    "compare_algorithms",
]

