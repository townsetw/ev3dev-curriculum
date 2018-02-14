"""Final Project Idea: Frogger    WHY IS THIS THE THEME?? Because it was a
fun game that I played as a kid on my playstation.
Having the robot follow a line (black/white) with obstacles slowly going
back and forth that may or may not get in the robots way.
If the IR sensor (analog sensor) senses the object a certain distance in front of
it, the robot stops and waits for human interaction to 'continue?' and the user either
clicks the 'continue?' button on python (Tkinter/MQTT) OR the 'enter' button
on the computer keyboard (MQTT) OR by pressing the touch sensor on the
robot (digital input). Hitting the backspace button on the mindstorm brainends the game immediately."""

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import robot_controller as robo
import time
sensor = ev3.InfraredSensor()

def main():
    #robot = robo.Snatch3r
    print("Let the games begin!")
    ev3.Sound.speak("Starting Frogger Game").wait()

    main_follow_the_line()

def main_follow_the_line():

    white_level = 98
    black_level = 3
    robot = robo.Snatch3r()

    while True:
        command_to_run = input(
            "Enter 's' to start the game or 'q' to quit: ")
        if command_to_run == 's':
            print("Follow the line.")
            follow_the_line(robot, black_level)
        elif command_to_run == 'q':
            break
        else:
            print(command_to_run,
            "is not a known command. Please enter a valid choice.")

    print("Goodbye!")

def follow_the_line(robot, black_level):
        """
        The robot follows the black line until the touch sensor is pressed.
        You will need a black line track to test your code
        When the touch sensor is pressed, line following ends, the robot stops, and control is returned to main.

        Type hints:
          :type robot: robo.Snatch3r
          :type black_level: int
        """
        x = 2
        # DONE: 5. Use the calibrated values for white and black to calculate a
        # light threshold to determine if your robot
        # should drive straight or turn to the right.  You will need to test and refine your code until it works well.
        # Optional extra - For a harder challenge could you drive on the black line and handle left or right turns?

        while x == 2:
            if robot.color_sensor.reflected_light_intensity > black_level + 20:
                robot.turn_degrees(10, 900)
            else:
                robot.drive_forward(900, 900)
            if sensor.proximity <= 10:
                robot.stop_robot()
                break
                # Get continue_button to pop up here using function
            if robot.touch_sensor.is_pressed:
                break

        robot.stop_robot()
        ev3.Sound.speak("You win!")

    #MOTORS

    #left_motor.stop(stop_action ="brake") #Read comment on line 30
    #right_motor.stop(stop_action="brake") #OR use robot.stop_robot()

    #arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor
    #  finishes running

    #CHANGE UP BELOW FOR TURNING OFF PROGRAM WITH BACKSPACE

btn = ev3.Button() #button on the mindstorm brain
if btn.backspace:
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
    ev3.Sound.speak("Game Over").wait()
time.sleep(0.01)

#DIGITAL INPUTS
touch_sensor = ev3.TouchSensor()
if touch_sensor.is_pressed:
    print("stuff") #CHANGE THIS LATER


def mqtt_ev3_main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    #robot.loop_forever()

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()