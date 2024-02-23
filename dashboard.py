from flask import Flask, render_template,json,request,jsonify
from flask_socketio import SocketIO, emit
from rules import predefined_rules_list
from agent_manager import AgentManager
import requests
import logging



app = Flask(__name__)
socketio = SocketIO(app)
# Configure logging
logging.basicConfig(filename='Dashboard.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the agent URL
AGENT_URL = 'http://172.18.89.68:5001'

@app.route('/')
def index():
    return render_template('index.html', predefined_rules=predefined_rules_list)

# def agents_list():
#     """ Get a list of all available Agents from the Agent Manager Server """
#     try:
#         response = requests.get(urljoin(AGENT_URL, "agents"))
#         if response.status_code == 404:
#             logger.error("Agents not found on server")
#             raise Exception("No agents found.")
#         else:
#             data = json.loads(response.text)['agents']
#             # Sort by name (case-insensitive)
#             return sorted(data, key=lambda x: x["name"].lower())
#     except:
#         logger.exception("Error getting agents list")
#         return []

@socketio.on('connect')
def handle_connect():
    logger.info("Client connected")
    emit('server_message', {'data': 'Connected to Dashboard Server.'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.warning("Client disconnected")



@socketio.on('apply-rule')
def apply_rule(rule_index):
    selected_rule = predefined_rules_list[int(rule_index)]
    emit('response', {'message': f'Selected rule: {selected_rule["description"]}'})  # Change 'name' to 'description'
    logging.info(selected_rule)

    # Convert ObjectId to string
    selected_rule['_id'] = str(selected_rule['_id'])

    # Send the selected rule to the agent
    response = requests.post(f'{AGENT_URL}/apply-rules', json={'rules': [selected_rule]})

    if response.status_code == 200:
        emit('response', {'message': 'Rule applied successfully to the agent'})
    else:
        emit('response', {'message': 'Error applying rule to the agent'})


@app.route('/block_port', methods=['GET', 'POST'])
def block_port():
    if request.method == 'GET':
        return render_template('block_port.html')
    elif request.method == 'POST':
        port = request.form.get('portNumber')
        logging.info(port)
        if port is None:
            return jsonify({'error': 'Port number is required'}), 400

        try:
            # Define the URL of the block_port API endpoint
            # url = 'http://AGENT_URL/block_port'  # Replace <hostname> and <port> with the correct values

            # Define the JSON payload to send in the request
            payload = {'port': port}

            # Send a POST request to the API endpoint
            response = requests.post(f'{AGENT_URL}/block_port', json=payload)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                return jsonify({'message': f'Port {port} blocked successfully'}), 200
            else:
                return jsonify({'error': response.text}), response.status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# processor_details = []

# @app.route('/process_monitor', methods=["GET"])
# def process_monitor():
#     # Make a GET request to the endpoint where processor details are sent
#     url = 'http:/{AGENT_URL}/process_monitor'
#     response = requests.get(url)

#     if response.status_code == 200:
#         # If the request is successful, render the response in a template
#         return render_template('processor.html', processor_details=response.json())
#     else:
#         # If the request fails, return an error message
#         return "Failed to retrieve processor details from the endpoint."
    
    
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
