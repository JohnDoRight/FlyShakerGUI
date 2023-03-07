"""
Title: Fly Shaker GUI
Author: Johnny Duong
Creation Date: Feb 1st, 2023
Editor: [To Future Editors, delete this note and put your name here]

Description:
GUI using Thomas Zimmerman's wave generator code for Dr. Divya Sitaraman's drosophila melanogaster sleep research.

[Note: Put in Tom's CCC and IBM funding section here.]

TODO:
-Have time elapsed, start/end time for playing/stopping waveform
-TODO: Put hours/min into a frame and right-aligned. Maybe the Start/Stop Button too
-Disable input boxes based on Radio Sine/Pulse selection?
Possible solutions to that:
https://www.pysimplegui.org/en/latest/cookbook/#recipe-collapsible-sections-visible-invisible-elements
https://stackoverflow.com/questions/61006988/hiding-and-unhiding-text-input-and-filebrowse-in-pysimplegui
https://www.pysimplegui.org/en/latest/call%20reference/#input-element

-Preview wave form?
-Change duration so it can be float? How to check for floating values in str?
-Play audio sample for x seconds regardless of length? (1 seconds)

Changelog:
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

import os
import PySimpleGUI as sg
import threading
import time

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

# SINE SPECIFICATIONS
# Note: "DEF" means "Default"
FREQ_KEY = "-FREQ-"
# FREQ_DEF = "10"
FREQ_DEF = "200"
AMP_KEY = "-AMP-"
# AMP_DEF = "1"
AMP_DEF = "16000"
DUR_KEY = "-DURATION-"
DUR_DEF = "1"
BURST_SINE_KEY = "-BURST-"
BURST_SINE_DEF = "1"
SINE_KEYS = [FREQ_KEY, AMP_KEY, DUR_KEY, BURST_SINE_KEY]
SINE_DEFAULTS = [FREQ_DEF, AMP_DEF, DUR_DEF, BURST_SINE_DEF]

# Windows version to access the sine_wave image in the "img" folder
# If os.path.join fails, uncomment this next line, but comment the other one to make the image loading work
# SINE_IMG = "img/sine_wave.png"

# OS Independent way to get the "img" folder. Should work, but untested on Mac and Linux
# Note: If you change the "img" folder name or location, this will crash the GUI.
SINE_IMG = os.path.join(sourceFileDir, imgFolderDir, 'sine_wave.png')

# PULSE SPECIFICATIONS
# Note: "P" means "Pulse"
WIDTH_KEY = "-PULSE WIDTH-"
WIDTH_DEF = "1"
PERIOD_KEY = "-PULSE PERIOD-"
PERIOD_DEF = "1"
AMP_P_KEY = "-PULSE AMPLITUDE-"
AMP_P_DEF = "1"
COUNT_KEY = "-PULSE COUNT-"
COUNT_DEF = "1"
BURST_P_KEY = "-PULSE BURST PERIOD-"
BURST_P_DEF = "1"
PULSE_KEYS = [WIDTH_KEY, PERIOD_KEY, AMP_P_KEY, COUNT_KEY, BURST_P_KEY]
PULSE_DEFAULTS = [WIDTH_DEF, PERIOD_DEF, AMP_P_DEF, COUNT_DEF, BURST_P_DEF]

# Windows version to access the pulse_wave image in the "img" folder
# If os.path.join fails, uncomment this next line, but comment the other one to make the image loading work
# PULSE_IMG = "img/pulse_wave.png"

# OS Independent way to get the "img" folder. Should work, but untested on Mac and Linux
# Note: If you change the "img" folder name or location, this will crash the GUI.
PULSE_IMG = os.path.join(sourceFileDir, imgFolderDir, 'pulse_wave.png')

# Button Text
PLAY_AUDIO_BUTTON = "Play Audio Sample"
# STOP_BUTTON = "Stop Audio"
# PLOT_BUTTON = "Plot Waveform"

START_EXPERIMENT = "Start Experiment"
STOP_EXPERIMENT = "Stop Experiment"
BUTTON_EVENTS = [PLAY_AUDIO_BUTTON, START_EXPERIMENT, STOP_EXPERIMENT]

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
    sine_col1_layout = [[sg.Push(), sg.Text("Frequency (10 to 200 Hz):"), sg.InputText(default_text=FREQ_DEF, size=(4, 1), key=FREQ_KEY)],
                        [sg.Push(), sg.Text("Amplitude (1 to 100):"), sg.InputText(default_text=AMP_DEF, size=(4, 1), key=AMP_KEY)],
                        [sg.Push(), sg.Text("Duration (seconds):"), sg.InputText(default_text=DUR_DEF, size=(4, 1), key=DUR_KEY)],
                        [sg.Push(), sg.Text("Burst Period (seconds):"), sg.InputText(default_text=BURST_SINE_DEF, size=(4, 1), key=BURST_SINE_KEY)]
                        ]

    # Sine, Column 2
    sine_col2_img_layout = [[sg.Image(SINE_IMG)]]

    # Create Sine Column Layout
    sine_col_layout = [[sg.Column(sine_col1_layout), sg.Column(sine_col2_img_layout)]]

    # Put 2 columns into a frame (gives that box shape)
    sine_frame = sg.Frame("Sine Specifications", layout=sine_col_layout)

    # Pulse, Column 1
    pulse_col1_layout = [[sg.Push(), sg.Text("Width (msec):"), sg.InputText(default_text=WIDTH_DEF, disabled=False, size=(4, 1), key=WIDTH_KEY)],
                         [sg.Push(), sg.Text("Period (msec):"), sg.InputText(default_text=PERIOD_DEF, size=(4, 1), key=PERIOD_KEY)],
                         [sg.Push(), sg.Text("Amplitude (1 to 100):"), sg.InputText(default_text=AMP_P_DEF, size=(4, 1), key=AMP_P_KEY)],
                         [sg.Push(), sg.Text("Count (1 to 32,000):"), sg.InputText(default_text=COUNT_DEF, size=(4, 1), key=COUNT_KEY)],
                         [sg.Push(), sg.Text("Burst Period (seconds):"), sg.InputText(default_text=BURST_P_DEF, size=(4, 1), key=BURST_P_KEY)]
                         ]

    # Pulse, Column 2
    pulse_col2_img_layout = [[sg.Image(PULSE_IMG)]]

    # Create Pulse Column Layout
    pulse_col_layout = [[sg.Column(pulse_col1_layout), sg.Column(pulse_col2_img_layout)]]

    # Put 2 columns into a frame (gives that box shape)
    pulse_frame = sg.Frame("Pulse Specifications", layout=pulse_col_layout)

    # Setup Layout
    layout = [[sg.Text('Choose a Wave Type (Sine or Pulse):'),
               sg.Radio(SINE, group_id=GROUP_ID, key=SINE, default=True),
               sg.Radio(PULSE, group_id=GROUP_ID, key=PULSE)],
              [sine_frame],
              [pulse_frame],
              [sg.Button(PLAY_AUDIO_BUTTON)],
              [sg.Text("How long do I run the experiment?")],
              [sg.Text("Hours:"), sg.Input(default_text="0", size=(4, 1))],
              [sg.Text("Min:"), sg.Input(default_text="1", size=(4, 1))],
              [sg.Button("Start Experiment"), sg.Button("Stop Experiment", disabled=True)]
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
        for key in SINE_KEYS:
            print(key, ":", values[key])

        amp = int(values[AMP_KEY])
        freq = int(values[FREQ_KEY])
        dur = float(values[DUR_KEY])

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

        width_p = int(values[WIDTH_KEY])
        period_p = int(values[PERIOD_KEY])
        amp_p = int(values[AMP_P_KEY])
        count_p = int(values[COUNT_KEY])
        burst_p = int(values[BURST_P_KEY])

        # Get Pulse Wave array and sound array

    # return wave_arr and wave_snd
    return wave_arr, wave_snd


def start_experiment(window, event, values):
    # Runs the experiment for x hours and y minutes (in a thread)

    global is_running_experiment

    wave_arr, wave_snd = get_wave(values)
    W.play_audio(wave_snd)
    for i in range(5):
        W.play_audio(wave_snd)
        if not is_running_experiment:
            print(event, "was pressed")
            print("Stopping experiment after playing current audio sample")
            break

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
    pass


def event_manager(window, event, values):
    global is_running_experiment
    # Get Sine/Pulse Radio selection.
    # If Sine is selected, values[SINE] will be true.
    is_sine_wave = values[SINE]

    if event == PLAY_AUDIO_BUTTON:
        print("You pressed", event)
        # Where Tom's Code will be accessed.

        # wave_arr is for plotting, wave_snd is for playing sound
        wave_arr, wave_snd = get_wave(values)
        W.play_audio(wave_snd)

    elif event == START_EXPERIMENT:
        set_start_experiment_variables_and_buttons(window)
        print("You pressed", event)

        # TODO: Add in a audio playback manager since there is redundancy with the "Play Audio" section.

        # Extract experiment time in hours and minutes.

        # Put in Elapsed time experiment ran?
        # wave_arr, wave_snd = get_wave(values)
        # W.play_audio(wave_snd)
        # start_experiment(values)

        experiment_thread = threading.Thread(target=start_experiment, args=(window, event, values), daemon=True)
        experiment_thread.start()
        # time.sleep(5)

    elif event == STOP_EXPERIMENT:
        set_stop_experiment_variables_and_buttons(window)
        print("You pressed", event)

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
