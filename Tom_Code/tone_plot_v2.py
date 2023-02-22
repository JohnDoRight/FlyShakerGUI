"""
Created on Thu Sep  1 17:00:56 2022

@author: Tom Zimmerman, IBM Research
based on https://stackoverflow.com/questions/56592522/python-simple-audio-tone-generator
MedoAlmasry, Egypt, June 7, 2020

Direct Link to MedoAlmasry's post: https://stackoverflow.com/a/62250319

@editor: Johnny Duong

TODO:
-Turn into variables/functions: sampleRate, freq, duration, fade_in, fade_out, amp
-Modularize to work with a GUI

"""

import numpy
import pygame
import matplotlib.pyplot as plt

from scipy import signal


sampleRate = 44100
freq = 60
fade_in=100     # rise time of sound time in milliseconds
duration=5000   # time in milliseconds
fade_out=50     # fall time of sound time in milliseconds
amp=4096        # amplitude of sound 4096 is max
amp=16000        # MAX 32000 !


def get_sine_wave(amp, freq, sample_rate):
    # Generate sine wave with amp (how far from zero in the y direction it goes) with sampleRate x values (44100 in this case)
    #  Then normalize it so the x values will be from 0 to 1 in the x direction. Sine formula is Sin(2*pi*freq*x) TODO: Fix the formula.
    #  Generates a horizontal vector
    arr = numpy.array([amp * numpy.sin(2.0 * numpy.pi * freq * x / sample_rate) for x in range(0, sample_rate)]).astype(numpy.int16)
    # Creates 2 duplicate horizontal vectors, stacks them on top of each other. TODO: Figure out why?
    arr2 = numpy.c_[arr,arr]
    return arr, arr2


def get_square_wave(amp, freq, sample_rate):
    # Generate sine wave with amp (how far from zero in the y direction it goes) with sampleRate x values (44100 in this case)
    #  Then normalize it so the x values will be from 0 to 1 in the x direction. Sine formula is Sin(2*pi*freq*x) TODO: Fix the formula.
    #  Generates a horizontal vector
    arr = numpy.array([amp * signal.square(2.0 * numpy.pi * freq * x / sample_rate, duty=0.5) for x in range(0, sample_rate)]).astype(numpy.int16)
    # Creates 2 duplicate horizontal vectors, stacks them on top of each other. TODO: Figure out why?
    arr2 = numpy.c_[arr,arr]
    return arr, arr2


def get_square_wave2(amp, freq, sample_rate):
    # Generate sine wave with amp (how far from zero in the y direction it goes) with sampleRate x values (44100 in this case)
    #  Then normalize it so the x values will be from 0 to 1 in the x direction. Sine formula is Sin(2*pi*freq*x) TODO: Fix the formula.
    #  Generates a horizontal vector

    # sampling interval
    ts = 1.0/sample_rate
    seconds_start = 0
    seconds_end = 10
    t = numpy.arange(seconds_start, seconds_end, ts)

    square_wave = amp * signal.square(2.0 * numpy.pi * freq * t, duty=0.5)
    arr = square_wave.astype(numpy.int16)
    # Creates 2 duplicate horizontal vectors, stacks them on top of each other. TODO: Figure out why?
    arr2 = numpy.c_[arr,arr]
    return arr, arr2


def main3():
    print("main3")

    pygame.mixer.init(44100,-16,1,512)

    PLOT_SAMPLES=1000

    # sampling rate
    sr = 44100
    # sampling interval
    ts = 1.0/sr
    t = numpy.arange(0, 1, ts)

    # frequency of the signal
    freq = 200
    # y = numpy.sin(2*numpy.pi*freq*t)
    y = signal.square(2*numpy.pi*freq*t, duty=0.5)

    plt.figure(figsize = (8, 8))
    plt.subplot(211)
    plt.plot(t[0:PLOT_SAMPLES], y[0:PLOT_SAMPLES], 'b')
    plt.ylabel('Amplitude')

    # freq = 10
    # y = numpy.sin(2*numpy.pi*freq*t)
    amp = 16000
    arr, arr2 = get_square_wave2(amp, freq, sr)
    y = arr[0:PLOT_SAMPLES]

    plt.subplot(212)
    plt.plot(t[0:PLOT_SAMPLES], y, 'b')
    plt.ylabel('Amplitude')

    plt.xlabel('Time (s)')
    plt.show()

    sound = pygame.sndarray.make_sound(arr2)
    sound.play(fade_ms=fade_in)
    pygame.time.delay(duration)

    # Both might be redundant.
    sound.fadeout(fade_out)
    pygame.time.wait(fade_out)


