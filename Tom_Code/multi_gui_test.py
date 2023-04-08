"""
Solution based on:
https://stackoverflow.com/a/61178541

"""

import PySimpleGUI as sg
from time import sleep
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Process



def work(a):

    for i in range(10):
        print("Hello", i)
        sleep(1)


def main():

    sg.theme('DarkGrey')

    layout = [[sg.Button("Start"), sg.Button("Stop")]]

    window = sg.Window("Multi Test", layout)

    # test_input = 123
    # p = Process(target=work, args=(test_input,))


    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == "Start":
            print("You pressed:", event)

            # Non-Process
            # work()
            temp = {"window": window}

            #Process
            test_input = 123
            p = Process(target=work, args=(test_input,))
            p.start()
        elif event == "Stop":
            print("You pressed:", event)
            p.terminate()

    window.close()

    pass


if __name__ == "__main__":
    main()
