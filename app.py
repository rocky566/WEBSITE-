from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)
tasks = {}  # Dictionary to store task details


@app.route('/')
def dashboard():
    """Admin dashboard showing active tasks."""
    return render_template('dashboard.html', tasks=tasks)


@app.route('/start_task', methods=['POST'])
def start_task():
    """Start a new task."""
    task_id = request.form['task_id']
    if task_id in tasks:
        return jsonify({"status": "error", "message": "Task already running"}), 400

    def run_task(task_id):
        tasks[task_id] = {"status": "running"}
        try:
            # Simulate a long-running task
            time.sleep(10)
        finally:
            tasks[task_id] = {"status": "completed"}

    thread = threading.Thread(target=run_task, args=(task_id,))
    thread.start()
    tasks[task_id] = {"status": "starting"}
    return jsonify({"status": "success", "task_id": task_id})


@app.route('/stop_task', methods=['POST'])
def stop_task():
    """Stop a running task."""
    task_id = request.form['task_id']
    if task_id not in tasks or tasks[task_id]["status"] != "running":
        return jsonify({"status": "error", "message": "Task not running"}), 400

    # Simulate stopping the task
    tasks[task_id]["status"] = "stopped"
    return jsonify({"status": "success", "task_id": task_id})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
