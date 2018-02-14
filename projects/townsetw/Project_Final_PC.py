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

    center_button_label = ttk.Label(main_frame, text="DRIVE SPEED")
    center_button_label.grid(row=0, column=3)

    center_button = ttk.Entry(main_frame, text="Green", width=10)
    center_button.grid(row=1, column=3)




    root.mainloop()


main()