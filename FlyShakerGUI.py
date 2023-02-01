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


def main():
    print("main")

    # Setup Theme
    sg.theme('TealMono')

    # Setup Layout
    layout = [[sg.Text('Choose a Wave Type (Sine or Pulse):')],
              [sg.Radio("Sine", "RADIO1", default=True), sg.Radio('Pulse', "RADIO1")],
              [sg.Button('Cancel')]
              ]

    # Create Window
    window = sg.Window('FlyShaker GUI', layout)

    # Event Loop to process "events" and get the "values" of the inputs

    # While Loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        print('You entered', values[0])
    #  Get event and values
    #  Check for events.

    # Close Window after breaking out of loop
    window.close()


if __name__ == "__main__":
    main()
