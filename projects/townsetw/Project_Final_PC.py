#!/usr/bin/env python3
""""THIS is the pc portion of the project - Tyler Townsend"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):
    """ This class will help receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, command):
        print(command)
        message_to_display = "{}".format(command)
        self.display_label.configure(text=message_to_display)


def main():
    """Creates Tkinter GUI with drive speed entry, forward button,
    stop button, back button, turn right button, turn left button, pick up
    trash button, deposit trash button, quit out of the GUI and exit out of
    the program buttons, as well as lights buttons to turn the lights on and
    off on the robot depending on the time of day that the robot may be working in."""

    print("--------------------------------------------")
    print(" Controlling the Waste Bot")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    print("Down = Deposits Trash")
    print("Up = Searches for Radioactive Material")
    print("Left = Recycles")
    print("Right = Deposits Radioactive Material")

    root = tkinter.Tk()
    root.title("Recycle Bot Control")

    main_frame = ttk.Frame(root, padding=40, relief='raised')
    main_frame.grid()

    lights_button_label = ttk.Label(main_frame, text="Lights")
    lights_button_label.grid(row=0, column=0)
    lights_button = ttk.Checkbutton(main_frame, onvalue=1,
                                    offvalue=0)
    lights_button.grid(row=1, column=0)
    light_button_observer = tkinter.StringVar()
    lights_button['variable'] = light_button_observer
    lights_button['command'] = lambda: turn_on_off_lights(mqtt_client,
                                                          light_button_observer.get())

    speed_label = ttk.Label(main_frame, text="DRIVE SPEED")
    speed_label.grid(row=0, column=3)

    speed_entry = ttk.Entry(main_frame, text="Green", width=11)
    speed_entry.insert(0, "450")
    speed_entry.grid(row=1, column=3)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=4, column=3)
    forward_button['command'] = lambda: drive_forward(mqtt_client, speed_entry)
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=5, column=3)
    stop_button['command'] = lambda: stop_robot(mqtt_client)
    root.bind('s', lambda event: stop_robot(mqtt_client))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=6, column=3)
    back_button['command'] = lambda: drive_backwards(mqtt_client, speed_entry)
    root.bind('<Down>', lambda event: drive_backwards(mqtt_client,
                                                      speed_entry))

    left_turning = ttk.Button(main_frame, text="Turn Left")
    left_turning.grid(row=5, column=0)
    left_turning['command'] = lambda: turn_left(mqtt_client, speed_entry)
    root.bind('<Left>', lambda event: turn_left(mqtt_client,
                                                speed_entry))

    right_turning = ttk.Button(main_frame, text="Turn Right")
    right_turning.grid(row=5, column=4)
    right_turning['command'] = lambda: turn_right(mqtt_client, speed_entry)
    root.bind('<Right>', lambda event: turn_right(mqtt_client,
                                                  speed_entry))

    pick_up_trash_button = ttk.Button(main_frame, text="Pick Up Trash")
    pick_up_trash_button.grid(row=9, column=0)
    pick_up_trash_button['command'] = lambda: pick_up_trash(mqtt_client)
    root.bind('z', lambda event: pick_up_trash(mqtt_client))

    deposit_trash_button = ttk.Button(main_frame, text="Deposit Trash")
    deposit_trash_button.grid(row=10, column=0)
    deposit_trash_button['command'] = lambda: deposit_trash(mqtt_client)
    root.bind('x', lambda event: deposit_trash(mqtt_client))

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

    pc_delegate = MyDelegateOnThePc(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()


def drive_forward(mqtt_client, speed_entry):
    """Utilizes Mqtt clients to communicate with the robot to drive forward"""
    print('Driving Forwards')
    mqtt_client.send_message("drive_forward", [int(speed_entry.get()),
                                               int(speed_entry.get())])


def turn_on_off_lights(mqtt_client, value):
    """Utilizes Mqtt clients to communicate with the robot to turn on and
    off the lights on the Brickman"""
    x = int(value)
    if x == 1:
        print('Lights Are On')
        mqtt_client.send_message("turn_on_lights")
    if x == 0:
        print('Lights Are Off')
        mqtt_client.send_message("turn_off_lights")


def stop_robot(mqtt_client):
    """Utilizes Mqtt clients to communicate with the robot to stop the robot"""
    print("Stopping Robot")
    mqtt_client.send_message("stop_robot")


def drive_backwards(mqtt_client, speed_entry):
    """Utilizes Mqtt clients to communicate with the robot to drive
    backwards"""
    print("Driving Backwards")
    mqtt_client.send_message("drive_backward", [int(speed_entry.get()),
                                                int(speed_entry.get())])


def turn_left(mqtt_client, speed_entry):
    """Utilizes Mqtt clients to communicate with the robot to turn left"""
    print("Turning Left")
    mqtt_client.send_message("drive_left", [int(speed_entry.get()),
                                            int(speed_entry.get())])


def turn_right(mqtt_client, speed_entry):
    """Utilizes Mqtt clients to communicate with the robot to turn right"""
    print("Turning Right")
    mqtt_client.send_message("drive_right", [int(speed_entry.get()),
                                             int(speed_entry.get())])


def pick_up_trash(mqtt_client):
    """Utilizes Mqtt clients to communicate with the robot to move arm up"""
    print('Picking Up Trash')
    mqtt_client.send_message("arm_up")


def deposit_trash(mqtt_client):
    """Utilizes Mqtt clients to communicate with the robot to move arm down"""
    print('Depositing Trash')
    mqtt_client.send_message("arm_down")


def quit_program(mqtt_client, shutdown_ev3):
    """Utilizes Mqtt clients to communicate with the robot to either exit
    the tkinter gui or exit the entire program"""
    if shutdown_ev3:
        print("Shutting Down")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
