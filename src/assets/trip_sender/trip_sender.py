from paho.mqtt import client as mqtt_client
from random import Random as random
import time
import json

broker = 'broker.emqx.io'
port = 1883
topic = 'esp/gps'
client_id = f'python-mqtt-879868976'

trip_file = open('trip.json')
trip_data = json.load(trip_file)
trip_file.close



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
     msg_count = 0
     while True:
        time.sleep(1)
        for i in trip_data:
            lat = json.dumps(i["Latitude"])
            lng = json.dumps(i["Longitude"])
            latLng = lat + ',' + lng
            print(latLng)
            client.publish(topic, latLng)
            time.sleep(.25)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()