"""
Title: Fly Shaker GUI
Author: Johnny Duong
Creation Date: Feb 1st, 2023
Editor: [To Future Editors, delete this note and put your name here]

Description:
GUI using Thomas Zimmerman's wave generator code for Dr. Divya Sitaraman's drosophila melanogaster sleep research.

[Note: Put in Tom's CCC and IBM funding section here.]

Changelog:
2-1-2023: Initial Creation
"""

import PySimpleGUI as sg

# WAVETYPE SELECTION
# RADIO TEXT/KEYs
SINE = 'Sine'
PULSE = 'Pulse'
GROUP_ID = "RADIO1"

# SINE SPECIFICATIONS
FREQ_KEY = "-FREQ-"
FREQ_DEFAULT = "10"
AMP_KEY = "-AMP-"
AMP_DEFAULT = "1"
DUR_KEY = "-DURATION-"
DUR_DEFAULT = "1"
BURST_SINE_KEY = "-BURST-"
BURST_SINE_DEF = "1"
SINE_KEYS = [FREQ_KEY, AMP_KEY, DUR_KEY, BURST_SINE_KEY]

# PULSE SPECIFICATIONS
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

def main():
    print("main")

    # Setup Theme
    sg.theme('TealMono')

    # Setup Layout
    layout = [[sg.Text('Choose a Wave Type (Sine or Pulse):')],
              [sg.Radio(SINE, group_id=GROUP_ID, key=SINE, default=True),
               sg.Radio(PULSE, group_id=GROUP_ID, key=PULSE)],
              [sg.HorizontalSeparator()],
              [sg.Text("Sine Specifications:")],
              [sg.Push(), sg.Text("Frequency (10 to 200 Hz):"), sg.InputText(default_text=FREQ_DEFAULT, size=(4, 1), key=FREQ_KEY)],
              [sg.Push(), sg.Text("Amplitude (1 to 100):"), sg.InputText(default_text=AMP_DEFAULT, size=(4, 1), key=AMP_KEY)],
              [sg.Push(), sg.Text("Duration (seconds):"), sg.InputText(default_text=DUR_DEFAULT, size=(4, 1), key=DUR_KEY)],
              [sg.Push(), sg.Text("Burst Period (seconds):"), sg.InputText(default_text=BURST_SINE_DEF, size=(4, 1), key=BURST_SINE_KEY)],
              [sg.HorizontalSeparator()],
              [sg.Text("Pulse Specifications:")],
              [sg.Push(), sg.Text("Width (msec):"), sg.InputText(default_text=WIDTH_DEF, size=(4, 1), key=WIDTH_KEY)],
              [sg.Push(), sg.Text("Period (msec):"), sg.InputText(default_text=PERIOD_DEF, size=(4, 1), key=PERIOD_KEY)],
              [sg.Push(), sg.Text("Amplitude (1 to 100):"), sg.InputText(default_text=AMP_P_DEF, size=(4, 1), key=AMP_P_KEY)],
              [sg.Push(), sg.Text("Count (1 to 32,000):"), sg.InputText(default_text=COUNT_DEF, size=(4, 1), key=COUNT_KEY)],
              [sg.Push(), sg.Text("Burst Period (seconds):"), sg.InputText(default_text=BURST_P_DEF, size=(4, 1), key=BURST_P_KEY)],
              [sg.HorizontalSeparator()],
              [sg.Button('Generate Waveform')]
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
            print(SINE, values[SINE])
            print("Freq:", values[FREQ_KEY])
            print("Amp:", values[AMP_KEY])
            print("Duration:", values[DUR_KEY])
            print("Burst Period:", values[BURST_SINE_KEY])

            for key in PULSE_KEYS:
                print(key, ":", values[key])

    #  Get event and values
    #  Check for events.

    # Close Window after breaking out of loop
    window.close()


if __name__ == "__main__":
    main()
