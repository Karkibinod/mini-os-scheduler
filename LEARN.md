# LEARN.md - Building the Mini OS CPU Scheduler

This document provides step-by-step instructions on how the Mini OS CPU Scheduler project was built, explaining the design decisions, implementation details, and development process.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Project Setup](#step-1-project-setup)
4. [Step 2: Defining Data Models](#step-2-defining-data-models)
5. [Step 3: Implementing Scheduling Algorithms](#step-3-implementing-scheduling-algorithms)
6. [Step 4: Building the Simulator](#step-4-building-the-simulator)
7. [Step 5: Creating the CLI](#step-5-creating-the-cli)
8. [Step 6: Adding Tests](#step-6-adding-tests)
9. [Step 7: Building the Web Dashboard](#step-7-building-the-web-dashboard)
10. [Step 8: Packaging for PyPI](#step-8-packaging-for-pypi)
11. [Lessons Learned](#lessons-learned)

---

## Project Overview

**Goal**: Build a CPU scheduling simulator that implements four fundamental scheduling algorithms (FCFS, SJF, Priority, Round Robin) and provides both CLI and web interfaces.

**Key Features**:
- Multiple scheduling algorithm implementations
- Detailed metrics calculation (waiting time, turnaround time, etc.)
- Command-line interface
- Optional web dashboard
- PyPI package distribution

---

## Prerequisites

To follow along, you should have:
- Python 3.7+ installed
- Basic understanding of:
  - Operating systems concepts (CPU scheduling)
  - Python programming
  - Data structures (queues, lists)
  - Object-oriented programming

---

## Step 1: Project Setup

### 1.1 Create Project Structure

```bash
mkdir mini-os-scheduler
cd mini-os-scheduler
mkdir mini_os_scheduler
mkdir mini_os_scheduler/tests
mkdir mini_os_scheduler/web
mkdir mini_os_scheduler/web/templates
mkdir tests
```

### 1.2 Initialize Git Repository

```bash
git init
echo "*.pyc" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.egg-info/" >> .gitignore
echo "dist/" >> .gitignore
echo "build/" >> .gitignore
```

### 1.3 Create Basic Package Structure

Create `__init__.py` files:
```bash
touch mini_os_scheduler/__init__.py
touch mini_os_scheduler/tests/__init__.py
touch mini_os_scheduler/web/__init__.py
touch tests/__init__.py
```

**Why?** This structure follows Python packaging conventions and separates concerns clearly.

---

## Step 2: Defining Data Models

### 2.1 Create `models.py`

The first step in any well-designed application is defining the data structures. We use Python's `dataclass` decorator for clean, immutable data models.

**File**: `mini_os_scheduler/models.py`

```python
from dataclasses import dataclass

@dataclass
class Process:
    """Represents a process in the CPU scheduler."""
    pid: int
    arrival_time: int
    burst_time: int
    priority: int = 0
    
    def __post_init__(self):
        """Validate process attributes."""
        if self.arrival_time < 0:
            raise ValueError("Arrival time cannot be negative")
        if self.burst_time <= 0:
            raise ValueError("Burst time must be positive")
        if self.priority < 0:
            raise ValueError("Priority cannot be negative")
```

**Key Decisions**:
- Used `dataclass` for automatic `__init__`, `__repr__`, and `__eq__` methods
- Added validation in `__post_init__` to ensure data integrity
- Type hints for better IDE support and code clarity

### 2.2 Create `ProcessResult` Model

```python
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
```

**Why separate models?** Input data (`Process`) and output data (`ProcessResult`) serve different purposes and should be kept separate.

---

## Step 3: Implementing Scheduling Algorithms

### 3.1 First-Come, First-Serve (FCFS)

**File**: `mini_os_scheduler/algorithms.py`

FCFS is the simplest algorithm - processes are executed in order of arrival.

```python
def fcfs(processes: List[Process]) -> List[ProcessResult]:
    """First-Come, First-Serve scheduling."""
    # Sort by arrival time
    sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
    
    results = []
    current_time = 0
    
    for process in sorted_processes:
        # Wait for process to arrive
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        start_time = current_time
        finish_time = current_time + process.burst_time
        waiting_time = start_time - process.arrival_time
        turnaround_time = finish_time - process.arrival_time
        
        results.append(ProcessResult(...))
        current_time = finish_time
    
    return results
```

**Key Points**:
- Sort processes by arrival time
- Track `current_time` to simulate CPU execution
- Handle CPU idle time when no process is available
- Calculate metrics: waiting time = start - arrival, turnaround = finish - arrival

### 3.2 Shortest Job First (SJF)

SJF is a greedy algorithm that always picks the shortest available job.

```python
def sjf(processes: List[Process]) -> List[ProcessResult]:
    """Shortest Job First scheduling."""
    pending = processes.copy()
    results = []
    current_time = 0
    
    while pending:
        # Find available processes
        available = [p for p in pending if p.arrival_time <= current_time]
        
        if not available:
            # CPU idle - jump to next arrival
            current_time = min(p.arrival_time for p in pending)
            continue
        
        # Pick shortest job
        next_process = min(available, key=lambda p: p.burst_time)
        pending.remove(next_process)
        
        # Execute process...
```

**Key Points**:
- Maintain a list of pending processes
- At each decision point, select the shortest available job
- Handle CPU idle time by jumping to the next arrival

### 3.3 Priority Scheduling

Similar to SJF but uses priority instead of burst time.

```python
def priority_scheduling(processes: List[Process]) -> List[ProcessResult]:
    """Priority-based scheduling (lower priority number = higher priority)."""
    # Similar structure to SJF
    next_process = min(available, key=lambda p: (p.priority, p.arrival_time))
```

**Key Decision**: Break ties using arrival time for deterministic results.

### 3.4 Round Robin (RR)

RR is preemptive - each process gets a time quantum before switching.

```python
def round_robin(processes: List[Process], time_quantum: int) -> List[ProcessResult]:
    """Round Robin scheduling with time quantum."""
    from collections import deque
    
    queue = deque()
    remaining_time = {p.pid: p.burst_time for p in processes}
    start_times = {}
    
    # Complex implementation with queue management...
```

**Key Points**:
- Use a `deque` for efficient queue operations
- Track remaining burst time for each process
- Handle process arrivals during execution
- Preempt after time quantum expires

---

## Step 4: Building the Simulator

### 4.1 Create Wrapper Functions

**File**: `mini_os_scheduler/simulator.py`

```python
def run_fcfs(processes: List[Process]) -> ScheduleResult:
    """Run FCFS and return results with metrics."""
    results = fcfs(processes)
    avg_waiting = sum(r.waiting_time for r in results) / len(results)
    avg_turnaround = sum(r.turnaround_time for r in results) / len(results)
    
    return ScheduleResult(
        algorithm_name="FCFS",
        results=results,
        avg_waiting_time=avg_waiting,
        avg_turnaround_time=avg_turnaround
    )
```

### 4.2 Create Comparison Function

```python
def compare_algorithms(processes: List[Process], time_quantum: int = 2) -> dict:
    """Compare all algorithms on the same process set."""
    return {
        'FCFS': run_fcfs(processes),
        'SJF': run_sjf(processes),
        'Priority': run_priority(processes),
        'Round Robin': run_round_robin(processes, time_quantum)
    }
```

### 4.3 Add Output Formatting

```python
def print_results(result: ScheduleResult):
    """Pretty-print scheduling results in table format."""
    print(f"{'='*80}")
    print(f"Algorithm: {result.algorithm_name}")
    print(f"{'='*80}")
    # Format as table...
```

---

## Step 5: Creating the CLI

### 5.1 Set Up Argument Parser

**File**: `mini_os_scheduler/main.py`

```python
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="CPU Scheduler Simulator"
    )
    
    parser.add_argument('--file', '-f', type=str, help='Input file path')
    parser.add_argument('--algorithm', '-a', choices=['fcfs', 'sjf', 'priority', 'rr', 'all'])
    parser.add_argument('--quantum', '-q', type=int, default=2)
    parser.add_argument('--sample', '-s', action='store_true')
```

### 5.2 Implement File Loaders

```python
def load_processes_from_json(filepath: str) -> List[Process]:
    """Load processes from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return [Process(**item) for item in data]

def load_processes_from_csv(filepath: str) -> List[Process]:
    """Load processes from CSV file."""
    processes = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            processes.append(Process(
                pid=int(row['pid']),
                arrival_time=int(row['arrival_time']),
                # ...
            ))
    return processes
```

### 5.3 Configure Entry Point

**File**: `pyproject.toml`

```toml
[project.scripts]
mini-scheduler = "mini_os_scheduler.main:main"
```

This creates a command-line tool that users can run as `mini-scheduler`.

---

## Step 6: Adding Tests

### 6.1 Set Up Testing Framework

**File**: `mini_os_scheduler/tests/test_algorithms.py`

```python
import pytest
from mini_os_scheduler.models import Process
from mini_os_scheduler.algorithms import fcfs, sjf, priority_scheduling, round_robin

def test_fcfs_simple():
    """Test FCFS with basic process set."""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5, priority=0),
        Process(pid=2, arrival_time=1, burst_time=3, priority=0),
    ]
    
    results = fcfs(processes)
    
    assert len(results) == 2
    assert results[0].pid == 1
    assert results[0].waiting_time == 0
    assert results[1].waiting_time == 4
```

### 6.2 Test Edge Cases

```python
def test_fcfs_with_idle_time():
    """Test FCFS when CPU is idle."""
    processes = [
        Process(pid=1, arrival_time=0, burst_time=2, priority=0),
        Process(pid=2, arrival_time=5, burst_time=3, priority=0),
    ]
    
    results = fcfs(processes)
    assert results[1].start_time == 5  # CPU waits
```

### 6.3 Test All Algorithms

Create comprehensive tests for each algorithm covering:
- Normal operation
- Edge cases (empty list, single process)
- CPU idle time
- Tie-breaking behavior
- Metric calculations

---

## Step 7: Building the Web Dashboard

### 7.1 Create Flask Application

**File**: `mini_os_scheduler/web/app.py`

```python
from flask import Flask, render_template, request, jsonify
from mini_os_scheduler import Process, compare_algorithms

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    processes = [Process(**p) for p in data['processes']]
    quantum = data.get('quantum', 2)
    
    results = compare_algorithms(processes, quantum)
    return jsonify(results)
```

### 7.2 Create HTML Template

**File**: `mini_os_scheduler/web/templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>CPU Scheduler Simulator</title>
    <style>
        /* Styling for tables, forms, charts */
    </style>
</head>
<body>
    <h1>CPU Scheduling Simulator</h1>
    <form id="processForm">
        <!-- Input fields for processes -->
    </form>
    <div id="results">
        <!-- Display results -->
    </div>
    <script>
        // JavaScript for interactivity
    </script>
</body>
</html>
```

---

## Step 8: Packaging for PyPI

### 8.1 Create `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mini-os-scheduler"
version = "0.1.0"
description = "A comprehensive CPU scheduling simulator"
readme = "README.md"
requires-python = ">=3.7"
license = {text = "MIT"}
authors = [{name = "Binod Karki", email = "karkibinod367@gmail.com"}]
keywords = ["cpu", "scheduler", "scheduling", "operating-systems"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Education",
    "Topic :: System :: Operating System",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

[project.optional-dependencies]
web = ["flask>=2.0.0"]
dev = ["pytest>=7.0.0", "pytest-cov"]

[project.scripts]
mini-scheduler = "mini_os_scheduler.main:main"
```

### 8.2 Build and Upload

```bash
# Build distribution
python -m build

# Upload to PyPI
twine upload dist/*
```

---

## Lessons Learned

### 1. **Start with Data Models**
Defining clear data structures first makes implementation much easier. The `Process` and `ProcessResult` classes became the foundation of the entire system.

### 2. **Separate Concerns**
- `models.py`: Data structures
- `algorithms.py`: Pure algorithm logic
- `simulator.py`: Orchestration and metrics
- `main.py`: User interface

This separation made testing and maintenance much easier.

### 3. **Type Hints Are Valuable**
Adding type hints throughout the codebase:
- Caught bugs during development
- Made the code self-documenting
- Improved IDE autocomplete

### 4. **Test Edge Cases**
The most bugs were found when testing:
- Empty process lists
- CPU idle time
- Single process scenarios
- Processes arriving at the same time

### 5. **Documentation Matters**
Writing docstrings for every function forced me to think clearly about each function's purpose and made the code more maintainable.

### 6. **Incremental Development**
Built the project in stages:
1. Models → 2. FCFS → 3. Other algorithms → 4. CLI → 5. Tests → 6. Web → 7. Package

Each stage was tested before moving to the next.

### 7. **Round Robin Is Complex**
The Round Robin implementation was the most challenging due to:
- Queue management
- Process preemption
- Handling arrivals during execution
- Tracking remaining burst time

Don't underestimate preemptive algorithms!

### 8. **PyPI Packaging**
Publishing to PyPI requires:
- Proper `pyproject.toml` configuration
- Comprehensive README
- Semantic versioning
- Clear license
- Testing on clean environments

---

## Next Steps

To extend this project, consider:

1. **More Algorithms**: SRTF (Shortest Remaining Time First), Multilevel Queue
2. **Visualization**: Gantt charts, timeline animations
3. **Advanced Metrics**: CPU utilization, throughput, context switches
4. **Real-time Simulation**: Animated step-by-step execution
5. **Benchmarking**: Performance comparison tools
6. **Interactive Tutorial**: Guided learning mode

---

## Resources

- [Operating System Concepts (Silberschatz)](https://www.os-book.com/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Happy Learning!** If you have questions or want to contribute, feel free to open an issue or pull request on GitHub.
