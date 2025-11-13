"""
Test suite for CPU scheduling algorithms.
"""

import pytest
from mini_os_scheduler.models import Process
from mini_os_scheduler.algorithms import fcfs, sjf, priority_scheduling, round_robin


class TestFCFS:
    """Tests for First-Come, First-Serve algorithm."""

    def test_fcfs_basic_order(self):
        """Test that FCFS executes processes in arrival order."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=5),
            Process(pid=2, arrival_time=1, burst_time=3),
            Process(pid=3, arrival_time=2, burst_time=2),
        ]

        results = fcfs(processes)

        # Check execution order
        assert results[0].pid == 1
        assert results[1].pid == 2
        assert results[2].pid == 3

        # Check timing
        assert results[0].start_time == 0
        assert results[0].finish_time == 5
        assert results[1].start_time == 5
        assert results[1].finish_time == 8
        assert results[2].start_time == 8
        assert results[2].finish_time == 10

    def test_fcfs_with_gaps(self):
        """Test FCFS when processes don't arrive consecutively."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=2),
            Process(pid=2, arrival_time=5, burst_time=3),
            Process(pid=3, arrival_time=10, burst_time=1),
        ]

        results = fcfs(processes)

        assert results[0].start_time == 0
        assert results[0].finish_time == 2
        assert results[1].start_time == 5  # Waits for arrival
        assert results[1].finish_time == 8
        assert results[2].start_time == 10
        assert results[2].finish_time == 11


class TestSJF:
    """Tests for Shortest Job First algorithm."""

    def test_sjf_chooses_shortest(self):
        """Test that SJF selects shortest available job."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=5),
            Process(pid=2, arrival_time=0, burst_time=2),  # Shortest
            Process(pid=3, arrival_time=0, burst_time=8),
        ]

        results = sjf(processes)

        # Process 2 should execute first (shortest burst)
        assert results[0].pid == 2
        assert results[0].start_time == 0
        assert results[0].finish_time == 2

        # Then process 1 (shorter than 3)
        assert results[1].pid == 1
        assert results[1].start_time == 2

        # Finally process 3
        assert results[2].pid == 3

    def test_sjf_with_arrival_times(self):
        """Test SJF considers only arrived processes."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=5),
            # Shortest but arrives later
            Process(pid=2, arrival_time=2, burst_time=1),
            Process(pid=3, arrival_time=0, burst_time=3),
        ]

        results = sjf(processes)

        # At time 0, only P1 and P3 are available. P3 is shorter.
        assert results[0].pid == 3
        assert results[0].start_time == 0

        # After P3 finishes at time 3, P1 and P2 are available. P2 is shorter.
        assert results[1].pid == 2
        assert results[1].start_time == 3

        # Finally P1
        assert results[2].pid == 1


class TestPriorityScheduling:
    """Tests for Priority Scheduling algorithm."""

    def test_priority_respects_priority(self):
        """Test that priority scheduling selects highest priority process."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=5, priority=3),
            Process(pid=2, arrival_time=0, burst_time=3,
                    priority=1),  # Highest priority
            Process(pid=3, arrival_time=0, burst_time=2, priority=2),
        ]

        results = priority_scheduling(processes)

        # Process 2 should execute first (priority 1 = highest)
        assert results[0].pid == 2
        assert results[0].start_time == 0

        # Then process 3 (priority 2)
        assert results[1].pid == 3

        # Finally process 1 (priority 3)
        assert results[2].pid == 1

    def test_priority_with_arrival_times(self):
        """Test priority scheduling only considers arrived processes."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=5, priority=1),
            # Higher priority but arrives later
            Process(pid=2, arrival_time=3, burst_time=2, priority=0),
            Process(pid=3, arrival_time=0, burst_time=3, priority=2),
        ]

        results = priority_scheduling(processes)

        # At time 0, only P1 and P3 available. P1 has higher priority.
        assert results[0].pid == 1
        assert results[0].start_time == 0

        # After P1 finishes at time 5, P2 and P3 are available. P2 has higher priority.
        assert results[1].pid == 2
        assert results[1].start_time == 5


class TestRoundRobin:
    """Tests for Round Robin algorithm."""

    def test_round_robin_basic(self):
        """Test basic Round Robin execution."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=5),
            Process(pid=2, arrival_time=0, burst_time=3),
        ]

        results = round_robin(processes, time_quantum=2)

        # Both processes should complete
        assert len(results) == 2

        # Verify all processes are in results
        pids = {r.pid for r in results}
        assert pids == {1, 2}

        # Verify turnaround times are reasonable
        for result in results:
            assert result.turnaround_time >= result.burst_time
            assert result.waiting_time >= 0

    def test_round_robin_quantum_respected(self):
        """Test that Round Robin respects time quantum."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=10),
        ]

        results = round_robin(processes, time_quantum=3)

        # Process should complete
        result = results[0]
        assert result.pid == 1
        assert result.finish_time == 10
        assert result.turnaround_time == 10
        assert result.waiting_time == 0

    def test_round_robin_multiple_processes(self):
        """Test Round Robin with multiple processes."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=4),
            Process(pid=2, arrival_time=0, burst_time=3),
            Process(pid=3, arrival_time=0, burst_time=2),
        ]

        results = round_robin(processes, time_quantum=2)

        assert len(results) == 3

        # All processes should complete
        pids = {r.pid for r in results}
        assert pids == {1, 2, 3}

        # Verify metrics are valid
        for result in results:
            assert result.finish_time > result.start_time
            assert result.turnaround_time == result.finish_time - result.arrival_time
            assert result.waiting_time == result.turnaround_time - result.burst_time

    def test_round_robin_invalid_quantum(self):
        """Test that Round Robin raises error for invalid quantum."""
        processes = [Process(pid=1, arrival_time=0, burst_time=5)]

        with pytest.raises(ValueError):
            round_robin(processes, time_quantum=0)

        with pytest.raises(ValueError):
            round_robin(processes, time_quantum=-1)


class TestMetrics:
    """Tests for metric calculations across all algorithms."""

    def test_waiting_time_calculation(self):
        """Test that waiting time is calculated correctly."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=5),
            Process(pid=2, arrival_time=2, burst_time=3),
        ]

        results = fcfs(processes)

        # Process 1: arrives at 0, starts at 0, waits 0
        assert results[0].waiting_time == 0

        # Process 2: arrives at 2, starts at 5, waits 3
        assert results[1].waiting_time == 3

    def test_turnaround_time_calculation(self):
        """Test that turnaround time is calculated correctly."""
        processes = [
            Process(pid=1, arrival_time=0, burst_time=5),
        ]

        results = fcfs(processes)

        # Turnaround = finish - arrival = 5 - 0 = 5
        assert results[0].turnaround_time == 5
        assert results[0].turnaround_time == results[0].waiting_time + \
            results[0].burst_time
