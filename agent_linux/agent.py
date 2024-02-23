# agent.py

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from rules import add_iptables_rule ,block_port
import logging
import process_monitor

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/apply-rules', methods=['POST'])
def apply_rules():
    rules = request.json.get('rules', [])
    for rule in rules:
        add_iptables_rule(rule['protocol'], rule['destination_port'], rule['action'])
    return jsonify({'status': 'success'})


@app.route('/block_port', methods=['POST'])
def block_port_route():
    port = request.json.get('port')
    if not port:
        return jsonify({"error": "port is required"}), 400
    try:
        port = int(port)
    except ValueError:
        return jsonify({"error": "port must be a number"}), 400
    block_port(port)
    return jsonify({"message": f"port {port} blocked"}), 200


@app.route('/process_results')
def process_results():
    logging.debug(process_monitor.results)
    return jsonify(process_monitor.get_process_data())


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
