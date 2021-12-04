EE250 Final Project

By: Chiara Di Camillo and Anaka Mahesh

Link to video demo: https://drive.google.com/file/d/1oSqXkoZKBwmEuEnm5BZn6pMJ6tz8SUxC/view?usp=sharing
Link to git repo: https://github.com/anakamahesh/finalprojectcdam/tree/finalproject/m_audio

Instructions to execute the code: 

1.) The first thing to do when you want to execute the code is that there need to be 4 terminals open in the VM. Each one will correlate to each of the 4 programs that will be run to execute this system. 

2.) The programs that need to be run on different terminals are laptop_pub, laptop_sub, and rpi_pub_and_sub. Each of these programs will connect to a server/broker since we are conducting a pub/sub-model. 

3.) The program laptop_sub will execute the distance sensor; in short, this program will indicate if there is an individual at the door of the housing complex so that the system can start listening to the voice of the individual. On the VM, the terminal will output the distance that the sensor is reading from the rpi and will also indicate if there is a person present. 

4.) When the program laptop_pub and rpi_pub_and_sub run, they will connect to the server, and then the laptop_pub terminal will be ready for the user to start the device using the "a" key and then after clicking the female or male option using "f" or "m" key on the keyboard of the laptop. 

5.) When the "f" key is pressed, then the LCD will light up red with the words "Device is ON. Listen: female". This means that the device is listening to toa female voice and is expecting a voice within the female voice frequency. IF it hears a male voice, then the buzzer will go off and then the LCD will read "IMPOSTER". This means that there is an intruder. 

6.) If we want to switch the scenario (male housing, female intruder), drag back the test.wav file into the f_audio folder and drag out the .wav file from the m_audio folder into the 250finalproject folder. 

7.) Follow the same instruction in step 5 to indicate female intruder. 

8.) For FFT, run the visualization.py on a separate terminal and this will create an FFT graph for the male or female voice frequency ranges.

List of External Libraries used:
We used matplotlib.py, grovepi, time, random, pynput, numpy, pydub. 
