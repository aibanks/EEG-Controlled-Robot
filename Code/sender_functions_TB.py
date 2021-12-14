import paho.mqtt.client as mqtt
import time


client = mqtt.Client( protocol=mqtt.MQTTv311,transport="websockets")
#ip address of mqtt broker
client.connect("broker.hivemq.com", 8000, 60)

def go_straight(speed):
    send = f'MoveTank {speed} {speed}'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')
    return send  #may need to add this line to the other functions below

def stop():
    send = 'MoveTank 0 0'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

def go_straight_timed(speed, duration):
    # start by going forward
    send = f'MoveTank {speed} {speed}'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')
    # pause for {duration}, then set speed to 0 to brake
    time.sleep(duration)
    send = 'MoveTank 0 0' 
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

def move_bispeed(left_speed, right_speed):
    send = f'MoveTank {left_speed} {right_speed}'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

def move_bispeed_timed(left_speed, right_speed, duration):
    # start by moving
    send = f'MoveTank {left_speed} {right_speed}'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')
    # pause for {duration}, then set speed to 0 to brake
    time.sleep(duration)
    send = 'MoveTank 0 0' 
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

def turn_around(speed, clockwise = True):
    if clockwise == True:
        send = f'MoveTankRotation {speed} {-speed} 1.7'
    else:
        send = f'MoveTankRotation {-speed} {speed} 1.7'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

def turn_90(speed, clockwise = True):
    if clockwise == True:
        send = f'MoveTankRotation {speed} {-speed} 0.85'
    else:
        send = f'MoveTankRotation {-speed} {speed} 0.85'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

def spin(speed, clockwise = True):
    if clockwise == True:
        send = f'MoveTank {speed} {-speed}'
    else:
        send = f'MoveTank {-speed} {speed}'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

def spin_timed(speed, duration, clockwise = True):
    if clockwise == True:
        send = f'MoveTank {speed} {-speed}'
    else:
        send = f'MoveTank {-speed} {speed}'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')
    # pause for {duration}, then set speed to 0 to brake
    time.sleep(duration)
    send = 'MoveTank 0 0' 
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

def spin_degrees(speed, degrees, clockwise = True):
    constant = 0.00944 # tire rotations per ~1 degree rotation of ev3
    if clockwise == True:
        send = f'MoveTankRotation {speed} {-speed} {constant * degrees}'
    else:
        send = f'MoveTankRotation {-speed} {speed} {constant * degrees}'
    client.publish("tag/networktest", send)
    print(f'published message: {send}')

