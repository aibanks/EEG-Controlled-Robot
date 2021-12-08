import paho.mqtt.client as mqtt
import datetime
import sender_functions_TB as move


count = 0

def on_connect(client, userdata, flags, rc):
    global logger
    print("Connected with result code " + str(rc))
    #client.subscribe("tag/networktest")
    client.subscribe("tag/E4_dat")

def on_message(client, userdata, msg):
    global count
    data = msg.payload.decode()
    print(f'message recieved: {data}')
    
    if count == 0:
        send = move.go_straight(15)
        count += 1
    elif count == 1:
        send = move.stop()
        count += 1
    elif count == 2:
        send = move.go_straight(-15)
        count += 1
    else:
        send = move.stop()
        count = 0

    client.publish("tag/networktest", send)
    print(f'published message: {send}')

    with open("log.txt", 'a') as file:
        file.write(str(datetime.datetime.now()) + " " + str(data) + "\n" + 
        str(datetime.datetime.now()) + str(send))


client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
#ip address of mqtt broker
client.connect("broker.hivemq.com", 8000, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()