"""
Title: Fly Shaker GUI
Author: Johnny Duong
Creation Date: Feb 1st, 2023
Editor: [To Future Editors, delete this note and put your name here]

Description:
GUI using Thomas Zimmerman's wave generator code for Dr. Divya Sitaraman's drosophila melanogaster sleep research.

[Note: Put in Tom's CCC and IBM funding section here.]

TODO:
-Put in tooltips?

-Disable input boxes based on Radio Sine/Pulse selection?
Possible solutions to that:
https://www.pysimplegui.org/en/latest/cookbook/#recipe-collapsible-sections-visible-invisible-elements
https://stackoverflow.com/questions/61006988/hiding-and-unhiding-text-input-and-filebrowse-in-pysimplegui
https://www.pysimplegui.org/en/latest/call%20reference/#input-element

-Preview wave form?
-Change duration so it can be float? How to check for floating values in str?
-Play audio sample for x seconds regardless of length? (1 seconds)
https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python
https://www.geeksforgeeks.org/python-check-for-float-string/

Changelog:
4-8-2023: Made Pulse Specs match Sine Specs, added in Duty Cycle. Added in Random Burst checkbox and code.
          Added in updated Pulse Spec image to match Sine more.
          Updated module_wave_gen with test code and more functions for flexibility.
          Commented out threading and processing due to potential bugs.
          To stop the GUI, you will have to use Task Manager to End it, or if using an IDE, stopping it through that.
3-10-2023: Fixed main thread bug, just put in flag for Stop Experiment Button.
3-10-2023: Version 1 complete. Sine/Pulse wave creation works and experiment works.
2-11-2023: Added in sine/pulse specifications and radio.
           Put sections in frames, spec/img to columns.
           Put in image loading that is OS independent, but untested on non-Windows.
           Put in number check for input boxes
2-1-2023: Initial Creation

Sources for code ideas:
https://www.tutorialspoint.com/pysimplegui/pysimplegui_frame_element.htm
https://www.pysimplegui.org/en/latest/cookbook/
https://csveda.com/pysimplegui-column-and-frame/
https://stackoverflow.com/questions/57596338/load-an-image-that-is-in-a-subfolder-using-pygame

https://www.pysimplegui.org/en/latest/call%20reference/#input-element

Possible solution for getting/setting cursor position
https://stackoverflow.com/questions/65923933/pysimplegui-set-and-get-the-cursor-position-in-a-multiline-widget

"""

import cv2
import os
import PySimpleGUI as sg
import random
import threading
import time

from multiprocessing import Process

# Import modules
import module_wave_gen as W

# Get full directory of where this file is, used for image loading.
sourceFileDir = os.path.dirname(os.path.abspath(__file__))
imgFolderDir = "img"

# WAVE TYPE SELECTION
# RADIO TEXT/KEYs
SINE = 'Sine'
PULSE = 'Pulse'
GROUP_ID = "RADIO1"

# CHECKBOX KEY
RANDOM_BURST_KEY = "-=RANDOM BURST=-"

# -----------------------
# SINE SPECIFICATIONS
# -----------------------
# Note: "DEF" means "Default"
FREQ_KEY = "-FREQ-"
FREQ_DEF = "200"
AMP_KEY = "-AMP-"
AMP_DEF = "50"
DUR_KEY = "-DURATION-"
DUR_DEF = "1"
BURST_SINE_KEY = "-BURST-"
BURST_SINE_DEF = "1"
SINE_KEYS = [FREQ_KEY, AMP_KEY, DUR_KEY, BURST_SINE_KEY]
SINE_DEFAULTS = [FREQ_DEF, AMP_DEF, DUR_DEF, BURST_SINE_DEF]

# AMP Min/Max values, Actual Version
# Used for the "to" part of MAP function in the module_wave_gen.py
# underscores can be used as a "comma", but it's more for the human since the
AMP_ACTUAL_MAX = 32_000
AMP_ACTUAL_MIN = 1