def main2():
    print("main2")
    pygame.mixer.init(44100,-16,1,512)
    # sampling frequency, size, channels, buffer

    # Sampling frequency
    # Analog audio is recorded by sampling it 44,100 times per second,
    # and then these samples are used to reconstruct the audio signal
    # when playing it back.

    # size
    # The size argument represents how many bits are used for each
    # audio sample. If the value is negative then signed sample
    # values will be used.

    # channels
    # 1 = mono, 2 = stereo

    # buffer
    # The buffer argument controls the number of internal samples
    # used in the sound mixer. It can be lowered to reduce latency,
    # but sound dropout may occur. It can be raised to larger values
    # to ensure playback never skips, but it will impose latency on sound playback.

    # this is the frequency range of the speaker
    START_FREQ=10
    STOP_FREQ=100
    STEP_FREQ=10    # frequency steps

    # this you can hear with a laptop speaker
    START_FREQ=200
    STOP_FREQ=500
    STEP_FREQ=100    # frequency steps
    PLOT_SAMPLES=1000

    for f in range(START_FREQ,STOP_FREQ,STEP_FREQ):
        print(f)
        freq=f
        # Generate sine wave with amp (how far from zero in the y direction it goes) with sampleRate x values (44100 in this case)
        #  Then normalize it so the x values will be from 0 to 1 in the x direction. Sine formula is Sin(2*pi*freq*x) TODO: Fix the formula.
        #  Generates a horizontal vector
        # arr = numpy.array([amp * numpy.sin(2.0 * numpy.pi * freq * x / sampleRate) for x in range(0, sampleRate)]).astype(numpy.int16)
        # arr, arr2 = get_sine_wave(amp, freq, sampleRate)

        arr, arr2 = get_square_wave(amp, freq, sampleRate)
        plt.plot(arr[0:PLOT_SAMPLES])
        plt.ylabel('some numbers')
        plt.show()
        # Creates 2 duplicate horizontal vectors, stacks them on top of each other. TODO: Figure out why?
        # arr2 = numpy.c_[arr,arr]
        print(arr.shape)
        print(arr)
        print(arr2.shape)
        sound = pygame.sndarray.make_sound(arr2)
        sound.play(fade_ms=fade_in)
        pygame.time.delay(duration)

        # Both might be redundant.
        sound.fadeout(fade_out)
        pygame.time.wait(fade_out)


def main():
    pygame.mixer.init(44100,-16,1,512)
    # sampling frequency, size, channels, buffer

    # Sampling frequency
    # Analog audio is recorded by sampling it 44,100 times per second,
    # and then these samples are used to reconstruct the audio signal
    # when playing it back.

    # size
    # The size argument represents how many bits are used for each
    # audio sample. If the value is negative then signed sample
    # values will be used.

    # channels
    # 1 = mono, 2 = stereo

    # buffer
    # The buffer argument controls the number of internal samples
    # used in the sound mixer. It can be lowered to reduce latency,
    # but sound dropout may occur. It can be raised to larger values
    # to ensure playback never skips, but it will impose latency on sound playback.

    # this is the frequency range of the speaker
    START_FREQ=10
    STOP_FREQ=100
    STEP_FREQ=10    # frequency steps

    # this you can hear with a laptop speaker
    START_FREQ=200
    STOP_FREQ=500
    STEP_FREQ=100    # frequency steps
    PLOT_SAMPLES=1000

    for f in range(START_FREQ,STOP_FREQ,STEP_FREQ):
        print(f)
        freq=f
        # Generate sine wave with amp (how far from zero in the y direction it goes) with sampleRate x values (44100 in this case)
        #  Then normalize it so the x values will be from 0 to 1 in the x direction. Sine formula is Sin(2*pi*freq*x) TODO: Fix the formula.
        #  Generates a horizontal vector
        arr = numpy.array([amp * numpy.sin(2.0 * numpy.pi * freq * x / sampleRate) for x in range(0, sampleRate)]).astype(numpy.int16)
        plt.plot(arr[0:PLOT_SAMPLES])
        plt.ylabel('some numbers')
        plt.show()
        # Creates 2 duplicate horizontal vectors, stacks them on top of each other. TODO: Figure out why?
        arr2 = numpy.c_[arr,arr]
        print(arr.shape)
        print(arr)
        print(arr2.shape)
        sound = pygame.sndarray.make_sound(arr2)
        sound.play(fade_ms=fade_in)
        pygame.time.delay(duration)

        # Both might be redundant.
        sound.fadeout(fade_out)
        pygame.time.wait(fade_out)


if __name__ == "__main__":
    # main()
    # main2()
    main3()
