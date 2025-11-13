"""
Flask web application for CPU Scheduler Simulator.
"""

from flask import Flask, render_template, request, jsonify
from mini_os_scheduler.models import Process
from mini_os_scheduler.simulator import (
    run_fcfs, run_sjf, run_priority, run_round_robin,
    SchedulingResult
)

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')


@app.route('/api/schedule', methods=['POST'])
def schedule():
    """API endpoint to run scheduling algorithms."""
    try:
        data = request.json
        
        # Parse processes from request
        processes_data = data.get('processes', [])
        algorithm = data.get('algorithm', 'all')
        time_quantum = int(data.get('time_quantum', 2))
        
        # Validate input
        if not processes_data:
            return jsonify({'error': 'No processes provided'}), 400
        
        # Create Process objects
        processes = []
        for p in processes_data:
            processes.append(Process(
                pid=int(p['pid']),
                arrival_time=int(p['arrival_time']),
                burst_time=int(p['burst_time']),
                priority=int(p.get('priority', 0))
            ))
        
        # Run selected algorithm
        if algorithm == 'all':
            results = {
                'FCFS': run_fcfs(processes),
                'SJF': run_sjf(processes),
                'Priority': run_priority(processes),
                'Round Robin': run_round_robin(processes, time_quantum)
            }
        elif algorithm == 'fcfs':
            results = {'FCFS': run_fcfs(processes)}
        elif algorithm == 'sjf':
            results = {'SJF': run_sjf(processes)}
        elif algorithm == 'priority':
            results = {'Priority': run_priority(processes)}
        elif algorithm == 'rr':
            results = {'Round Robin': run_round_robin(processes, time_quantum)}
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        # Convert results to JSON-serializable format
        output = {}
        for name, result in results.items():
            output[name] = {
                'algorithm': name,
                'results': [
                    {
                        'pid': r.pid,
                        'arrival_time': r.arrival_time,
                        'burst_time': r.burst_time,
                        'priority': r.priority,
                        'start_time': r.start_time,
                        'finish_time': r.finish_time,
                        'waiting_time': r.waiting_time,
                        'turnaround_time': r.turnaround_time
                    }
                    for r in result.results
                ],
                'avg_waiting_time': round(result.avg_waiting_time, 2),
                'avg_turnaround_time': round(result.avg_turnaround_time, 2)
            }
        
        return jsonify(output)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