# AMP Min/Max values, User Version, what the user sees in the GUI
# Used for the "from" part of MAP function in the module_wave_gen.py
AMP_USER_MAX = 100
AMP_USER_MIN = 1

# Windows version to access the sine_wave image in the "img" folder
# If os.path.join fails, uncomment this next line, but comment the other one to make the image loading work
# SINE_IMG = "img/sine_wave.png"

# OS Independent way to get the "img" folder. Should work, but untested on Mac and Linux
# Note: If you change the "img" folder name or location, this will crash the GUI.
SINE_IMG = os.path.join(sourceFileDir, imgFolderDir, 'sine_wave.png')

# -----------------------
# PULSE SPECIFICATIONS
# -----------------------
# Note: "P" means "Pulse", "DEF" means "Default Value"
PULSE_FREQ_KEY = "-PULSE FREQ-"
PULSE_FREQ_DEF = "50"
AMP_P_KEY = "-PULSE AMPLITUDE-"
AMP_P_DEF = "10"
DUTY_CYCLE_KEY = "-DUTY CYCLE-"
DUTY_CYCLE_DEF = "50"
DUR_P_KEY = "-PULSE DURATION-"
DUR_P_DEF = "1"
BURST_P_KEY = "-PULSE BURST PERIOD-"
BURST_P_DEF = "1"


# ===== START OLD to be deleted ======
WIDTH_KEY = "-PULSE WIDTH-"
WIDTH_DEF = "250"
PERIOD_KEY = "-PULSE PERIOD-"
PERIOD_DEF = "500"
COUNT_KEY = "-PULSE COUNT-"
COUNT_DEF = "200"

# PULSE_KEYS = [WIDTH_KEY, PERIOD_KEY, AMP_P_KEY, COUNT_KEY, DUR_P_KEY, BURST_P_KEY]
# PULSE_DEFAULTS = [WIDTH_DEF, PERIOD_DEF, AMP_P_DEF, COUNT_DEF, DUR_P_DEF, BURST_P_DEF]

# ===== END OLD to be deleted ======

PULSE_KEYS = [PULSE_FREQ_KEY, AMP_P_KEY, DUTY_CYCLE_KEY, DUR_P_KEY, BURST_P_KEY]
PULSE_DEFAULTS = [PULSE_FREQ_DEF, AMP_P_DEF, DUTY_CYCLE_DEF, DUR_P_DEF, BURST_P_DEF]

# Windows version to access the pulse_wave image in the "img" folder
# If os.path.join fails, uncomment this next line, but comment the other one to make the image loading work
# PULSE_IMG = "img/pulse_wave.png"

# OS Independent way to get the "img" folder. Should work, but untested on Mac and Linux
# Note: If you change the "img" folder name or location, this will crash the GUI.
PULSE_IMG = os.path.join(sourceFileDir, imgFolderDir, 'pulse_wave2.png')

# Button Text
PLAY_AUDIO_BUTTON = "Play Audio Sample"
# STOP_BUTTON = "Stop Audio"
# PLOT_BUTTON = "Plot Waveform"

START_EXPERIMENT = "Start Experiment"
STOP_EXPERIMENT = "Stop Experiment"
BUTTON_EVENTS = [PLAY_AUDIO_BUTTON, START_EXPERIMENT, STOP_EXPERIMENT]

# Experiment Run Time
HOURS_EXP_DEF = "0"
HOURS_EXP_KEY = "-HOURS EXP-"
MIN_EXP_DEF = "1"
MIN_EXP_KEY = "-MIN EXP-"

# STOP IMAGE (for when there is silence in audio)
# Windows version to access the pulse_wave image in the "img" folder
# If os.path.join fails, uncomment this next line, but comment the other one to make the image loading work
# STOP_IMG = "img/stop_image.png"

