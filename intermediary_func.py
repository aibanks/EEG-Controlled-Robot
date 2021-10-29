import paho.mqtt.client as mqtt
import datetime

def on_connect(client, userdata, flags, rc):
    global logger
    print("Connected with result code " + str(rc))
    client.subscribe("tag/networktest")
    client.subscribe("tag/insight_dat")

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print(f'message recieved: {data}')
    
    send = 'sending function to ev3'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

    with open("log.txt", 'a') as file:
        file.write(str(datetime.datetime.now()) + " " + str(data) + "\n")


client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
#ip address of mqtt broker
client.connect("broker.hivemq.com", 8000, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()