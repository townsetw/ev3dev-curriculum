#!/usr/bin/env python3

"""Final Project: Maze Runner:

The Robot will drive in a straight line until hitting a black line on the
floor. The user will then be prompted to pick a direction to turn. The robot
will then turn either left right or backward based on user input,
and continue forward. Once the robot reaches the middle of the maze the user
can press a button to pick  up the "treasure" in the middle of the maze.
There will then be a return to beginning button which the user can press to
have the robot automatically return to the start, hence leaving the maze
with the treasure."""


import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyPcDelegate(object):
    """ This class will help receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, command):
        print("Received Command: " + command)
        message_to_display = "{} was initiated.".format(command)
        self.display_label.configure(text=message_to_display)


def main():
    print("--------------------------------------------")
    print(" Controlling the Maze Runner")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")

    root = tkinter.Tk()
    root.title("Maze Runner Controller")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

    speed_label = ttk.Label(main_frame, text="DRIVE SPEED")
    speed_label.grid(row=0, column=3)

    speed_entry = ttk.Entry(main_frame, text="Green", width=11)
    speed_entry.insert(0, "450")
    speed_entry.grid(row=1, column=3)

    start_button = ttk.Button(main_frame, text="Start")
    start_button.grid(row=4, column=3)
    start_button['command'] = lambda: drive_forward(mqtt_client, speed_entry)
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=5, column=3)
    stop_button['command'] = lambda: stop_robot(mqtt_client)
    root.bind('s', lambda event: stop_robot(mqtt_client))

    back_button = ttk.Button(main_frame, text="Turn Around")
    back_button.grid(row=6, column=3)
    back_button['command'] = lambda: turn_around(mqtt_client, speed_entry)
    root.bind('<Down>', lambda event: turn_around(mqtt_client, speed_entry))

    left_turning = ttk.Button(main_frame, text="Turn Left")
    left_turning.grid(row=5, column=0)
    left_turning['command'] = lambda: turn_left(mqtt_client, speed_entry)
    root.bind('<Left>', lambda event: turn_left(mqtt_client, speed_entry))

    right_turning = ttk.Button(main_frame, text="Turn Right")
    right_turning.grid(row=5, column=4)
    right_turning['command'] = lambda: turn_right(mqtt_client, speed_entry)
    root.bind('<Right>', lambda event: turn_right(mqtt_client, speed_entry))

    pick_up_treasure_button = ttk.Button(main_frame, text="Pick Up Treasure")
    pick_up_treasure_button.grid(row=9, column=0)
    pick_up_treasure_button['command'] = lambda: pick_up_treasure(mqtt_client)
    root.bind('z', lambda event: pick_up_treasure(mqtt_client))

    return_to_start_button = ttk.Button(main_frame, text="Return to Beginning")
    return_to_start_button.grid(row=10, column=0)
    return_to_start_button['command'] = lambda: return_to_start(mqtt_client, speed_entry)
    root.bind('x', lambda event: return_to_start(mqtt_client, speed_entry))

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=9, column=4)
    quit_button['command'] = (lambda: quit_program(mqtt_client))
    root.bind('q', lambda event: quit_program(mqtt_client))

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root.mainloop()


def drive_forward(mqtt_client, speed_entry):
    print('Driving Forward')
    mqtt_client.send_message("drive_forward", [int(speed_entry.get()),
                                               int(speed_entry.get())])


def stop_robot(mqtt_client):
    print('Stopping Robot')
    mqtt_client.send_message("stop_robot")


def turn_around(mqtt_client, speed_entry):
    print('Turning Around')
    mqtt_client.send_message("turn_around", [int(speed_entry.get()),
                                               int(speed_entry.get())])


def turn_left(mqtt_client, speed_entry):
    print('Turning Left')
    mqtt_client.send_message("turn_left", [int(speed_entry.get()),
                                               int(speed_entry.get())])


def turn_right(mqtt_client, speed_entry):
    print('Turning Right')
    mqtt_client.send_message("turn_right", [int(speed_entry.get()),
                                               int(speed_entry.get())])


def pick_up_treasure(mqtt_client):
    print('Found the Teasure!')
    mqtt_client.send_message("arm_up")


def return_to_start(mqtt_client, speed_entry):
    print('Returning to beginning')
    mqtt_client.send_message("return_to)start", [int(speed_entry.get()),
                                               int(speed_entry.get())])


def quit_program(mqtt_client):
    print("Shutting Down")
    mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