# OS Independent way to get the "img" folder. Should work, but untested on Mac and Linux
# Note: If you change the "img" folder name or location, this will crash the GUI.
STOP_IMG = os.path.join(sourceFileDir, imgFolderDir, 'stop_image.png')


# ==== Non-GUI Variables ====
is_running_experiment = False


# ---- [START] FUNCTIONS FOR INTEGER CHECK IN INPUT BOXES -----
# TODO: Put in a module


def does_string_have_non_digit(input_string):
    # Helper function for check_for_digits_in_key()
    # Return True if there is at least one non-digit in string, assumes at least 1 char in string
    result = False

    for char in input_string:
        if not char.isdigit():
            result = True
            break
    return result


def get_default_from_key(key_str):
    # Helper function used by check_for_digits_in_key()
    # if accidentally deleting entire input box with a letter or non-digit..
    result = ""

    # Go through Sine keys and defaults,
    # if key matches key_str (input), then store associated value in result
    for key, val in zip(SINE_KEYS, SINE_DEFAULTS):
        if key_str == key:
            result = val

    # Go through Pulse keys and defaults,
    # if key matches key_str (input), then store associated value in result
    for key, val in zip(PULSE_KEYS, PULSE_DEFAULTS):
        if key_str == key:
            result = val

    # Return the resulting value from associated key_str
    return result


# Define function to check an InputText key for digits only
def check_for_digits_in_key(key_str, values, window):
    # print("check_for_digits_in_key")

    # TODO: Figure out how to get cursor location so when deleting character, return cursor to that location.

    # Old version that will only delete non-digits at the start or end, but not in the middle.
    # if len(values[key_str]) and values[key_str][-1] not in ('0123456789'):
    #     # delete last char from input
    #     # print("Found a letter instead of a number")
    #     window[key_str].update(values[key_str][:-1])

    # Go through each character, only return digits
    digit_only_str = ""
    # Only run this if the values[key_str] has at least 1 character in there.
    if len(values[key_str]):
        # Check if at least one non-digit exists in values[key_str]
        #   If it exists, only allow digits in string
        if does_string_have_non_digit(values[key_str]):
            for char in values[key_str]:
                if char.isdigit():
                    # Concatenate
                    digit_only_str = digit_only_str + char
            # Update that InputText with removed letters

            if len(digit_only_str) == 0:
                # If accidentally replacing all with a letter, replace with default
                # TODO: Figure out how to replace with previous value
                # window[key_str].update("1")
                window[key_str].update(get_default_from_key(key_str))
            else:
                # Otherwise, put in the digital only string.
                window[key_str].update(digit_only_str)


def check_input_keys_for_non_digits(values, window):
    # Check Sine Wave Specifications for non-digits and removing them
    for key_str in SINE_KEYS:
        check_for_digits_in_key(key_str, values, window)

    # Check Pulse Wave Specifications for non-digits and removing them
    for key_str in PULSE_KEYS:
        check_for_digits_in_key(key_str, values, window)


# ---- [END] FUNCTIONS FOR INTEGER CHECK IN INPUT BOXES -----


# ---- [START] FUNCTIONS FOR Sine/Pulse input disabling -----
def check_radio(window, values):
    if values[SINE] == True:

        # Enable Sine inputs
        for key in SINE_KEYS:
            window[key].update(disabled=False)

        # Disable Pulse inputs
        for key in PULSE_KEYS:
            window[key].update(disabled=True)

    else:
        # Disable Sine inputs
        for key in SINE_KEYS:
            window[key].update(disabled=True)

        # Enable Pulse inputs
        for key in PULSE_KEYS:
            window[key].update(disabled=False)


# ---- [END] FUNCTIONS FOR Sine/Pulse input disabling -----


