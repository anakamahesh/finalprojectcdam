'''
EE 250 Final Project
Signal Processing FFT
Team Members: Chiara Di Camillo, Anaka Mahesh
Github link: https://github.com/usc-ee250-fall2021/finalprojectcdam
'''

import matplotlib.pyplot as plt
import numpy as np
from numpy.core.numeric import full
from pydub import AudioSegment

SLICE_SIZE = 0.1 #seconds
WINDOW_SIZE = 0.2 #seconds

min_male_freq = 100
max_male_freq = 200
min_female_freq = 200
max_female_freq = 300
gender = ''

def get_max_frq(frq, fft):
    max_frq = 0
    max_fft = 0
    for idx in range(len(fft)):
        if abs(fft[idx]) > max_fft:
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return (max_frq,max_fft)

def get_peak_freq(frq, fft):
    vfreq = []
    vfreq_fft = []
    for i in range(len(frq)):
        if (100 < frq[i] < 300):
            vfreq.append(frq[i])
            vfreq_fft.append(fft[i])

    return (get_max_frq(vfreq, vfreq_fft))

def main(file):
    RESULT = []
    global gender
    print("Importing {}".format(file))
    audio = AudioSegment.from_mp3(file)

    sample_count = audio.frame_count()
    sample_rate = audio.frame_rate
    samples = audio.get_array_of_samples()

    period = 1/sample_rate                              #the period of each sample
    duration = sample_count/sample_rate                 #length of full audio in seconds

    slice_sample_size = int(SLICE_SIZE*sample_rate)     #get the number of elements expected for [SLICE_SIZE] seconds

    n = slice_sample_size                               #n is the number of elements in the slice

    #generating the frequency spectrum
    k = np.arange(n)                                    #k is an array from 0 to [n] with a step of 1
    slice_duration = n/sample_rate                      #slice_duration is the length of time the sample slice is (seconds)
    frq = k/slice_duration                              #generate the frequencies by dividing every element of k by slice_duration

    frq = frq[range(800)]                               #truncate the frequency array so it goes from 0 to 800 Hz

    start_index = 0                                     #set the starting index at 0
    end_index = start_index + slice_sample_size         #find the ending index for the slice

    print()
    i = 1
    max_frq=-1
    max_fft=-1
    while end_index < len(samples):
        #print("Sample {}:".format(i))
        i += 1

        #grab the sample slice and perform FFT on it
        sample_slice = samples[start_index: end_index]
        sample_slice_fft = np.fft.fft(sample_slice)/n

        #truncate the FFT to 0 to 2000 Hz
        sample_slice_fft = sample_slice_fft[range(800)]

        voicefreq, voicefft = get_peak_freq(frq, sample_slice_fft)
        if voicefft > max_fft:
            max_frq = voicefreq
            max_fft = voicefft

        #Incrementing the start and end window for FFT analysis
        start_index += int(WINDOW_SIZE*sample_rate)
        end_index = start_index + slice_sample_size

    print(max_frq)
    if (min_male_freq < max_frq < max_male_freq):
        gender = 'm'
    elif (min_female_freq < max_frq < max_female_freq):
        gender = 'f'

    return gender
    print("Program completed")

if __name__ == '__main__':
    main('test.wav')
