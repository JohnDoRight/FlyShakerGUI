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

    #  Get event and values
    #  Check for events.

    # Close Window after breaking out of loop
    window.close()


if __name__ == "__main__":
    main()
