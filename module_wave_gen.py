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

TODO: Try Pulse Gen following Example 1 from MIT:
https://www.programcreek.com/python/example/100545/scipy.signal.square
"""

import matplotlib.pyplot as plt
import numpy as np
import pygame

from scipy import signal

# Used for calculating duration of wave audio
# TODO: Change code in this module to use this constant
SAMPLE_RATE_DEFAULT = 44100


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

    # sine_arr: for plotting (a vector)
    # sine_snd: sine sound (snd) for audio playback in pygame (2 row vectors, or stereo)
    sine_arr = arr
    sine_snd = arr2
    return sine_arr, sine_snd


def get_pulse_wave(amp=16000, period=1000, pulse_width=500, pulse_count=200, dur=1.0, sample_rate=44100):
    """
    Generates 2 pulse_wave arrays, one for plotting, another for audio playback with PyGame.

    Note: Duty Cycle = Pulse Width / Period. Duty Cycle is a value between 0 and 1,
          you can think of it as a percentage if you multiply the result by 100.
          So 0.5 calculated from the formula above results in 50% duty cycle.

    :param amp: an int, value from 1 to 32,000 (max); no unit. Max amp value found by Thomas Zimmerman.
    :param period: an int, unit: msec (milliseconds). Note: 1000 milliseconds is 1 second.
                   Used in calculating duty cycle. How long the full period of a square wave is.
    :param pulse_width: an int, unit: msec (milliseconds). Used in calculating duty cycle and duration.
                        Determines how wide a pulse s, or how long it is on.
    :param pulse_count: an int, unitless. Value from 1 to 32,000.
                        For wave generation calculation, is treated like frequency.
                        Used in calculating and duration.
    :param dur: a float, unit: seconds. Determines time length of square wave.
                Note: Burst Period in play_audio determines how short or long playback actually is.
    :param sample_rate: Hz, number of samples for a second.
                        Default is 44100 Hz.
    :return: pulse_arr (for plotting), pulse_snd (for audio playback in PyGame, might be stereo)
    """
    # Recommended inputs:
    #  amp=16000, freq=200, dur=1.0, sample_rate=44100
    #  make freq into pulse count
    #  Duty Cycle = (Pulse Width / Period) * 100%
    #    more inputs: pulse width and period, use these to calculate duty cycle
    #  Note: Burst is for playback

    # Calculate duration for creating time array
    # Convert period (msec) to seconds, then multiply by pulse_count
    #  Units are in seconds.
    #  If pulse_count is sufficiently high, this results in a long duration.
    #   So it's good burst period is there to control how long things are played.
    # dur = (period / 1000) * pulse_count
    # print("dur:", dur)
    # Bug: don't do this! Creates a large array that crashed my computer if pulse count is high enough.

    # Use sine's time array creation
    ts = 1.0/sample_rate  # time step size
    seconds_start = 0
    seconds_end = dur
    t = np.arange(seconds_start, seconds_end, ts)

    # Calculate duty cycle
    duty_cycle = pulse_width / period

    # For purposes of calculations, pulse_count is playing role of frequency.
    # Reasoning: I couldn't figure out how to make it work any other way and even scipy.signal uses frequency.
    #            Bug: if using pulse count and period to create time array above,
    #                 it creates a ridiculously long array that causes my computer to crash.
    # Reasoning 2: Pulse Count appears to act similar to Frequency since I think "Frequency Counting" is related, maybe?
    pulse_wave = amp * signal.square(2.0 * np.pi * pulse_count * t, duty=duty_cycle)

    # Makes sure sound is 16 bit integers, as pygame.mixer is initialized to 16 bits.
    # Refer to get_sine_wave() for more details
    arr = pulse_wave.astype(np.int16)

    # Create pygame.mixer compatible array
    arr2 = np.c_[arr,arr]

    # pulse_arr: for plotting (a vector)
    # pulse_snd: square wave sound (snd) for audio playback in pygame (2 vectors, or stereo)
    pulse_arr = arr
    pulse_snd = arr2
    return pulse_arr, pulse_snd


def get_pulse_wave2(amp=16000, freq=200, duty_cycle=0.5, dur=1.0, sample_rate=44100):
    """
    Generates 2 pulse_wave arrays, one for plotting, another for audio playback with PyGame.

    Note: Duty Cycle = Pulse Width / Period. Duty Cycle is a value between 0 and 1,
          you can think of it as a percentage if you multiply the result by 100.
          So 0.5 calculated from the formula above results in 50% duty cycle.

    :param amp: an int, value from 1 to 32,000 (max); no unit. Max amp value found by Thomas Zimmerman.
    :param freq: Hertz (Hz), Frequency of sine wave (Note: 1/freq is the period).
                 Default 200 for human audible troubleshooting.
    :param duty_cycle: a float, value from 0 to 1; no unit.
    :param dur: a float, unit: seconds. Determines time length of square wave.
                Note: Burst Period in play_audio determines how short or long playback actually is.
    :param sample_rate: Hz, number of samples for a second.
                        Default is 44100 Hz.
    :return: pulse_arr (for plotting), pulse_snd (for audio playback in PyGame, might be stereo)
    """

    # Use sine's time array creation
    ts = 1.0/sample_rate  # time step size
    seconds_start = 0
    seconds_end = dur
    t = np.arange(seconds_start, seconds_end, ts)

    # Calculate duty cycle
    # duty_cycle = pulse_width / period
    # Get period from freq
    period = 1 / freq
    print("period:", period * 1000, "msec")
    # Get pulse_width from duty_cycle and period
    pulse_width = duty_cycle * period
    print("pulse_width:", pulse_width * 1000, "msec")
    # Print the results

    # For purposes of calculations, pulse_count is playing role of frequency.
    # Reasoning: I couldn't figure out how to make it work any other way and even scipy.signal uses frequency.
    #            Bug: if using pulse count and period to create time array above,
    #                 it creates a ridiculously long array that causes my computer to crash.
    # Reasoning 2: Pulse Count appears to act similar to Frequency since I think "Frequency Counting" is related, maybe?
    pulse_wave = amp * signal.square(2.0 * np.pi * freq * t, duty=duty_cycle)

    # Makes sure sound is 16 bit integers, as pygame.mixer is initialized to 16 bits.
    # Refer to get_sine_wave() for more details
    arr = pulse_wave.astype(np.int16)

    # Create pygame.mixer compatible array
    arr2 = np.c_[arr,arr]

    # pulse_arr: for plotting (a vector)
    # pulse_snd: square wave sound (snd) for audio playback in pygame (2 vectors, or stereo)
    pulse_arr = arr
    pulse_snd = arr2
    return pulse_arr, pulse_snd


def get_pulse_wave3(amp=16000, period=200, duty_cycle=0.5, dur=1.0, sample_rate=44100):
    """
    Generates 2 pulse_wave arrays, one for plotting, another for audio playback with PyGame.

    Code inspired from https://www.programcreek.com/python/example/100545/scipy.signal.square

    Note: Duty Cycle = Pulse Width / Period. Duty Cycle is a value between 0 and 1,
          you can think of it as a percentage if you multiply the result by 100.
          So 0.5 calculated from the formula above results in 50% duty cycle.

    :param amp: an int, value from 1 to 32,000 (max); no unit. Max amp value found by Thomas Zimmerman.
    :param period: an int, unit: msec.
    :param duty_cycle: a float, value from 0 to 1; no unit.
    :param dur: a float, unit: seconds. Determines time length of square wave.
                Note: Burst Period in play_audio determines how short or long playback actually is.
    :param sample_rate: Hz, number of samples for a second.
                        Default is 44100 Hz.
    :return: pulse_arr (for plotting), pulse_snd (for audio playback in PyGame, might be stereo)
    """

    # Use sine's time array creation
    ts = 1.0/sample_rate  # time step size
    seconds_start = 0
    seconds_end = dur
    t = np.arange(seconds_start, seconds_end, ts)

    # Calculate duty cycle
    # duty_cycle = pulse_width / period
    # Get period from freq
    # Convert period msec to sec (1000 msec = 1 sec)
    period_sec = period / 1000
    freq = 1 / (period_sec)
    print("freq:", freq, "Hz")
    # Get pulse_width from duty_cycle and period
    pulse_width = duty_cycle * period
    print("pulse_width:", pulse_width, "msec")
    # Print the results

    # For purposes of calculations, pulse_count is playing role of frequency.
    # Reasoning: I couldn't figure out how to make it work any other way and even scipy.signal uses frequency.
    #            Bug: if using pulse count and period to create time array above,
    #                 it creates a ridiculously long array that causes my computer to crash.
    # Reasoning 2: Pulse Count appears to act similar to Frequency since I think "Frequency Counting" is related, maybe?
    pulse_wave = amp * signal.square(2.0 * np.pi * t / period_sec, duty=duty_cycle)

    # Makes sure sound is 16 bit integers, as pygame.mixer is initialized to 16 bits.
    # Refer to get_sine_wave() for more details
    arr = pulse_wave.astype(np.int16)

    # Create pygame.mixer compatible array
    arr2 = np.c_[arr,arr]

    # pulse_arr: for plotting (a vector)
    # pulse_snd: square wave sound (snd) for audio playback in pygame (2 vectors, or stereo)
    pulse_arr = arr
    pulse_snd = arr2
    return pulse_arr, pulse_snd


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


def play_audio2(snd, playback_time=1000):
    # playback_time, time in milliseconds
    print("play_audio2")
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
    sound.play()
    pygame.time.delay(playback_time)

    # Fade Out seems to lowers chance for bug where short wave samples play over each other,
    # causing an increase in volume (probably amplitude since it is constructive interference)
    sound.fadeout(fade_out)

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


def main2():

    # Test play_audio2(), will be used in combination of silence waiting
    pulse_arr, pulse_snd = get_pulse_wave2(dur=2.0)

    # Will play audio only for the playback_time in milliseconds,
    # so it can either cut off the audio early or add silence itself
    # But the goal is to have it only audio wave audio, the silence will be handled by another function.
    # play_audio2(pulse_snd, playback_time=1000)
    # play_audio2(pulse_snd, playback_time=1000)

    # Duration calculation test (works, divide number of samples by sample_rate, gets number of seconds of audio)
    audio_sample_rate = 44100
    print(pulse_snd.shape)
    print(pulse_snd)
    # print(len(pulse_arr) / audio_sample_rate)


    pass


def main():
    print("main")

    # --------------------------------
    # Test sine wave audio playback
    # --------------------------------
    # sine_arr, sine_snd = get_sine_wave(dur=1.0)
    # play_audio(sine_snd)
    # play_audio(sine_snd)

    # --------------------------------
    # Test sine wave plotting
    # --------------------------------
    # sine_arr, sine_snd = get_sine_wave(dur=1.0)
    # plot_waveform(sine_arr, dur=1.0, sample_rate=44100)
    # play_audio(sine_snd, burst=10000)

    # --------------------------------
    # Test square wave plotting
    # --------------------------------
    # Period and pulse_width are in msec
    # Duty Cycle is pulse_width / period, and is a value between 0 and 1
    #   e.g. if you want 0.5 duty cycle (or 50%), pulse_width needs to be half of the period.
    # pulse_width = 250 # milliseconds, only used for duty cycle calculation
    # period = 500      # milliseconds, only used for duty cycle calculation
    # pulse_count = 200 # unitless, but treat it as frequency, so Hz
    # burst = 4000      # milliseconds
    # duration = 2.0    # seconds
    # pulse_arr, pulse_snd = get_pulse_wave(period=period, pulse_width=pulse_width, pulse_count=pulse_count, dur=duration)
    # plot_waveform(pulse_arr, dur=duration, sample_rate=44100)
    # play_audio(pulse_snd, burst=burst)

    # --------------------------------
    # Listening test for square and sine with same freq and pulse count.
    # --------------------------------
    # freq = 200
    # sine_arr, sine_snd = get_sine_wave(freq=freq, dur=duration)
    # plot_waveform(sine_arr, dur=duration, sample_rate=44100)
    # play_audio(sine_snd, burst=burst)

    # --------------------------------
    # Pulse Wave: Test same freq, different duty cycle
    # --------------------------------
    # pulse_width = 10 # milliseconds, only used for duty cycle calculation
    # period = 500      # milliseconds, only used for duty cycle calculation
    # pulse_count = 200 # unitless, but treat it as frequency, so Hz
    # burst = 1000      # milliseconds
    # duration = 1.0    # seconds
    #
    # for pulse_width in range(0, period + 50, 50):
    #     print("pulse_width:", pulse_width)
    #     print("duty cycle:", pulse_width / period)
    #     pulse_arr, pulse_snd = get_pulse_wave(period=period, pulse_width=pulse_width, pulse_count=pulse_count, dur=duration)
    #     plot_waveform(pulse_arr, dur=duration, sample_rate=44100)
    #     play_audio(pulse_snd, burst=burst)

    # --------------------------------
    # Pulse Wave 2: Test get_pulse_wave2()
    # --------------------------------
    # freq = 1000
    # duty_cycle = 0.5
    # duration = 1.0
    # burst = 1000
    # pulse_arr, pulse_snd = get_pulse_wave2(amp=16000, freq=freq, duty_cycle=duty_cycle, dur=duration, sample_rate=44100)
    # plot_waveform(pulse_arr, dur=duration, sample_rate=44100)
    # play_audio(pulse_snd, burst=burst)

    # --------------------------------
    # Pulse Wave 3: Test get_pulse_wave3()
    # --------------------------------
    # period = 50      # in msec
    # duty_cycle = 0.5 # unitless, value from 0 to 1
    # duration = 1.0   # in sec
    # burst = 1000     # in msec
    # pulse_arr, pulse_snd = get_pulse_wave3(amp=16000, period=period, duty_cycle=duty_cycle, dur=duration, sample_rate=32000)
    # plot_waveform(pulse_arr, dur=duration, sample_rate=32000)
    # play_audio(pulse_snd, burst=burst)

    # for period in range(1, 50, 1):
    #     print("period:", period, " msec")
    #     pulse_arr, pulse_snd = get_pulse_wave3(amp=16000, period=period, duty_cycle=duty_cycle, dur=duration, sample_rate=44100)
    #     plot_waveform(pulse_arr, dur=duration, sample_rate=44100)
    #     play_audio(pulse_snd, burst=burst)

    # --------------------------------
    # Test different pulse counts
    # --------------------------------
    # for pulse_count in range(1, 32000, 5000):
    #     square_arr, square_snd = get_square_wave(pulse_count=pulse_count, dur=1.0)
    #     plot_waveform(square_arr, dur=1.0, sample_rate=44100)
    #     play_audio(square_snd, burst=1000)
    #     # TODO: Put in way to smartly detect duty cycle and choose plot sample so square wave is visible?

    # --------------------------------
    # Test map_function
    # --------------------------------
    # value = 41
    # from_low = 0
    # from_high = 100
    # to_low = 0
    # to_high = 32000
    # output = map_function(value, from_low, from_high, to_low, to_high)
    # print("output:", output)

    pass


if __name__ == "__main__":
    # main()
    main2()
