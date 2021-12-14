#!/usr/bin/python3
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from Funcs_Table import FunctionTable
import datetime
from subprocess import run

def on_connect(client, userdata, flags, rc):
    global logger
    print("Connected with result code " + str(rc))
    client.subscribe("tag/networktest")

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    if(data=="MoveTank 70 70"):
        return

    split = data.find(' ')
    FunctionTable[data[:split]](data[split+1:])
    
    with open("log.txt", 'a') as file:
        file.write(str(datetime.datetime.now()) + " " + str(data) + "\n")

client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
#ip address of mqtt broker
client.connect("192.168.0.160", 11883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