def get_layout():
    # Separate function to create/get the layout for the GUI

    # Sine, Column 1
    sine_col1_layout = [[sg.Push(), sg.Text("Frequency (10 to 200 Hz):"),
                         sg.InputText(default_text=FREQ_DEF, size=(4, 1), key=FREQ_KEY)],
                        [sg.Push(), sg.Text("Amplitude (1 to 100):"),
                         sg.InputText(default_text=AMP_DEF, size=(4, 1), key=AMP_KEY)],
                        [sg.Push(), sg.Text("Duration (seconds):"),
                         sg.InputText(default_text=DUR_DEF, size=(4, 1), key=DUR_KEY)],
                        [sg.Push(), sg.Text("Burst Period (seconds):"),
                         sg.InputText(default_text=BURST_SINE_DEF, size=(4, 1), key=BURST_SINE_KEY)]
                        ]

    # Sine, Column 2
    sine_col2_img_layout = [[sg.Image(SINE_IMG)]]

    # Create Sine Column Layout
    sine_col_layout = [[sg.Column(sine_col1_layout), sg.Column(sine_col2_img_layout)]]

    # Put 2 columns into a frame (gives that box shape)
    sine_frame = sg.Frame("Sine Specifications", layout=sine_col_layout)

    # Pulse, Column 1
    # pulse_col1_layout = [[sg.Push(), sg.Text("Width (msec):"),
    #                       sg.InputText(default_text=WIDTH_DEF, disabled=False, size=(4, 1), key=WIDTH_KEY)],
    #                      [sg.Push(), sg.Text("Period (msec):"),
    #                       sg.InputText(default_text=PERIOD_DEF, size=(4, 1), key=PERIOD_KEY)],
    #                      [sg.Push(), sg.Text("Amplitude (1 to 100):"),
    #                       sg.InputText(default_text=AMP_P_DEF, size=(4, 1), key=AMP_P_KEY)],
    #                      [sg.Push(), sg.Text("Count (1 to 32,000):"),
    #                       sg.InputText(default_text=COUNT_DEF, size=(4, 1), key=COUNT_KEY)],
    #                      [sg.Push(), sg.Text("Duration (seconds):"),
    #                       sg.InputText(default_text=DUR_P_DEF, size=(4, 1), key=DUR_P_KEY)],
    #                      [sg.Push(), sg.Text("Burst Period (seconds):"),
    #                       sg.InputText(default_text=BURST_P_DEF, size=(4, 1), key=BURST_P_KEY)]
    #                      ]

    pulse_col1_layout = [[sg.Push(), sg.Text("Frequency (10 to 200 Hz):"),
                          sg.InputText(default_text=PULSE_FREQ_DEF, disabled=False, size=(4, 1), key=PULSE_FREQ_KEY)],
                         [sg.Push(), sg.Text("Amplitude (1 to 100):"),
                          sg.InputText(default_text=AMP_P_DEF, size=(4, 1), key=AMP_P_KEY)],
                         [sg.Push(), sg.Text("Duty Cycle (1% to 99%):"),
                          sg.InputText(default_text=DUTY_CYCLE_DEF, size=(4, 1), key=DUTY_CYCLE_KEY)],
                         [sg.Push(), sg.Text("Duration (seconds):"),
                          sg.InputText(default_text=DUR_P_DEF, size=(4, 1), key=DUR_P_KEY)],
                         [sg.Push(), sg.Text("Burst Period (seconds):"),
                          sg.InputText(default_text=BURST_P_DEF, size=(4, 1), key=BURST_P_KEY)]
                         ]

    # Pulse, Column 2
    pulse_col2_img_layout = [[sg.Image(PULSE_IMG)]]

    # Create Pulse Column Layout
    pulse_col_layout = [[sg.Column(pulse_col1_layout), sg.Column(pulse_col2_img_layout)]]

    # Put 2 columns into a frame (gives that box shape)
    pulse_frame = sg.Frame("Pulse Specifications", layout=pulse_col_layout)

    # Experiment Layout
    exp_layout = [[sg.Text("How long do I run the experiment?")],
                  [sg.Push(), sg.Text("Hours:"), sg.Input(default_text="0", size=(4, 1), key=HOURS_EXP_KEY)],
                  [sg.Push(), sg.Text("Min:"), sg.Input(default_text="1", size=(4, 1), key=MIN_EXP_KEY)],
                  [sg.Button(START_EXPERIMENT), sg.Button(STOP_EXPERIMENT, disabled=True)]
                  ]

    exp_frame = sg.Frame("Experiment Parameters", layout=exp_layout)

    # Setup Layout
    layout = [[sg.Text('Choose a Wave Type (Sine or Pulse):'),
               sg.Radio(SINE, group_id=GROUP_ID, key=SINE, default=True),
               sg.Radio(PULSE, group_id=GROUP_ID, key=PULSE),
               sg.Checkbox("Random Burst", default=False, key=RANDOM_BURST_KEY)],
              [sine_frame],
              [pulse_frame],
              [sg.Button(PLAY_AUDIO_BUTTON)],
              [exp_frame]
              ]

    return layout


