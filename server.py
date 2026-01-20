from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import threading, subprocess, os

app = Flask(__name__, template_folder='templates')
CORS(app)
system_logs = []
is_running = False

def run_logic(mode, coin, custom):
    global system_logs, is_running
    is_running = True
    system_logs.clear()
    cmd = f"python -u omni_bot.py {mode} \"{coin}\" \"{custom}\""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        system_logs.append(line.strip())
    is_running = False

@app.route('/')
def home(): return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    global is_running
    if is_running: return jsonify({"status": "busy"}), 400
    data = request.json
    threading.Thread(target=run_logic, args=(data.get('mode'), data.get('coin'), data.get('custom'))).start()
    return jsonify({"status": "success"})

@app.route('/get_status')
def get_status(): return jsonify({"is_running": is_running, "logs": system_logs})

@app.route('/download')
def download(): return send_file('final_video.mp4') if os.path.exists('final_video.mp4') else ("Not Found", 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
