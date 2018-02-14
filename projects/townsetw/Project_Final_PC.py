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
    print(" Controlling the Player")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")


    #my_delegate = MyDelegate()
    #mqtt_client = com.MqttClient(my_delegate)
    #mqtt_client.connect_to_pc()



    root = tkinter.Tk()
    root.title("Controlling the player")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    lights_button_label = ttk.Label(main_frame, text="Lights")
    lights_button_label.grid(row=0, column=0)
    lights_button = ttk.Checkbutton(main_frame)
    lights_button.grid(row=1, column=0)

    speed_label = ttk.Label(main_frame, text="DRIVE SPEED")
    speed_label.grid(row=0, column=3)

    speed_entry = ttk.Entry(main_frame, text="Green", width=11)
    speed_entry.insert(0,0)
    speed_entry.grid(row=1, column=3)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=4, column=3)

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




    root.mainloop()


main()