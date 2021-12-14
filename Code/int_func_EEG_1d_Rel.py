import paho.mqtt.client as mqtt
import datetime
import sender_functions_TB as move
import numpy as np
import pandas as pd
import ast
import time


class DataProcessing():
    def __init__(self):
        self.data = pd.DataFrame(columns= ["time","eng.isActive","eng","exc.isActive","exc","lex", "str.isActive","str",
                                            "rel.isActive","rel","int.isActive","int","foc.isActive","foc"])
        self.messageCount = 0
        self.speed = 0
        self.time_init = time.time()

    def updateDataFrame(self, new_dat):
        dat_unpacked = [new_dat["time"]] + new_dat["met"]
        self.data.loc[len(self.data.index)] = dat_unpacked
      
    def relaxation_Mapping(self):
        if self.messageCount > 1:
            rel_previous, rel_current = self.data['rel'][self.messageCount-2:]
            delta = rel_current - rel_previous
            speed_change = round(delta * 100)  # 100 to convert from decimals on EEG to 0-100 scale for speed. Second value: test different values to scale the change
            text = f'Relaxation changed from {rel_previous} to {rel_current}. Updating speed from {self.speed} to '
            self.speed += speed_change
            text += f'{self.speed}.'
            print(text)
            command = move.go_straight(self.speed)
            with open(f'dat_{self.time_init}.csv', "w") as f:
                self.data.to_csv(f, header= True, index=False)

        else:
            command = 'Not enough data, no command sent'
            print(command)
        return command


##  ________________________________________________________

def on_connect(client, userdata, flags, rc):
    global logger
    print("Connected with result code " + str(rc))
    #client.subscribe("tag/networktest")
    client.subscribe("tag/insight_dat")

def on_message(client, userdata, msg):
    global count
    new_data_str = msg.payload.decode()
    print(f'message recieved: {new_data_str}')
    new_data_dict = ast.literal_eval(new_data_str)
    
    dp.messageCount += 1
    dp.updateDataFrame(new_data_dict)
    ev3_command = dp.relaxation_Mapping()

    #client.publish("tag/networktest", send)
    #print(f'published message: {send}')

    with open("log.txt", 'a') as file:
        file.write(str(datetime.datetime.now()) + ' ' + str(new_data_str) + ' ' + str(ev3_command))

dp = DataProcessing()

client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
#ip address of mqtt broker
client.connect("broker.hivemq.com", 8000, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

