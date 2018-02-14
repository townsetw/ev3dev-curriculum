import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    continue_button = ttk.Button(main_frame, text="Click to Continue OR "
                                                  "press the SPACE key on "
                                                  "your keyboard")
    continue_button.grid(row=3, column=1)
    continue_button['command'] = lambda: send_continue_robot(mqtt_client)
    root.bind('<space>', lambda event: send_continue_robot(mqtt_client))

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=2)
    stop_button['command'] = lambda: send_stop_robot(mqtt_client)
    root.bind('<e>', lambda event: send_stop_robot(mqtt_client))

    '''TEST BELOW'''

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: send_forward(mqtt_client,
                                                     left_speed_entry,
                                                     right_speed_entry)
    root.bind('<Up>', lambda event: send_forward(mqtt_client, left_speed_entry,
                                                 right_speed_entry))

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------

def send_continue_robot(mqtt_client):
    print("send_continue_robot")
    mqtt_client.send_message("do_continue_robot")


def send_stop_robot(mqtt_client):
    print("send_stop_robot")
    mqtt_client.send_message("stop_robot")

def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print('send_forward')
    mqtt_client.send_message("drive_forward", [int(left_speed_entry.get()),
                                               int(right_speed_entry.get())])

def send_backward(mqtt_client, left_speed_entry, right_speed_entry):
    print("send_backward")
    mqtt_client.send_message("drive_backward", [int(left_speed_entry.get()),
                                               int(right_speed_entry.get())])

def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("send_left")
    mqtt_client.send_message("drive_left", [int(left_speed_entry.get()),
                                               int(right_speed_entry.get())])


def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("send_right")
    mqtt_client.send_message("drive_right", [int(left_speed_entry.get()),
                                               int(right_speed_entry.get())])

# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
