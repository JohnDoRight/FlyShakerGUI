"""
Title: Fly Shaker GUI
Author: Johnny Duong
Creation Date: Feb 1st, 2023
Editor: [To Future Editors, delete this note and put your name here]

Description:
GUI using Thomas Zimmerman's wave generator code for Dr. Divya Sitaraman's drosophila melanogaster sleep research.

[Note: Put in Tom's CCC and IBM funding section here.]

TODO:
-Do a number check for input boxes.
-Disable input boxes based on Radio Sine/Pulse selection?

Changelog:
2-11-2023: Added in sine/pulse specifications and radio.
           Put sections in frames, spec/img to columns.
           Put in image loading that is OS independent, but untested on non-Windows.
2-1-2023: Initial Creation

Sources for code ideas:
https://www.tutorialspoint.com/pysimplegui/pysimplegui_frame_element.htm
https://www.pysimplegui.org/en/latest/cookbook/
https://csveda.com/pysimplegui-column-and-frame/
https://stackoverflow.com/questions/57596338/load-an-image-that-is-in-a-subfolder-using-pygame
"""

import os
import PySimpleGUI as sg

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
FREQ_DEF = "10"
AMP_KEY = "-AMP-"
AMP_DEF = "1"
DUR_KEY = "-DURATION-"
DUR_DEF = "1"
BURST_SINE_KEY = "-BURST-"
BURST_SINE_DEF = "1"
SINE_KEYS = [FREQ_KEY, AMP_KEY, DUR_KEY, BURST_SINE_KEY]

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

# Windows version to access the pulse_wave image in the "img" folder
# If os.path.join fails, uncomment this next line, but comment the other one to make the image loading work
# PULSE_IMG = "img/pulse_wave.png"

# OS Independent way to get the "img" folder. Should work, but untested on Mac and Linux
# Note: If you change the "img" folder name or location, this will crash the GUI.
PULSE_IMG = os.path.join(sourceFileDir, imgFolderDir, 'pulse_wave.png')


def main():
    print("main")

    # Setup Theme
    sg.theme('TealMono')

    sine_col1_layout = [[sg.Push(), sg.Text("Frequency (10 to 200 Hz):"), sg.InputText(default_text=FREQ_DEF, size=(4, 1), key=FREQ_KEY)],
                        [sg.Push(), sg.Text("Amplitude (1 to 100):"), sg.InputText(default_text=AMP_DEF, size=(4, 1), key=AMP_KEY)],
                        [sg.Push(), sg.Text("Duration (seconds):"), sg.InputText(default_text=DUR_DEF, size=(4, 1), key=DUR_KEY)],
                        [sg.Push(), sg.Text("Burst Period (seconds):"), sg.InputText(default_text=BURST_SINE_DEF, size=(4, 1), key=BURST_SINE_KEY)]
                        ]

    sine_col2_img_layout = [[sg.Image(SINE_IMG)]]

    sine_col_layout = [[sg.Column(sine_col1_layout), sg.Column(sine_col2_img_layout)]]

    sine_frame = sg.Frame("Sine Specifications", layout=sine_col_layout)

    pulse_col1_layout = [[sg.Push(), sg.Text("Width (msec):"), sg.InputText(default_text=WIDTH_DEF, size=(4, 1), key=WIDTH_KEY)],
                    [sg.Push(), sg.Text("Period (msec):"), sg.InputText(default_text=PERIOD_DEF, size=(4, 1), key=PERIOD_KEY)],
                    [sg.Push(), sg.Text("Amplitude (1 to 100):"), sg.InputText(default_text=AMP_P_DEF, size=(4, 1), key=AMP_P_KEY)],
                    [sg.Push(), sg.Text("Count (1 to 32,000):"), sg.InputText(default_text=COUNT_DEF, size=(4, 1), key=COUNT_KEY)],
                    [sg.Push(), sg.Text("Burst Period (seconds):"), sg.InputText(default_text=BURST_P_DEF, size=(4, 1), key=BURST_P_KEY)]
                    ]

    pulse_col2_img_layout = [[sg.Image(PULSE_IMG)]]

    pulse_col_layout = [[sg.Column(pulse_col1_layout), sg.Column(pulse_col2_img_layout)]]

    pulse_frame = sg.Frame("Pulse Specifications", layout=pulse_col_layout)

    # Setup Layout
    layout = [[sg.Text('Choose a Wave Type (Sine or Pulse):')],
              [sg.Radio(SINE, group_id=GROUP_ID, key=SINE, default=True),
               sg.Radio(PULSE, group_id=GROUP_ID, key=PULSE)],
              [sine_frame],
              [pulse_frame],
              [sg.Push(), sg.Button('Generate Waveform')]
              ]

    # Create Window
    window = sg.Window('FlyShaker GUI', layout)

    # Event Loop to process "events" and get the "values" of the inputs

    # While Loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Generate Waveform':
            print("You pressed Generate Waveform")

            if values[SINE] == True:
                print("Sine")
                for key in SINE_KEYS:
                    print(key, ":", values[key])
            else:
                print("Pulse")
                for key in PULSE_KEYS:
                    print(key, ":", values[key])

    #  Get event and values
    #  Check for events.

    # Close Window after breaking out of loop
    window.close()


if __name__ == "__main__":
    main()