def get_wave(values):
    # Note: Will only work for sine/pulse. If you use different wave types, this code will need to be changed.
    # Future feature: Store these into a class or dictionary?

    wave_arr = ""

    wave_snd = ""

    # Get is_sine_wave
    is_sine_wave = values[SINE]

    # Get either sine or pulse specfications
    if is_sine_wave:
        print("Sine")

        # For troubleshooting, are the input values accessible?
        # for key in SINE_KEYS:
        #     print(key, ":", values[key])

        amp_user = int(values[AMP_KEY])
        freq = int(values[FREQ_KEY])
        dur = float(values[DUR_KEY])

        # Convert user's AMP selection of 1-100 (user) to 1-32000 (actual)
        amp = W.map_function(amp_user, from_low=AMP_USER_MIN, from_high=AMP_USER_MAX,
                             to_low=AMP_ACTUAL_MIN, to_high=AMP_ACTUAL_MAX)

        # sine_arr, sine_snd = W.get_sine_wave(dur=1.0)
        sine_arr, sine_snd = W.get_sine_wave(amp, freq, dur)
        # W.play_audio(sine_snd)
        wave_arr = sine_arr
        wave_snd = sine_snd

    else:
        print("Pulse")

        # For troubleshooting, are the input values accessible?
        for key in PULSE_KEYS:
            print(key, ":", values[key])

        # width_p = int(values[WIDTH_KEY])
        # period_p = int(values[PERIOD_KEY])

        freq_p = int(values[PULSE_FREQ_KEY])
        amp_p_user = int(values[AMP_P_KEY])

        # Convert from int between 1 and 99 to float between 0.01 to 0.99
        duty_cycle_p = int(values[DUTY_CYCLE_KEY]) / 100
        # count_p = int(values[COUNT_KEY])
        dur_p = int(values[DUR_P_KEY])
        burst_p = int(values[BURST_P_KEY])

        # Convert user's AMP selection of 1-100 (user) to 1-32000 (actual)
        amp_p = W.map_function(amp_p_user, from_low=AMP_USER_MIN, from_high=AMP_USER_MAX,
                               to_low=AMP_ACTUAL_MIN, to_high=AMP_ACTUAL_MAX)

        # Get Pulse Wave array and sound array
        # square_arr, square_snd = W.get_pulse_wave(amp=amp_p, period=period_p, pulse_width=width_p, pulse_count=count_p, dur=dur_p)
        pulse_arr, pulse_snd = W.get_pulse_wave2(amp=amp_p, freq=freq_p, duty_cycle=duty_cycle_p, dur=dur_p)
        wave_arr = pulse_arr
        wave_snd = pulse_snd

    # return wave_arr and wave_snd
    return wave_arr, wave_snd


def get_burst(values):
    # Get is_sine_wave
    is_sine_wave = values[SINE]

    # Initialize burst
    burst = 0

    # If sine, get sine burst, convert from seconds to milliseconds
    if is_sine_wave:
        # For Sine
        burst = int(values[BURST_SINE_KEY]) * 1000
    else:
        # For Pulse
        burst = int(values[BURST_P_KEY]) * 1000

    return burst


