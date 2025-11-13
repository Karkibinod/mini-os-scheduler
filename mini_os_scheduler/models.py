"""
Process data model for CPU scheduling simulator.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Process:
    """Represents a process in the CPU scheduler."""
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0  # Lower number = higher priority
    
    def __post_init__(self):
        """Validate process attributes."""
        if self.arrival_time < 0:
            raise ValueError("Arrival time cannot be negative")
        if self.burst_time <= 0:
            raise ValueError("Burst time must be positive")
        if self.priority < 0:
            raise ValueError("Priority cannot be negative")


@dataclass
class ProcessResult:
    """Results for a single process after scheduling."""
    pid: int
    arrival_time: int
    burst_time: int
    priority: int
    start_time: int
    finish_time: int
    waiting_time: int
    turnaround_time: int
    
    @property
    def response_time(self) -> int:
        """Time from arrival to first execution."""
        return self.start_time - self.arrival_time

