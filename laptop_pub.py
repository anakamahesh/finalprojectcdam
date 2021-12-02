"""EE 250 Final Project
Team: Chiara Di Camillo, Anaka Mahesh
Run laptop_pub.py in a separate terminal on VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard
import sys

IS_ON = False

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press(key):
    global IS_ON
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'a':
        if IS_ON == False:
            IS_ON = True
            print("\nON")
            client.publish("cdam/lcd","ON")            # Send message to rpi
        else:
            return
    elif k == 'b':
        if IS_ON == True:
            IS_ON = False
            print("\nOFF")
            client.publish("cdam/lcd","OFF")             # Send message to rpi
        else:
            return

    if IS_ON == True:
        if (k == 'f'):
            print("\nListening for female voice")
            client.publish("cdam/lcd", "f")   # Send "f" character to rpi
        elif (k == 'm'):
            print("\nListening for male voice")
            client.publish("cdam/lcd", "m")     # Send "m" character to rpi

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
