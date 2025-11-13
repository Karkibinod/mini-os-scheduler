"""
Main CLI entry point for CPU Scheduler Simulator.
"""

import argparse
import json
import csv
import sys
from typing import List
from pathlib import Path

from mini_os_scheduler.models import Process
from mini_os_scheduler.simulator import (
    run_fcfs, run_sjf, run_priority, run_round_robin,
    print_results, compare_algorithms, print_comparison
)


def load_processes_from_json(filepath: str) -> List[Process]:
    """Load processes from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        processes = []
        for item in data:
            processes.append(Process(
                pid=item['pid'],
                arrival_time=item['arrival_time'],
                burst_time=item['burst_time'],
                priority=item.get('priority', 0)
            ))
        return processes
    except Exception as e:
        print(f"Error loading JSON file: {e}", file=sys.stderr)
        sys.exit(1)


def load_processes_from_csv(filepath: str) -> List[Process]:
    """Load processes from a CSV file."""
    try:
        processes = []
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                processes.append(Process(
                    pid=int(row['pid']),
                    arrival_time=int(row['arrival_time']),
                    burst_time=int(row['burst_time']),
                    priority=int(row.get('priority', 0))
                ))
        return processes
    except Exception as e:
        print(f"Error loading CSV file: {e}", file=sys.stderr)
        sys.exit(1)


def get_sample_processes() -> List[Process]:
    """Return a sample set of processes for demonstration."""
    return [
        Process(pid=1, arrival_time=0, burst_time=5, priority=2),
        Process(pid=2, arrival_time=1, burst_time=3, priority=1),
        Process(pid=3, arrival_time=2, burst_time=8, priority=3),
        Process(pid=4, arrival_time=3, burst_time=6, priority=2),
        Process(pid=5, arrival_time=4, burst_time=4, priority=1),
    ]


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="CPU Scheduler Simulator - Compare different scheduling algorithms"
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Path to JSON or CSV file containing process data'
    )
    
    parser.add_argument(
        '--algorithm', '-a',
        choices=['fcfs', 'sjf', 'priority', 'rr', 'all'],
        default='all',
        help='Scheduling algorithm to run (default: all)'
    )
    
    parser.add_argument(
        '--quantum', '-q',
        type=int,
        default=2,
        help='Time quantum for Round Robin (default: 2)'
    )
    
    parser.add_argument(
        '--sample', '-s',
        action='store_true',
        help='Use sample process data'
    )
    
    args = parser.parse_args()
    
    # Load processes
    if args.file:
        filepath = Path(args.file)
        if filepath.suffix.lower() == '.json':
            processes = load_processes_from_json(str(filepath))
        elif filepath.suffix.lower() == '.csv':
            processes = load_processes_from_csv(str(filepath))
        else:
            print("Error: File must be JSON (.json) or CSV (.csv)", file=sys.stderr)
            sys.exit(1)
    elif args.sample:
        processes = get_sample_processes()
    else:
        # Default to sample if no file specified
        print("No file specified. Using sample data. Use --sample or --file to specify.")
        processes = get_sample_processes()
    
    if not processes:
        print("Error: No processes to schedule", file=sys.stderr)
        sys.exit(1)
    
    # Run selected algorithm(s)
    if args.algorithm == 'all':
        results = compare_algorithms(processes, args.quantum)
        for result in results.values():
            print_results(result)
        print_comparison(results)
    elif args.algorithm == 'fcfs':
        result = run_fcfs(processes)
        print_results(result)
    elif args.algorithm == 'sjf':
        result = run_sjf(processes)
        print_results(result)
    elif args.algorithm == 'priority':
        result = run_priority(processes)
        print_results(result)
    elif args.algorithm == 'rr':
        result = run_round_robin(processes, args.quantum)
        print_results(result)


if __name__ == '__main__':
    main()

