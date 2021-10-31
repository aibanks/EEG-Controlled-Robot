import paho.mqtt.client as mqtt
import datetime
import sender_functions_TB as move
import numpy as np
import pandas as pd


class Intermediary():
    def __init__(self):
        self.data = pd.DataFrame(columns= ["time","eng.isActive","eng","exc.isActive","exc","lex", "str.isActive","str",
                                            "rel.isActive","rel","int.isActive","int","foc.isActive","foc"])
        self.relaxOnly = True
        self.messageCount = 0
        self.speed = 0
        self.client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
        self.client.connect("broker.hivemq.com", 8000, 60)

    def on_connect(self):   #, rc):
        global logger
        print("Connected with result code " + '{testing this part...}') #str(rc))
        self.client.subscribe("tag/insight_dat")

    def updateDataFrame(self, new_dat):
        dat_unpacked = [new_dat["time"]] + new_dat["met"]
        self.data.loc[len(self.data.index)] = dat_unpacked
        
    def relaxation_Mapping(self):
        rel_previous, rel_current = self.data['rel'][self.messageCount-1:]
        delta = rel_current - rel_previous
        speed_change = delta * 5  #test different values to scale the change
        text = f'Updating speed from {self.speed} to '
        self.speed += speed_change
        text += f'{self.speed}.'
        print(text)
        command = move.go_straight(self.speed)
        return command

    def on_message(client,  msg):
        new_data = msg.payload.decode()
        print(f'message recieved: {new_data}')
        self.messageCount += 1
        self.updateDataFrame(new_data)
        if self.messageCount > 1: # Need to enhance for robustness against Null value readings
            send = relaxation_Mapping() # this sends commands to the EV3's MQTT channel, and returns the text string to be logged
        with open("log.txt", 'a') as file:
            file.write(str(datetime.datetime.now()) + " " + str(new_data) + str(send) + "\n")



i = Intermediary()

i.on_connect()

i.on_message()

i.client.loop_forever()

        






#client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
#ip address of mqtt broker
#client.connect("broker.hivemq.com", 8000, 60)

#client.on_connect = on_connect
#client.on_message = on_message

#client.loop_forever()