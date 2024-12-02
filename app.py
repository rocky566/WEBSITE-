from flask import Flask, render_template, request, jsonify
import threading
from facebook_tool import FacebookTool

app = Flask(__name__)
tasks = {}  # Dictionary to store task details


@app.route('/')
def dashboard():
    """Admin dashboard showing active tasks."""
    return render_template('dashboard.html', tasks=tasks)


@app.route('/start_task', methods=['GET', 'POST'])
def start_task():
    """Start a new task."""
    if request.method == 'POST':
        task_id = request.form['task_id']
        post_url = request.form['post_url']
        cookies = request.form['cookies']
        delay = int(request.form['delay'])
        comments_file = request.form['comments_file']

        if task_id in tasks:
            return jsonify({"status": "error", "message": "Task already running"}), 400

        def task_logic():
            tasks[task_id] = {"status": "running"}
            fb_tool = FacebookTool(task_id, post_url, cookies, delay, comments_file)
            fb_tool.run()
            tasks[task_id]["status"] = "completed"

        thread = threading.Thread(target=task_logic)
        thread.start()

        tasks[task_id] = {"status": "starting"}
        return jsonify({"status": "success", "task_id": task_id})
    
    return render_template('start_task.html')


@app.route('/stop_task', methods=['POST'])
def stop_task():
    """Stop a running task."""
    task_id = request.form['task_id']
    if task_id not in tasks or tasks[task_id]["status"] != "running":
        return jsonify({"status": "error", "message": "Task not running"}), 400

    # Logic to stop task
    tasks[task_id]["status"] = "stopped"
    return jsonify({"status": "success", "task_id": task_id})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
