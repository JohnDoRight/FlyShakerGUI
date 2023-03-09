"""
Wave Generation Module

Based on original code by Thomas (Tom) Zimmerman, IBM Research
and https://stackoverflow.com/a/62250319
MedoAlmasry, Egypt, June 7, 2020

@author Thomas Zimmerman, Johnny Duong

Description:
Wave generation module for sine and pulse waves (aka pulse trains)
to be used in the FlyShakerGUI.

Pulse wave calculations for Duty Cycle and Period from
https://www.youtube.com/watch?v=pFl-swR8BRo
The Organic Chemistry Tutor, 2020

Note: Burst Period can cut into wave creation, so will only be applied on playback.
If Burst Period is larger than Duration, silence will be "added".
If Burst Period is less than Duration, then audio playback will be cut short.

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
                        TODO: Research this, related to pygame.mixer.init()?
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

    # print("before:", sine_wave.shape)
    # Implement burst here
    # Calculate wait time, which is burst - dur
    #   Formula: duration + wait time = burst.
    # wait_time = burst - dur
    # print("wait_time", wait_time)

    # Convert wait time to number of zeroes (silence) to add to the end of sine_wave.
    # Use sample_rate, if want to add 1 second of silence and sample rate is 44100, then 44100 zeroes will be added to the end.
    # N = int(wait_time * sample_rate)
    # print("N:", N)
    # sine_wave = np.pad(sine_wave, (0, N), 'constant', constant_values=1)

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


def get_square_wave(amp=16000, period=1000, pulse_width=500, pulse_count=200, dur=1.0, sample_rate=44100):
    # Recommended inputs:
    #  amp=16000, freq=200, dur=1.0, sample_rate=44100
    #  make freq into pulse count
    #  Duty Cycle = (Pulse Width / Period) * 100%
    #    more inputs: pulse width and period, use these to calculate duty cycle
    #  Note: Burst is for playback

    # Use sine's time array creation
    ts = 1.0/sample_rate  # time step size
    seconds_start = 0
    seconds_end = dur
    t = np.arange(seconds_start, seconds_end, ts)

    # Calculate duty cycle
    duty_cycle = pulse_width / period

    square_wave = amp * signal.square(2.0 * np.pi * pulse_count * t, duty=duty_cycle)

    # Follow the rest of sine function here too.
    arr = square_wave.astype(np.int16)

    # Create pygame.mixer compatible array
    arr2 = np.c_[arr,arr]

    square_arr = arr
    square_snd = arr2
    return square_arr, square_snd


def play_audio(snd, burst=1000):
    # burst, time in milliseconds
    print("playing audio")
    fade_in=100     # rise time of sound time in milliseconds
    duration=1000   # time in milliseconds
    fade_out=50     # fall time of sound time in milliseconds

    # TODO: Decide where to initialize pygame.mixer (as global?)
    #       Notes: only needs to be initialized once, can put in main.
    # TODO: Figure out where to quit the mixer.
    # TODO: Where to put the pygame init constants, at the beginning?
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
    pygame.time.delay(burst)
    sound.fadeout(fade_out)
    pygame.time.wait(fade_out)
    # pygame.mixer.quit()
    print("Done playing audio")


def plot_waveform(wave_arr, plot_samples=1000, dur=1.0, sample_rate=44100):

    # Only plot the first 1000 values
    # PLOT_SAMPLES = 1000

    # Generate time values (x-axis)
    ts = 1.0/sample_rate  # time step size
    seconds_start = 0
    seconds_end = dur
    t = np.arange(seconds_start, seconds_end, ts)


    plt.plot(t[0:plot_samples], wave_arr[0:plot_samples])
    # plt.plot(t, wave_arr)
    # plt.plot(wave_arr)
    plt.ylabel('Amplitude')
    plt.xlabel('Time (s)')
    plt.show()
    plt.close()


def map_function(value, from_low, from_high, to_low, to_high):
    """
    Adpated from Arduino's map function. Link:
    https://www.arduino.cc/reference/en/language/functions/math/map/

    Will be used for mapping values from input range or 1-100 (amplitude, maybe pulse width).

    :param value: int, value you want to change.
    :param from_low: int, minimum or lowest value from input range; e.g. for range 1-100, 1 is the lowest.
    :param from_high: int, maximum or highest value from input range; e.g. for range 1-100, 100 is the highest.
    :param to_low: int, minimum or lowest value from output range; e.g. for range 1-32000, 1 is the lowest.
    :param to_high: int, maximum or highest value from output range; e.g. for range 1-32000, 32000 is the highest.
    :return: int, value mapped onto output range.
    """
    print("map_function")
    result = (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low
    return int(result)


def audio_playback_manager():
    pass


def main():
    print("main")

    # Test sine wave audio playback
    # sine_arr, sine_snd = get_sine_wave(dur=1.0)
    # play_audio(sine_snd)
    # play_audio(sine_snd)

    # Test sine wave plotting
    # sine_arr, sine_snd = get_sine_wave(dur=1.0)
    # plot_waveform(sine_arr, dur=1.0, sample_rate=44100)
    # play_audio(sine_snd, burst=10000)

    # Test square wave plotting
    # Period and pulse_width are in msec
    # Duty Cycle is pulse_width / period, and is a value between 0 and 1
    #   e.g. if you want 0.5 duty cycle (or 50%), pulse_width needs to be half of the period.
    pulse_width=100
    period=1000
    square_arr, square_snd = get_square_wave(period=period, pulse_width=pulse_width, dur=1.0)
    plot_waveform(square_arr, dur=1.0, sample_rate=44100)
    play_audio(square_snd, burst=1000)

    # Test different pulse counts
    # for pulse_count in range(1, 32000, 5000):
    #     square_arr, square_snd = get_square_wave(pulse_count=pulse_count, dur=1.0)
    #     plot_waveform(square_arr, dur=1.0, sample_rate=44100)
    #     play_audio(square_snd, burst=1000)
    #     # TODO: Put in way to smartly detect duty cycle and choose plot sample so square wave is visible?


    # Test map_function
    # value = 41
    # from_low = 0
    # from_high = 100
    # to_low = 0
    # to_high = 32000
    # output = map_function(value, from_low, from_high, to_low, to_high)
    # print("output:", output)

    pass


if __name__ == "__main__":
    main()
