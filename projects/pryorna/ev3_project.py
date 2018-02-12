"""Final Project Idea: Frogger    WHY IS THIS THE THEME?? Because it was a
fun game that I played as a kid on my playstation.
Having the robot follow a line (black/white) with obstacles slowly going
back and forth that may or may not get in the robots way.
If the IR sensor (analog) senses the object a certain distance in front of
it, the robot stops and waits for human interaction to 'continue?' and the user either
clicks the 'okay' button on python (Tkinter) OR the 'up' button on the
mindstorm brain attached to the robot (MQTT) OR by pressing the touch sensor on the
robot (digital input). Hitting the backspace button on the mindstorm brain
ends the game immediately."""
import ev3dev.ev3 as ev3
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    print("Let the games begin!")
    ev3.Sound.speak("Starting Frogger Game").wait()

    arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    assert arm_motor.connected
    assert left_motor.connected
    assert right_motor.connected
    assert touch_sensor

    #MOTORS
    left_motor.run_forever(speed_sp = 600)
    right_motor.run_forever(speed_sp= 600)

    left_motor.stop(stop_action ="brake") #Read comment on line 30
    right_motor.stop(stop_action="brake") #OR use robot.stop_robot()

    arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running

    #CHANGE UP BELOW FOR TURNING OFF PROGRAM WITH BACKSPACE
    btn = ev3.Button() #button on the mindstorm brain
    if btn.up:
        print("up")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)

    #DIGITAL INPUTS
    touch_sensor = ev3.TouchSensor()
    if touch_sensor.is_pressed:
        print("stuff") #CHANGE THIS LATER

    #MQTT (Make sure to create a separate program for EV3)
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    continue_button = ttk.Button(main_frame, text="Click to Continue OR "
                                                  "press the ENTER key on "
                                                  "your keyboard")
    continue_button.grid(row=3, column=1)
    continue_button['command'] = lambda: continue_robot(mqtt_client)
    root.bind('<enter>', lambda event: continue_robot(mqtt_client))

def continue_robot(mqtt_client):
    print("continue_robot")
    mqtt_client.send_message("send_continue_robot") #make
    # send_continue_robot on robot_controller!!
