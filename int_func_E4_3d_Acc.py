import paho.mqtt.client as mqtt
import datetime
import sender_functions_TB as move
import numpy as np
import pandas as pd
import ast
import time


class DataProcessing():
    def __init__(self):
        self.data = pd.DataFrame(columns= ["Time","Acc_x","Acc_y","Acc_z", "Left_Speed", "Right_Speed"])
        self.messageCount = 0
        self.time_init = time.time()
        #self.speed = 0

    def updateDataFrame(self, new_dat):
        dat_unpacked = new_dat["Data"]
        print(f'dat_unpacked: {dat_unpacked}')
        dat_unpacked.append('None')
        dat_unpacked.append('None')
        print(dat_unpacked)
        self.data.loc[len(self.data.index)] = dat_unpacked
      
    def accelerometer_Mapping(self):
        if self.messageCount > 1:
            x_previous, x_current = self.data['Acc_x'][self.messageCount-2:]
            y_previous, y_current = self.data['Acc_y'][self.messageCount-2:]
            z_previous, z_current = self.data['Acc_z'][self.messageCount-2:]
            deltas = [x_current - x_previous, y_current - y_previous, z_current - z_previous]

            print(f'y_current: {y_current}')

            if abs(x_current) > abs(y_current):  # more change of direction than speed, we want to increase the effect of y on speed
                if y_current >= 0:  # forward
                    y_current_mod = (abs(x_current)+y_current)/2
                else:       # backwards
                    y_current_mod = (-abs(x_current)+y_current)/2
            else:
                y_current_mod = y_current
            


            new_speed = round(y_current_mod*(100/128))  # Multiply by 100/128 to convert from 0-128 (0-2g) on E4 to 0-100 scale for speed
            new_direction = round(x_current*(180/128)) # Multiply by 180/128 to convert from 0-128 (0-2g) on E4 to -180-180 scale for changing angle

            # Convert change of direction into a left speed and right speed. Turn left when: right speed > left speed.  Turn right when: left speed > right speed
            if new_direction <= 0:  #turn left
                right_speed = new_speed
                left_speed = round(new_speed*(180+new_direction)/180) #Full left speed if new_direction equals 0.  No left speed if new_direction equals 180
            else:   # go straight or turn right
                right_speed = round(new_speed*(180-new_direction)/180)
                left_speed = new_speed

            #text = f'Acc_Y changed from {y_previous} to {y_current}. Updating speed from {self.speed} to '
            #self.speed = new_speed
            #text += f'{self.speed}.'
            #print(text)
            print(f'Updating left speed to {left_speed} and right speed to {right_speed}.')
            command = move.move_bispeed(left_speed, right_speed)
            print(str(command))
            self.data.loc[self.data.index[-1], "Left_Speed"] = left_speed
            self.data.loc[self.data.index[-1], "Right_Speed"] = right_speed
            print(self.data)
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
    client.subscribe("tag/E4_dat")

def on_message(client, userdata, msg):
    global count
    new_data = msg.payload.decode()
    new_data = ast.literal_eval(new_data)
    new_data = new_data[-1]
    print(f'message recieved: {new_data}')
    
    dp.messageCount += 1
    dp.updateDataFrame(new_data)   #taking the last input of the message chunk, can change this
    ev3_command = dp.accelerometer_Mapping()

    #client.publish("tag/networktest", ev3_command)  
    #print(f'published message: {ev3_command}')

    with open("log.txt", 'a') as file:
        file.write(str(datetime.datetime.now()) + ' ' + str(new_data) + ' ' + str(ev3_command))

dp = DataProcessing()

client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
#ip address of mqtt broker
client.connect("broker.hivemq.com", 8000, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

