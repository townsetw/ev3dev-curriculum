import tkinter
from tkinter import ttk
import tkinter as tk
import mqtt_remote_method_calls as com

def main():
    """Creates the commands for the gamepad, as well as the locations of
    those commands either on the keyboard or in the Tkinter window."""
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Frogger 2.0 Gamepad: Click the buttons OR Use the arrow keys on the computer"
               "to move around and press 'e' to stop moving")
    count_down = Tkintercount(mqtt_client)
    count_down.title("Frogger 2.0 COUNTDOWN")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")

    right_speed_label = ttk.Label(main_frame, text="")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")

    right_button = ttk.Button(main_frame, text="Turn Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_right(mqtt_client,
                                                 left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: send_right(mqtt_client,
                                                  left_speed_entry,
                                                  right_speed_entry))

    left_button = ttk.Button(main_frame, text="Turn Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_left(mqtt_client,
                                               left_speed_entry,
                                               right_speed_entry)
    root.bind('<Left>', lambda event: send_left(mqtt_client,
                                                left_speed_entry,
                                                right_speed_entry))

    back_button = ttk.Button(main_frame, text="Go Backwards")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: send_backward(mqtt_client,
                                                   left_speed_entry,
                                                   right_speed_entry)
    root.bind('<Down>', lambda event: send_backward(mqtt_client,
                                                    left_speed_entry,
                                                    right_speed_entry))

    exit_button = ttk.Button(main_frame, text="Exit Game")
    exit_button.grid(row=6, column=2)
    exit_button['command'] = (lambda: quit_program(mqtt_client, True))

    stop_button = ttk.Button(main_frame, text="Stop Movement")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_stop_robot(mqtt_client)
    root.bind('<e>', lambda event: send_stop_robot(mqtt_client))

    forward_button = ttk.Button(main_frame, text="Go Forwards")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_forward(mqtt_client,
                                                     left_speed_entry,
                                                     right_speed_entry)
    root.bind('<Up>', lambda event: send_forward(mqtt_client, left_speed_entry,
                                                 right_speed_entry))

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------

def send_stop_robot(mqtt_client):
    """Callbacks the stop button on the computer gamepad. The mqtt_client
    argument connects the computer to the robot."""
    print("send_stop_robot")
    mqtt_client.send_message("stop_robot")

def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    """Callbacks the forward button on the computer gamepad with given
    left and right speeds. The mqtt_client
    argument connects the computer to the robot."""
    print('send_forward')
    mqtt_client.send_message("drive_forward", [int(left_speed_entry.get()),
                                               int(right_speed_entry.get())])

def send_backward(mqtt_client, left_speed_entry, right_speed_entry):
    """Callbacks the backward button on the computer gamepad with given
    left and right speeds. The mqtt_client
    argument connects the computer to the robot."""
    print("send_backward")
    mqtt_client.send_message("drive_backward", [int(left_speed_entry.get()),
                                                int(right_speed_entry.get())])

def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    """Callbacks the left button on the computer gamepad with given left
    and right speeds. The mqtt_client
    argument connects the computer to the robot."""
    print("send_left")
    mqtt_client.send_message("drive_left", [int(left_speed_entry.get()),
                                            int(right_speed_entry.get())])

def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    """Callbacks the right button on the computer gamepad with given left
    and right speeds. The mqtt_client
    argument connects the computer to the robot."""
    print("send_right")
    mqtt_client.send_message("drive_right", [int(left_speed_entry.get()),
                                             int(right_speed_entry.get())])

def quit_program(mqtt_client, shutdown_ev3):
    """Callbacks the quit button on the computer gamepad. The mqtt_client
    argument connects the computer to the robot. The shutdown_ev3 argument
    is a boolean that when True the robot 'shuts down'."""
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


class Tkintercount(tkinter.Tk):
    """Makes a class called 'Tkintercount' that makes a countdown tkinter
    window."""
    def __init__(self, mqtt_client):
        """Assigning initial variables under the 'Tkintercount' class, and
        using the mqtt_client so the countdown window works with stopping
        the robot when it hits zero."""
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)
        self.label.pack()
        self.remains = 0
        self.countdown(60)
        self.mqtt_client = mqtt_client

    def countdown(self, remains=None):
        """Uses an argument when whatever number you put into the
        'countdown' function, the Tkinter window that is created will count
        down from that starting number. Once the timer reaches 0,
        the motors stops and the game ends."""
        if remains is not None:
            self.remains = remains

        if self.remains <= 0:
            self.label.configure(text="Your time is up!")
            send_stop_robot(self.mqtt_client)
            print("Congratulations. You Win!")

        else:
            self.label.configure(text="%d" % self.remains)
            self.remains = self.remains - 1
            self.after(1000, self.countdown)


main()
