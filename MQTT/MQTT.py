import paho.mqtt.client as mqtt
import time

mqtt_broker_ip = "127.0.0.1"   #


def on_connect(client, userdata, flags, rc):
    print("Connected!", str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    try:
        inSB = msg.payload  # Get everything in
        inS = inSB.decode("utf-8")

        if msg.topic == 'm':
            if (('A' in inS) | ('C' in inS)):
                return
            _2_data.timeModule().setMotorTime()
                


client = mqtt.Client()


def init():
    try:
        print("Starting MQTT Service")
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(mqtt_broker_ip, 1883)
    except Exception as e:
        print(e)


def sendRequest():
    client.publish("m", 'A' + str(_2_data.motor().getBrakeValue()) + "%")



init()

client.loop_forever()
client.disconnect()
