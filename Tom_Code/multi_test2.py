# SuperFastPython.com
# example of running a function in another process
from time import sleep
from multiprocessing import Process

import numpy as np
import pygame


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



# a custom function that blocks for a moment
def task(test):
    # block for a moment
    # sleep(1)
    # display a message
    print('This is from another process')
    for i in range(100):
        print("Hello", test)
        sleep(1)


def main():
    # create a process
    # test = 123
    # process = Process(target=task, args=(test,))
    # # run the process
    # process.start()
    # # wait for the process to finish
    # print('Waiting for the process...')
    # # input("press ENTER to stop playback")
    # sleep(5)
    # process.terminate()
    # print("Process Terminated")
    # # process.join()


    sine_arr, sine_snd = get_sine_wave(dur=5.0)
    # play_audio(sine_snd)
    p = Process(target=play_audio, args=(sine_snd, 5000))
    p.start()
    sleep(2)
    p.terminate()



# entry point
if __name__ == '__main__':
    main()