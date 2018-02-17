
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3


class MyDelegate(object):

    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print(" Recycle Robot Ready")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("Recycle Bot Ready").wait()

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()

    btn = ev3.Button()
    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "Up")
    btn.on_down = lambda state: handle_button_press(state, mqtt_client, "Down")


def handle_button_press(button_state, mqtt_client, button_name):
    """Handle IR / button event."""
    if button_state:
        print("{} button was pressed".format(button_name))

        mqtt_client.send_message("button_pressed", [button_name])



main()
