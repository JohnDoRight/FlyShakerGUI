"""
Wave Generation Module

Based on original code by Thomas (Tom) Zimmerman, IBM Research
and https://stackoverflow.com/a/62250319
MedoAlmasry, Egypt, June 7, 2020

@author Thomas Zimmerman, Johnny Duong

Description:
Wave generation module for sine and pulse waves (aka pulse trains)
to be used in the FlyShakerGUI.

"""

import matplotlib.pyplot as plt
import numpy as np
import pygame

from scipy import signal


def get_sine_wave(amp=16000, freq=200, dur=1.0, sample_rate=44100):
    """
    Generates 2 arrays:
     1. sine_arr: single row vector for plotting
     2. sine_snd: 2 row vector for playing back using pygame.
                  Johnny note: Each vector is a channel, so 2 channels, or stereo.
                               Pygame requires stereo audio
                               even though pygame.mixer is init as 1 channel.
                               Requires further research.

    :param amp: Amplitude of sine wave. Max is 32000 (as per Tom). Default 16000.
    :param freq: Hertz (Hz), Frequency of sine wave (Note: 1/freq is the period).
                 Default 200 for human audible troubleshooting.
    :param dur: The duration of the signal. Default 1.0 seconds.
    :param sample_rate: Hz, number of samples for a second.
                        Default is 44100 Hz.
    :return: sine_arr (for plotting), sine_snd (sound array for playback.
    """

    # Generate time array used to create sine wave (usually the x-axis)

    ts = 1.0/sample_rate  # time step size
    seconds_start = 0
    seconds_end = dur
    t = np.arange(seconds_start, seconds_end, ts)

    # Generate sine wave with amp (how far from zero in the y direction it goes) with sampleRate x values (44100 in this case)
    #  Then normalize it so the x values will be from 0 to 1 in the x direction. Sine formula is Sin(2*pi*freq*x) TODO: Fix the formula.
    #  Generates a horizontal vector
    # Usually the y-axis.
    sine_wave = amp * np.sin(2.0 * np.pi * freq * t)

    # Makes sure sound is 16 bit integers, as pygame.mixer is initialized to 16 bits.
    # Source: https://stackoverflow.com/a/10690879
    #         John, Canada, May 21, 2012
    arr = sine_wave.astype(np.int16)

    # Create pygame.mixer compatible array
    arr2 = np.c_[arr,arr]

    # sine_arr: for plotting (a row vector)
    # sine_snd: sine sound (snd) for audio playback in pygame (2 row vectors, or stereo)
    sine_arr = arr
    sine_snd = arr2
    return sine_arr, sine_snd


def play_audio(snd):
    print("playing audio")
    fade_in=100     # rise time of sound time in milliseconds
    duration=1000   # time in milliseconds
    fade_out=50     # fall time of sound time in milliseconds

    # TODO: Decide where to initialize pygame.mixer (as global?)
    #       Notes: only needs to be initialized once, can put in main.
    # TODO: Figure out where to quit the mixer.
    # Initialize pygame.mixer.init()
    # Refer to pygame docs for more info about each variable:
    # https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.init
    sampling_frequency = 44100
    size = -16
    channels = 1
    buffer = 512
    pygame.mixer.init(sampling_frequency, size, channels, buffer)
    sound = pygame.sndarray.make_sound(snd)
    sound.play(fade_ms=fade_in)
    pygame.time.delay(duration)
    sound.fadeout(fade_out)
    pygame.time.wait(fade_out)
    # pygame.mixer.quit()
    print("Done playing audio")


def main():
    print("main")

    sine_arr, sine_snd = get_sine_wave(dur=1.0)
    play_audio(sine_snd)
    play_audio(sine_snd)
    pass


if __name__ == "__main__":
    main()