def get_burst2(values):
    # Get is_sine_wave
    is_sine_wave = values[SINE]

    # Initialize burst
    burst = 0

    # If sine, get sine burst, else get pulse burst (in seconds)
    if is_sine_wave:
        # For Sine
        burst = int(values[BURST_SINE_KEY])
    else:
        # For Pulse
        burst = int(values[BURST_P_KEY])

    return burst


def wait_seconds(time_to_wait):
    # Will use while loop to "wait" in time_to_wait seconds,
    #   allows user to press spacebar on keyboard to stop experiment
    # print("wait_seconds")

    global is_running_experiment

    if time_to_wait <= 0:
        return
    print("======================================")
    print("Press Spacebar to Stop Experiment!")
    print("Will wait", time_to_wait, "seconds")
    print("======================================")

    start_time = time.monotonic()

    elapsed_time = 0

    # Load a dummy image (actual version should say "Press any key or spacebar to stop the silence")
    img = cv2.imread(STOP_IMG)

    while elapsed_time < time_to_wait:

        # time.sleep(1)

        current_time = time.monotonic()
        elapsed_time = current_time - start_time

        # For troubleshooting, check if the loop is actually waiting.
        # print(f"Waited {elapsed_time:.1f} seconds")

        # OpenCV hack to capture keyboard input using an image.
        # Could use another library, but I wanted to use something that would be familiar.
        cv2.imshow("img", img)

        key = cv2.waitKey(1000)

        if key == 32:
            print("You pressed spacebar, stopping experiment!")
            is_running_experiment = False
            break

        # Alternative to above, press any key on the keyboard to break the loop
        # if key >= 0:
        #     print("You pressed any key, breaking loop")
        #     is_running_experiment = False
        #     break

    print(f"Silence elapsed_time: {elapsed_time:.1f} seconds")
    cv2.destroyAllWindows()
    print("End of Loop")
    pass


