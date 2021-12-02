# Rpi Subscriber
"""EE 250 Final Project
Team: Chiara Di Camillo, Anaka Mahesh
Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import random
import grovepi
from grovepi import *
from grove_rgb_lcd import *

# Define custom callbacks
def callback_lcd(client, userdata, message):
    # Check for correct string formatting
    if str(message.payload, "utf-8") == "ON":
        print("Received a message on", message.topic, ":", str(message.payload, "utf-8"))
        setText_norefresh("Device is ON")
    elif str(message.payload, "utf-8") == "OFF":
        print("Received a message on", message.topic, ":", str(message.payload, "utf-8"))
        setText_norefresh("Device is OFF")
    elif (str(message.payload, "utf-8") == "m") or (str(message.payload, "utf-8") == "f"):
        print("Received a message on", message.topic, ":", str(message.payload, "utf-8"))
        setText_norefresh(str(message.payload, 'utf-8'))

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # Subscribe to topics of interest here
    client.subscribe("cdam/lcd")

    # Add custom callback
    client.message_callback_add("cdam/lcd", callback_lcd)

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

    grovepi.set_bus("RPI_1")  # Set I2C to use the hardware bus

    while True:
        time.sleep(1)
