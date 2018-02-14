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

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()


main()