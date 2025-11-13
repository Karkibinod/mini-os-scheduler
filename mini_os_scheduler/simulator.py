"""
Simulator module for running CPU scheduling algorithms and calculating metrics.
"""

from typing import List, Dict, Any
from mini_os_scheduler.models import Process, ProcessResult
from mini_os_scheduler.algorithms import fcfs, sjf, priority_scheduling, round_robin


class SchedulingResult:
    """Container for algorithm results and statistics."""
    
    def __init__(self, algorithm_name: str, results: List[ProcessResult]):
        self.algorithm_name = algorithm_name
        self.results = results
        self.avg_waiting_time = sum(r.waiting_time for r in results) / len(results) if results else 0
        self.avg_turnaround_time = sum(r.turnaround_time for r in results) / len(results) if results else 0


def run_fcfs(processes: List[Process]) -> SchedulingResult:
    """Run FCFS algorithm and return results."""
    results = fcfs(processes)
    return SchedulingResult("FCFS", results)


def run_sjf(processes: List[Process]) -> SchedulingResult:
    """Run SJF algorithm and return results."""
    results = sjf(processes)
    return SchedulingResult("SJF", results)


def run_priority(processes: List[Process]) -> SchedulingResult:
    """Run Priority Scheduling algorithm and return results."""
    results = priority_scheduling(processes)
    return SchedulingResult("Priority Scheduling", results)


def run_round_robin(processes: List[Process], time_quantum: int) -> SchedulingResult:
    """Run Round Robin algorithm and return results."""
    results = round_robin(processes, time_quantum)
    return SchedulingResult(f"Round Robin (Q={time_quantum})", results)


def format_results_table(result: SchedulingResult) -> str:
    """
    Format scheduling results as a table.
    
    Args:
        result: SchedulingResult object containing algorithm results
        
    Returns:
        Formatted string table
    """
    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"Algorithm: {result.algorithm_name}")
    lines.append(f"{'='*80}")
    lines.append(f"{'PID':<6} {'Arrival':<8} {'Burst':<8} {'Priority':<10} "
                 f"{'Start':<8} {'Finish':<8} {'Waiting':<8} {'Turnaround':<10}")
    lines.append("-" * 80)
    
    for r in result.results:
        lines.append(f"{r.pid:<6} {r.arrival_time:<8} {r.burst_time:<8} {r.priority:<10} "
                    f"{r.start_time:<8} {r.finish_time:<8} {r.waiting_time:<8} {r.turnaround_time:<10}")
    
    lines.append("-" * 80)
    lines.append(f"{'Average':<6} {'':<8} {'':<8} {'':<10} "
                f"{'':<8} {'':<8} {result.avg_waiting_time:<8.2f} {result.avg_turnaround_time:<10.2f}")
    lines.append(f"{'='*80}\n")
    
    return "\n".join(lines)


def print_results(result: SchedulingResult):
    """Print formatted results to console."""
    print(format_results_table(result))


def compare_algorithms(processes: List[Process], time_quantum: int = 2) -> Dict[str, SchedulingResult]:
    """
    Run all algorithms and return comparison results.
    
    Args:
        processes: List of processes to schedule
        time_quantum: Time quantum for Round Robin
        
    Returns:
        Dictionary mapping algorithm names to SchedulingResult objects
    """
    results = {}
    
    results["FCFS"] = run_fcfs(processes)
    results["SJF"] = run_sjf(processes)
    results["Priority"] = run_priority(processes)
    results["Round Robin"] = run_round_robin(processes, time_quantum)
    
    return results


def print_comparison(comparison_results: Dict[str, SchedulingResult]):
    """Print comparison table of all algorithms."""
    print("\n" + "="*80)
    print("ALGORITHM COMPARISON")
    print("="*80)
    print(f"{'Algorithm':<25} {'Avg Waiting Time':<20} {'Avg Turnaround Time':<20}")
    print("-" * 80)
    
    for name, result in comparison_results.items():
        print(f"{name:<25} {result.avg_waiting_time:<20.2f} {result.avg_turnaround_time:<20.2f}")
    
    print("="*80 + "\n")

