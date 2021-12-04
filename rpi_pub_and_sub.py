"""
EE 250 Final Project
RPI Publisher and Subscriber
Team: Chiara Di Camillo, Anaka Mahesh
https://github.com/usc-ee250-fall2021/finalprojectcdam
"""

import paho.mqtt.client as mqtt
import time
import random
import grovepi
from grovepi import *
from grove_rgb_lcd import *

blueled = 3             # Connect to digital port D3
redled = 2              # Connect to digital port D2
buzzer = 5              # Connect to digital port D5
PORT = 4                # Connect to digital port D4

# Define custom callbacks
def callback_lcd(client, userdata, message):    # Print message to LCD
    # Check for correct string formatting
    if str(message.payload, "utf-8") == "RESET":
        print("Message on", message.topic, ":", str(message.payload, "utf-8"))
        setText_norefresh("Device is ON")
    elif (str(message.payload, "utf-8") == "Listen: male") or (str(message.payload, "utf-8") == "Listen: female") or (str(message.payload, "utf-8") == "cdam/lcd","Imposter!"):
        print("Message on", message.topic, ":", str(message.payload, "utf-8"))
        setText_norefresh('\n' + str(message.payload, 'utf-8'))

def callback_lights(client, userdata, message):     # Set lighting - red (represent female match) and blue (represent male match)
    if str(message.payload, "utf-8") == "RED_LIGHTS":          
        print("Message on", message.topic, ":", str(message.payload, "utf-8"))
        setRGB(128, 0, 0)                   # Red
        grovepi.digitalWrite(redled,1)		# Red LED on
        grovepi.digitalWrite(blueled,0)     # Blue LED off
    elif str(message.payload, "utf-8")  == "BLUE_LIGHTS":      
        print("Message on", message.topic, ":", str(message.payload, "utf-8"))
        setRGB(0, 0, 64)                    # Blue
        grovepi.digitalWrite(redled,0)		# Red LED off
        grovepi.digitalWrite(blueled,1)		# Blue LED on
    elif str(message.payload, "utf-8")  == "LIGHTS_OFF":       
        print("Message on", message.topic, ":", str(message.payload, "utf-8"))
        setRGB(0, 0, 0)                     # Turn off LCD backlight color
        grovepi.digitalWrite(redled,0)		# LED off  
        grovepi.digitalWrite(blueled,0)	    # LED off   

def callback_buzzer(client, userdata, message):
    if str(message.payload, "utf-8") == "ON":           
        print("Message on", message.topic, ":", str(message.payload, "utf-8"))
        grovepi.digitalWrite(buzzer,1)		      
    elif str(message.payload, "utf-8")  == "OFF":       
        print("Message on", message.topic, ":", str(message.payload, "utf-8"))
        grovepi.digitalWrite(buzzer,0)		     

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # Subscribe to topics of interest here
    client.subscribe("cdam/lcd")
    client.subscribe("cdam/lights")
    client.subscribe("cdam/buzzer")

    # Add custom callback
    client.message_callback_add("cdam/lcd", callback_lcd)
    client.message_callback_add("cdam/lights", callback_lights)
    client.message_callback_add("cdam/buzzer", callback_buzzer)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    pinMode(redled,"OUTPUT")        # Init output for led
    pinMode(blueled,"OUTPUT")       # Init output for led
    pinMode(buzzer, "OUTPUT")       # Init output for buzzer
    pinMode(PORT, "INPUT")          # Init input for ultrasonic ranger
    digitalWrite(redled,0)		    # Init led as off
    digitalWrite(blueled,0)		    # Init led as off
    grovepi.set_bus("RPI_1")        # Set I2C to use the hardware bus
    setRGB(0, 0, 0)                 # Clear color in LCD backlight

    while True:
        try:
            time.sleep(1)
            ranger_value = grovepi.ultrasonicRead(PORT)     # Read ranger distance
            client.publish("cdam/ultrasonicRanger", str(ranger_value))

        except KeyboardInterrupt:
            # Gracefully shutdown Rpi on Ctrl-C
            setText('')
            setRGB(0, 0, 0)
            digitalWrite(redled,0)
            digitalWrite(blueled,0)	
            digitalWrite(buzzer, 0)

            break
