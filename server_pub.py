from flask import Flask, render_template
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

# Configuration MQTT
mqtt_broker_host = "localhost"
mqtt_topics = ["home/cam", "home/data"]

# Directories for saving received images and data
static_image_folder = '/home/thomasm/mc-python/Projet/SERVER_Final/static'
image_filename = 'received_image.png'

# Initialize global variables to store the latest data
latest_image_path = ''
latest_data = ''

# Callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    global latest_image_path, latest_data

    if message.topic == "home/cam":
        # Save image and update the latest image path
        image_path = os.path.join(static_image_folder, image_filename)
        
        # Supprimer l'image existante si elle existe
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Ancienne image supprimée : {image_path}")

        # Enregistrer la nouvelle image
        with open(image_path, 'wb') as image_file:
            image_file.write(message.payload)
        print(f"Nouvelle image sauvegardée : {image_filename}")
        latest_image_path = image_path

    elif message.topic == "home/data":
        data_str = message.payload.decode("utf-8")
        data_parts = data_str.split(';')
        data_dict = {p.split('=')[0].strip(): p.split('=')[1].strip() for p in data_parts}
        latest_data = data_dict
        print(f"Data received on 'home/data': {latest_data}")  # Ajouter cette ligne


# Setup MQTT Client
client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker_host, 1883, 60)
for topic in mqtt_topics:
    client.subscribe(topic)

# Run the MQTT client in a separate thread
client.loop_start()

@app.route('/')
def index():
    # Render template with the latest image and data
    return render_template('index2.html', image_path=latest_image_path, data=latest_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, use_reloader=False, threaded=True)
