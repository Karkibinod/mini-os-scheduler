# Mini OS CPU Scheduler

[![PyPI version](https://badge.fury.io/py/mini-os-scheduler.svg)](https://badge.fury.io/py/mini-os-scheduler)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive CPU scheduling simulator implemented in Python that demonstrates core operating systems concepts. This package simulates and compares multiple CPU scheduling algorithms with detailed metrics and analysis.

## 🎯 Features

This simulator implements four fundamental CPU scheduling algorithms:

1. **First-Come, First-Serve (FCFS)** - Non-preemptive, executes processes in arrival order
2. **Shortest Job First (SJF)** - Non-preemptive, selects shortest available job
3. **Priority Scheduling** - Non-preemptive, executes highest priority process first
4. **Round Robin (RR)** - Preemptive, uses time quantum for fair scheduling

For each algorithm, the simulator calculates:
- Start time
- Finish time
- Waiting time
- Turnaround time
- Average waiting time
- Average turnaround time

## 🚀 Installation

Install from PyPI:

```bash
pip install mini-os-scheduler
```

For web dashboard support:

```bash
pip install "mini-os-scheduler[web]"
```

## 📖 Quick Start

### Command Line Interface

After installation, use the `mini-scheduler` command:

```bash
# Run all algorithms with sample data
mini-scheduler --sample --algorithm all

# Run specific algorithm
mini-scheduler --sample --algorithm fcfs
mini-scheduler --sample --algorithm sjf
mini-scheduler --sample --algorithm priority
mini-scheduler --sample --algorithm rr --quantum 3

# Load from JSON file
mini-scheduler --file processes.json --algorithm all

# Load from CSV file
mini-scheduler --file processes.csv --algorithm sjf
```

### Python API

```python
from mini_os_scheduler import Process, compare_algorithms

# Create processes
processes = [
    Process(pid=1, arrival_time=0, burst_time=5, priority=2),
    Process(pid=2, arrival_time=1, burst_time=3, priority=1),
    Process(pid=3, arrival_time=2, burst_time=8, priority=3),
]

# Compare all algorithms
results = compare_algorithms(processes, time_quantum=2)

# Access results
for name, result in results.items():
    print(f"{name}:")
    print(f"  Avg Waiting Time: {result.avg_waiting_time:.2f}")
    print(f"  Avg Turnaround Time: {result.avg_turnaround_time:.2f}")
    for r in result.results:
        print(f"    PID {r.pid}: Start={r.start_time}, Finish={r.finish_time}")
```

### Input File Formats

**JSON Format** (`processes.json`):
```json
[
  {"pid": 1, "arrival_time": 0, "burst_time": 5, "priority": 2},
  {"pid": 2, "arrival_time": 1, "burst_time": 3, "priority": 1},
  {"pid": 3, "arrival_time": 2, "burst_time": 8, "priority": 3}
]
```

**CSV Format** (`processes.csv`):
```csv
pid,arrival_time,burst_time,priority
1,0,5,2
2,1,3,1
3,2,8,3
```

## 📊 Example Output

```
================================================================================
Algorithm: FCFS
================================================================================
PID    Arrival  Burst    Priority   Start    Finish   Waiting  Turnaround
--------------------------------------------------------------------------------
1      0        5        2          0        5        0        5
2      1        3        1          5        8        4        7
3      2        8        3          8        16       6        14
4      3        6        2          16       22       13       19
5      4        4        1          22       26       18       22
--------------------------------------------------------------------------------
Average                                                8.20     13.40
================================================================================
```

## 🌐 Web Dashboard

Start the interactive web dashboard:

```bash
python -m mini_os_scheduler.web.app
```

Then open your browser to `http://localhost:5000`

**Note:** Requires `mini-os-scheduler[web]` installation.

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install "mini-os-scheduler[dev]"

# Run tests
pytest tests/ -v
```

## 🏗️ Architecture

The package follows clean software engineering principles:

```
mini_os_scheduler/
├── models.py          # Process data models (Process, ProcessResult)
├── algorithms.py      # Core scheduling algorithm implementations
├── simulator.py       # Simulation runner and metrics calculation
├── main.py            # CLI entry point
└── web/               # Optional Flask web dashboard
    ├── app.py
    └── templates/
```

### Design Principles

- **Type Hints**: Full type annotations for better code clarity and IDE support
- **Docstrings**: Comprehensive documentation for all functions
- **Modularity**: Each component has a single, well-defined responsibility
- **Testability**: Comprehensive test suite validating algorithm correctness

## 📈 Use Cases

- **Education**: Teaching operating systems concepts
- **Research**: Comparing scheduling algorithm performance
- **Development**: Understanding CPU scheduling behavior
- **Portfolio**: Demonstrating systems programming knowledge

## 🔧 Technical Details

### Algorithm Implementations

- **FCFS**: Simple queue-based execution in arrival order
- **SJF**: Greedy selection of shortest available job at each decision point
- **Priority**: Selection based on priority value (lower = higher priority)
- **Round Robin**: Preemptive scheduling with circular queue and time slicing

### Requirements

- Python 3.7 or higher
- No external dependencies (core package)
- Flask 2.0+ (for web dashboard, optional)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 🔗 Links

- **PyPI**: https://pypi.org/project/mini-os-scheduler/
- **GitHub**: https://github.com/Karkibinod/mini-os-scheduler
- **Issues**: https://github.com/Karkibinod/mini-os-scheduler/issues

---

**A CPU scheduling simulator demonstrating systems programming concepts and software engineering best practices.**
