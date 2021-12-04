"""
EE 250 Final Project
Laptop Publisher
Team: Chiara Di Camillo, Anaka Mahesh
Github link: https://github.com/usc-ee250-fall2021/finalprojectcdam
"""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard
import numpy as np
from pydub import AudioSegment
import signalprocessing

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    # Send corresponding messages to the RPI on designated topic based on key press
    if (k == 'a'): # Reset the LCD Display
        print("\nReset display")
        client.publish("cdam/lcd","RESET")           
        client.publish("cdam/lights", "LIGHTS_OFF")

    if (k == 'f'):  # Check for female voice
        print("\nListening for female voice")
        client.publish("cdam/lcd", "Listen: female")
        result = signalprocessing.main("test.wav")          # Use FFT to get highest peak frq - returns f/m based on if frq is in female/male frq ranges
        print(result)
        if result == 'f':                                   # If returned female - voice and expected gender matches
            client.publish("cdam/lights", "RED_LIGHTS")
        else:                                               # Else returned male - voice and expected gender don't match
            client.publish("cdam/lcd","Imposter!")
            client.publish("cdam/lights", "LIGHTS_OFF")
            client.publish("cdam/buzzer", "ON")
            time.sleep(1)
            client.publish("cdam/buzzer", "OFF")

    elif (k == 'm'):  # Check for male voice
        print("\nListening for male voice")
        client.publish("cdam/lcd", "Listen: male")
        result = signalprocessing.main("test.wav")          # Use FFT to get highest peak frq - returns f/m based on if frq is in female/male frq ranges
        print(result)
        if result == 'm':                                   # If returned female - voice and expected gender matches
            client.publish("cdam/lights", "BLUE_LIGHTS")
        else:                                               # Else returned male - voice and expected gender don't match
            client.publish("cdam/lcd","Imposter!")
            client.publish("cdam/lights", "LIGHTS_OFF")
            client.publish("cdam/buzzer", "ON")
            time.sleep(1)
            client.publish("cdam/buzzer", "OFF")

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
