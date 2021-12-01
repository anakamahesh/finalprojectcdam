'''
Signal Processing
Team Members: Chiara Di Camillo, Anaka Mahesh
'''

import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import math
import os
import sys


import grovepi
from grovepi import *
from grove_rgb_lcd import *

blueled = 3                     # Connect led to digital port D3
redled = 2                      # Connect led to digital port D2
pinMode(redled,"OUTPUT")        # Init output for led
pinMode(blueled,"OUTPUT")       # Init output for led
digitalWrite(redled,0)		      # Init led as off
digitalWrite(blueled,0)		      # Init led as off

MAX_FRQ = 2000
SLICE_SIZE = 0.1 #seconds
WINDOW_SIZE = 0.2 #seconds

max_male_freq = 155
min_male_freq = 85
min_female_freq = 165
max_female_freq = 255

NUMBER_DIC = {}
LOWER_FRQS = []
HIGHER_FRQS = []
FRQ_THRES = 20

def get_max_frq(frq, fft):
    max_frq = 0
    max_fft = 0
    for idx in range(len(fft)):
        if abs(fft[idx]) > max_fft:
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return max_frq

def main(file):
    print("Importing {}".format(file))
    audio = AudioSegment.from_mp3(file)

    sample_count = audio.frame_count()
    sample_rate = audio.frame_rate
    samples = audio.get_array_of_samples()

    #print("Number of channels: " + str(audio.channels))
    #print("Sample count: " + str(sample_count))
    #print("Sample rate: " + str(sample_rate))
    #print("Sample width: " + str(audio.sample_width))

    period = 1/sample_rate                     #the period of each sample
    duration = sample_count/sample_rate         #length of full audio in seconds

    slice_sample_size = int(SLICE_SIZE*sample_rate)   #get the number of elements expected for [SLICE_SIZE] seconds

    n = slice_sample_size                            #n is the number of elements in the slice

    #generating the frequency spectrum
    k = np.arange(n)                                #k is an array from 0 to [n] with a step of 1
    slice_duration = n/sample_rate                   #slice_duration is the length of time the sample slice is (seconds)
    frq = k/slice_duration                          #generate the frequencies by dividing every element of k by slice_duration

    #max_frq_idx = int(MAX_FRQ*slice_duration)       #get the index of the maximum frequency (2000)
    frq = frq[range(max_frq_idx)]                   #truncate the frequency array so it goes from 0 to 2000 Hz

    start_index = 0                                 #set the starting index at 0
    end_index = start_index + slice_sample_size      #find the ending index for the slice
    #output = ''

    print()
    i = 1
    while end_index < len(samples):
        #print("Sample {}:".format(i))
        i += 1

        #TODO: grab the sample slice and perform FFT on it
        sample_slice = samples[start_index: end_index]
        sample_slice_fft = np.fft.fft(sample_slice)/n

        #TODO: truncate the FFT to 0 to 2000 Hz
        sample_slice_fft = sample_slice_fft[range(2000)]

        result = get_max_frq(frq, abs(sample_slice_fft))

        if (min_male_freq < result < max_male_freq):
          digitalWrite(ledred,0)
          digitalWrite(ledblue,1)
        elif (min_female_freq < result < max_female_freq):
          digitalWrite(ledblue,0)
          digitalWrite(ledred,1)

        #TODO: calculate the locations of the upper and lower FFT peak using get_peak_frqs()
        #lower_frq, higher_frq = get_peak_frqs(frq, sample_slice_fft)
        
        #TODO: print the values and find the number that corresponds to the numbers
        #print('Lower peak freq: ' + str(lower_frq))
        #print('Higher peak freq: ' + str(higher_frq))
        #value = get_number_from_frq(lower_frq, higher_frq)
        #print('Number: ' + str(value))
        #output = str(output) + str(value)   # update sequence of numbers for output

        #Incrementing the start and end window for FFT analysis
        start_index += int(WINDOW_SIZE*sample_rate)
        end_index = start_index + slice_sample_size

    print("Program completed")
    #print("Decoded input: " + str(output))

if __name__ == '__main__':
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print("Usage: decode.py [file]")
        exit(1)
    main(sys.argv[1])