def start_experiment(window, event, values):
    # Runs the experiment for x hours and y minutes (in a thread)

    global is_running_experiment

    print("===================================================")
    print("Experiment will only STOP after audio is played!")
    print("Note: GUI will look like it is frozen!")
    print("===================================================")

    # Get if Random Burst is selected or not
    is_random_burst_selected = values[RANDOM_BURST_KEY]


    start_time = time.monotonic()
    elapsed_time = 0

    hours_run_time = int(values[HOURS_EXP_KEY])
    min_run_time = int(values[MIN_EXP_KEY])
    expected_run_time = (hours_run_time * 60 * 60) + (min_run_time * 60)
    print("expected_run_time:", expected_run_time, "seconds")

    wave_arr, wave_snd = get_wave(values)
    # W.play_audio(wave_snd)

    # while True:
    #     W.play_audio(wave_snd)
    #     current_time = time.monotonic()

    while elapsed_time < expected_run_time:
        # for i in range(5):
        # Convert burst, from seconds to milliseconds
        # Get burst value depending on sine/pulse selection
        # W.play_audio(wave_snd, burst=get_burst(values))

        # Get playback_time
        # If not doing random burst, will be the actual duration of the audio.
        #   Then enter wait_seconds() for silence loop
        # If doing random burst, playback_time will not exceed actual duration length.
        #   Will need to compare burst value with duration, and use smaller value
        #   IF burst is bigger than actual duration, this value will be silence

        # Random Burst Wave Playback

        # Compare Burst with Duration,
        #   choose smaller for wave playback.
        # If duration smaller than burst, calculate time_to_wait like normal
        # If duration bigger than burst, time_to_wait is zero.


        # Not Random Burst Wave Playback
        # Calculate actual duration of wave audio (number of samples divided by sample rate)
        # Note: You could get it from the GUI, but you would have to check if Sine/Pulse is selected
        #        Then pull the values out, but I wanted the faster coding option.
        #        Suggested idea: use a new function to extract based on Sine/Pulse selection

        # Get dimensions of numpy array
        num_rows, num_col = wave_snd.shape

        # Get duration in seconds
        wave_duration_sec = int(num_rows / W.SAMPLE_RATE_DEFAULT)

        # Get silence time from burst.
        # Math stuff: Burst = Wave_Duration + Time_to_Wait
        #   So solve for Time_to_Wait, Time_to_Wait = Burst - Wave_Duration

        # Convert to seconds
        burst_sec = get_burst2(values)

        # If random burst selected, change burst_sec to a random int between 1 and burst_max (should always be one)
        if is_random_burst_selected == True:
            # For troubleshooting:
            # print("is_random_burst_selected:", is_random_burst_selected)
            # Set burst_max as burst_sec
            burst_max = burst_sec
            print("Random Burst is Selected! Choosing random value between 1 and", burst_max)
            # Choose random int from 1 to burst_sect
            burst_sec = random.randint(1, burst_max)
            print("Random burst_sec:", burst_sec)

        # Compare Burst with Duration,
        #   choose smaller for wave playback.
        # If duration smaller than burst, calculate time_to_wait like normal
        # If duration bigger than burst, time_to_wait is zero.
        if burst_sec < wave_duration_sec:
            wave_duration_ms = int(1000 * burst_sec)
        else:
            wave_duration_ms = int(1000 * wave_duration_sec)

        # Calculate time_to_wait
        time_to_wait = burst_sec - wave_duration_sec

        # Convert to milliseconds since W.play_audio2() needs it in milliseconds
        print("Will play audio for:", wave_duration_ms / 1000, "seconds")

        # Play Audio and Wait Section
        # Play the audio to the desired duration
        W.play_audio2(wave_snd, playback_time=wave_duration_ms)

        # Actively wait the desired time (can press spacebar to end entire experiment)
        # Note: if time_to_wait is negative because of random burst,
        # function will run so fast that almost no time will go by.
        wait_seconds(time_to_wait)

        if not is_running_experiment:
            print(event, "was pressed")
            print("Stopping experiment after playing current audio sample")
            break

        current_time = time.monotonic()
        elapsed_time = current_time - start_time
        print("Experiment elapsed_time:", elapsed_time, "second(s)")

    print(f"Experiment has run for {elapsed_time:.2f} seconds")
    # Convert seconds to hours
    hours_elapsed = elapsed_time / 60 / 60

    # Get the decimal hours (everything after the decimal, e.g. 5.2 hours so extract the 0.2)
    #   This is the % 1, or mod 1 portion.
    # Then convert to minutes by multiplying by 60
    min_elapsed = (hours_elapsed % 1) * 60
    print(f"or {hours_elapsed:.1f} hour(s) and {min_elapsed:.1f} minute(s)")

    set_stop_experiment_variables_and_buttons(window)

    pass


def set_start_experiment_variables_and_buttons(window):
    # Used when "Start Experiment" button is pressed
    global is_running_experiment

    # Used for stopping/starting the thread
    # (allows user to have access to the main GUI when it would normally be frozen).
    is_running_experiment = True
    # print("is_running_experiment:", is_running_experiment)
    # Disable Start Experiment Button, Enable Stop Experiment Button
    window[START_EXPERIMENT].update(disabled=True)
    window[STOP_EXPERIMENT].update(disabled=False)
    window[PLAY_AUDIO_BUTTON].update(disabled=True)
    pass


def set_stop_experiment_variables_and_buttons(window):
    # Used when "Stop Experiment" button is pressed or when the experiment is over.
    global is_running_experiment

    # Used for stopping/starting the thread
    # (allows user to have access to the main GUI when it would normally be frozen).
    is_running_experiment = False
    # Disable Stop Experiment Button, Enable Start Experiment Button
    window[START_EXPERIMENT].update(disabled=False)
    window[STOP_EXPERIMENT].update(disabled=True)
    window[PLAY_AUDIO_BUTTON].update(disabled=False)
    pass


