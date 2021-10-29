#!/usr/bin/python3
import paho.mqtt.client as mqtt


client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
#ip address of mqtt broker
client.connect("broker.hivemq.com", 8000, 60)



while True:
    try:
        print ("enter command and left and right quantities (ie. MoveTank 10 10)")
        send = str((input()))
        print(f'sending: {send}')
        client.publish("tag/networktest", send)
    except:
        print("put in proper values")

client.disconnect()
