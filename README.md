# Mini OS CPU Scheduler

[![PyPI version](https://badge.fury.io/py/mini-os-scheduler.svg)](https://badge.fury.io/py/mini-os-scheduler)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A comprehensive, educational CPU scheduling simulator demonstrating fundamental operating systems concepts through clean, well-documented Python code.

**Mini OS CPU Scheduler** is a feature-rich simulation tool that implements and compares four classical CPU scheduling algorithms. Perfect for students learning operating systems, educators teaching scheduling concepts, and developers exploring systems programming.

## 🌟 Why This Project?

- **Educational Focus**: Clear implementations with extensive documentation and comments
- **Production Quality**: Full type hints, comprehensive tests, and clean architecture
- **Flexible Interface**: Use as a CLI tool, Python library, or interactive web dashboard
- **Real Metrics**: Calculates waiting time, turnaround time, and other performance metrics
- **Easy to Use**: Simple installation via pip, works on all platforms

Whether you're studying for an OS exam, teaching a class, or building your portfolio, this project demonstrates both operating systems concepts and software engineering best practices.

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

## 🎓 Learning Resources

Want to learn how this project was built? Check out [LEARN.md](LEARN.md) for:
- Step-by-step development process
- Design decisions and trade-offs
- Implementation details for each algorithm
- Testing strategies
- Packaging and distribution guide

## 📊 Performance Comparison

The simulator allows you to compare algorithms side-by-side. Here's what you'll discover:

| Algorithm | Best For | Drawback |
|-----------|----------|----------|
| **FCFS** | Simple, predictable systems | Can cause convoy effect |
| **SJF** | Minimizing average waiting time | Requires knowing burst times |
| **Priority** | Systems with process priorities | Can cause starvation |
| **Round Robin** | Time-sharing systems | Overhead from context switching |

## 🛠️ Advanced Usage

### Custom Process Generation

```python
from mini_os_scheduler import Process
import random

# Generate random process set
processes = [
    Process(
        pid=i,
        arrival_time=random.randint(0, 10),
        burst_time=random.randint(1, 20),
        priority=random.randint(1, 5)
    )
    for i in range(1, 11)
]
```

### Extract Specific Metrics

```python
from mini_os_scheduler import run_fcfs

result = run_fcfs(processes)

# Get process with longest waiting time
max_wait = max(result.results, key=lambda r: r.waiting_time)
print(f"Process {max_wait.pid} waited {max_wait.waiting_time} units")

# Calculate CPU utilization
total_burst = sum(p.burst_time for p in processes)
total_time = max(r.finish_time for r in result.results)
utilization = (total_burst / total_time) * 100
print(f"CPU Utilization: {utilization:.2f}%")
```

## 🔍 Algorithm Details

### FCFS (First-Come, First-Serve)
- **Type**: Non-preemptive
- **Selection**: Process with earliest arrival time
- **Use Case**: Batch systems, simple schedulers
- **Time Complexity**: O(n log n) for sorting

### SJF (Shortest Job First)
- **Type**: Non-preemptive
- **Selection**: Process with shortest burst time
- **Use Case**: Minimizing average waiting time
- **Time Complexity**: O(n²) worst case

### Priority Scheduling
- **Type**: Non-preemptive
- **Selection**: Process with highest priority (lowest number)
- **Use Case**: Real-time systems, critical processes
- **Time Complexity**: O(n²) worst case

### Round Robin
- **Type**: Preemptive
- **Selection**: Circular queue with time quantum
- **Use Case**: Time-sharing systems, interactive applications
- **Time Complexity**: O(n × (total_burst / quantum))

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Binod Karki

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue describing the bug and how to reproduce it
2. **Suggest Features**: Share ideas for new algorithms or features
3. **Submit PRs**: Fork, create a feature branch, and submit a pull request
4. **Improve Docs**: Help make documentation clearer and more comprehensive
5. **Write Tests**: Add test cases to improve coverage

Please ensure:
- Code follows existing style (type hints, docstrings)
- Tests pass (`pytest tests/ -v`)
- New features include tests and documentation

## 🙏 Acknowledgments

- Inspired by classical OS textbooks (Silberschatz, Tanenbaum)
- Built with modern Python best practices
- Thanks to the open-source community

## 📧 Contact

**Binod Karki**
- GitHub: [@Karkibinod](https://github.com/Karkibinod)
- Email: karkibinod367@gmail.com

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/mini-os-scheduler/
- **Source Code**: https://github.com/Karkibinod/mini-os-scheduler
- **Issue Tracker**: https://github.com/Karkibinod/mini-os-scheduler/issues
- **Documentation**: See [LEARN.md](LEARN.md) for detailed guide

## ⭐ Show Your Support

If you find this project helpful:
- Star the repository on GitHub
- Share it with others learning OS concepts
- Contribute improvements
- Use it in your teaching or projects

---

**A CPU scheduling simulator demonstrating operating systems concepts and software engineering best practices.**

*Made with ❤️ for students, educators, and systems programming enthusiasts.*
