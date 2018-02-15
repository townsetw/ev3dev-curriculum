#!/usr/bin/env python3
""""THIS is the pc portion of the project - Tyler Townsend"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate(object):
    """ This class will help receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, button_name):
        print("Received: " + button_name)
        message_to_display = "{} was pressed.".format(button_name)
        self.display_label.configure(text=message_to_display)


def main():
    print("--------------------------------------------")
    print(" Controlling the Recycle Bot")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Recycle Bot Control")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

    lights_button_label = ttk.Label(main_frame, text="Lights")
    lights_button_label.grid(row=0, column=0)
    lights_button = ttk.Checkbutton(main_frame, onvalue=turn_on_lights(
        mqtt_client), offvalue=turn_off_lights(mqtt_client))
    lights_button.grid(row=1, column=0)
    root.bind('l', lambda event: turn_on_lights)
    root.bind('o', lambda event: turn_off_lights)

    speed_label = ttk.Label(main_frame, text="DRIVE SPEED")
    speed_label.grid(row=0, column=3)

    speed_entry = ttk.Entry(main_frame, text="Green", width=11)
    speed_entry.insert(0, 0)
    speed_entry.grid(row=1, column=3)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=4, column=3)
    forward_button['command'] = lambda: drive_forward(mqtt_client, speed_entry)
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=5, column=3)

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=6, column=3)

    left_turning = ttk.Button(main_frame, text="Turn Left")
    left_turning.grid(row=5, column=0)

    right_turning = ttk.Button(main_frame, text="Turn Right")
    right_turning.grid(row=5, column=4)

    pick_up_trash_button = ttk.Button(main_frame, text="Pick Up Trash")
    pick_up_trash_button.grid(row=9, column=0)

    deposit_trash_button = ttk.Button(main_frame, text="Deposit Trash")
    deposit_trash_button.grid(row=10, column=0)

    button_label = ttk.Label(main_frame, text="  Button messages from EV3  ")
    button_label.grid(row=13, column=3)

    button_message = ttk.Label(main_frame, text="--")
    button_message.grid(row=14, column=3)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=9, column=4)
    quit_button['command'] = (lambda: quit_program(mqtt_client, False))
    root.bind('q', lambda event: quit_program(mqtt_client, False))

    exit_button = ttk.Button(main_frame, text="Exit")
    exit_button.grid(row=10, column=4)
    exit_button['command'] = (lambda: quit_program(mqtt_client, True))
    root.bind('e', lambda event: quit_program(mqtt_client, True))

    root.mainloop()


def drive_forward(mqtt_client, speed_entry):
    print('send_forward')
    mqtt_client.send_message("drive_forward", [int(speed_entry.get()),
                                               int(speed_entry.get())])


def turn_on_lights(mqtt_client):
    print('Turning On Lights')
    mqtt_client.send_message("turn_on_lights")


def turn_off_lights(mqtt_client):
    print('Turn Off Lights')
    mqtt_client.send_message("turn_off_lights")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()