# app_mqtt_web.py
import json
from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "health_monitoring/#"  # Subscreve todos os pacientes

# --- MQTT callbacks ---
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        # envia via websocket ao frontend
        socketio.emit('new_reading', {'topic': topic, 'data': payload})
    except Exception as e:
        print(f"Error processing message: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# --- Web routes ---
@app.route('/')
def index():
    return """
<!doctype html>
<html>
<head>
  <title>Health Monitor</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.min.js"></script>
</head>
<body>
<h1>Live Patient Readings</h1>
<ul id="readings"></ul>
<script>
  const socket = io();
  const list = document.getElementById('readings');
  socket.on('new_reading', (msg) => {
    const li = document.createElement('li');
    li.textContent = `[${msg.topic}] ${JSON.stringify(msg.data)}`;
    list.prepend(li);
    if(list.childNodes.length > 20) list.removeChild(list.lastChild);
  });
</script>
</body>
</html>
"""

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