def event_manager(window, event, values):
    global is_running_experiment
    # Get Sine/Pulse Radio selection.
    # If Sine is selected, values[SINE] will be true.
    is_sine_wave = values[SINE]

    p = Process()

    print(RANDOM_BURST_KEY, ":", values[RANDOM_BURST_KEY])

    if event == PLAY_AUDIO_BUTTON:
        print("You pressed", event)
        # Where Tom's Code will be accessed.

        # wave_arr is for plotting, wave_snd is for playing sound
        wave_arr, wave_snd = get_wave(values)
        W.play_audio(wave_snd, get_burst(values))

    elif event == START_EXPERIMENT:
        set_start_experiment_variables_and_buttons(window)
        print("You pressed", event)

        # TODO: Add in a audio playback manager since there is redundancy with the "Play Audio" section.

        # Extract experiment time in hours and minutes.

        # Put in Elapsed time experiment ran?
        # wave_arr, wave_snd = get_wave(values)
        # W.play_audio(wave_snd)
        # start_experiment(values)
        print(f"Will run experiment for {values[HOURS_EXP_KEY]} hour(s) and {values[MIN_EXP_KEY]} minute(s)")

        # Non-Thread, Non-Process Version
        start_experiment(window, event, values)

        # Thread Version
        # experiment_thread = threading.Thread(target=start_experiment, args=(window, event, values), daemon=True)
        # experiment_thread.start()
        # time.sleep(5)

        # Process Version (Should allow user to actually Stop Experiment whenever they want)
        # Current bug: GUI elements cannot be pickled.
        #   Two possible solutions: (1) put relevant values into a dictionary or (2) use pathos multiprocessing
        # p = Process(target=start_experiment, args=(window, event, values,))
        # p.start()

    elif event == STOP_EXPERIMENT:
        # set_stop_experiment_variables_and_buttons(window)
        is_running_experiment = False
        print("You pressed", event)

        # Process Version
        # p.terminate()

        # Stop experiment_thread (not needed, but line may be needed later for troubleshooting if it crashes).

        # experiment_thread.join(timeout=1)
    # TODO: Decide to keep or remove the following buttons (stop, plot):
    # elif event == STOP_BUTTON:
    #     print("You pressed", event)
    # elif event == PLOT_BUTTON:
    #     print("You pressed", event)
    # amp = int(values[AMP_KEY])
    # freq = int(values[FREQ_KEY])
    # dur = float(values[DUR_KEY])
    #
    # sine_arr, sine_snd = W.get_sine_wave(amp, freq, dur)
    # W.plot_waveform(sine_arr, dur)
    # # BUG: Shrinks GUI. Maybe use PySimpleGUI to plot it. Or don't have this button at all.

    pass


def main():
    print("main")

    # Setup Theme
    sg.theme('DarkGrey')

    # Create Window, call get_layout() to get layout.
    window = sg.Window('FlyShaker GUI', get_layout())


    # Initialize empty experiment_thread object, will be used with "Start Experiment" is pushed
    # experiment_thread = threading.Thread()

    # Event Loop to process "events" and get the "values" of the inputs

    # While Loop
    while True:
        event, values = window.read(timeout=10)

        # Make sure input boxes only have digits
        check_input_keys_for_non_digits(values, window)

        # Checks if Sine or Pulse is selected, then disables the non-selected input boxes.
        # For example, if Sine is selected, then Pulse Specification's input boxes are disabled (no input allowed).
        check_radio(window, values)

        if event == sg.WIN_CLOSED:
            break
        elif event in BUTTON_EVENTS:
            event_manager(window, event, values)

    # Close Window after breaking out of loop
    window.close()


if __name__ == "__main__":
    main()
