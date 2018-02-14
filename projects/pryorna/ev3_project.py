"""Final Project Idea: Frogger    WHY IS THIS THE THEME?? Because it was a
fun game that I played as a kid on my playstation.

Having the robot follow a line (black/white) with obstacles slowly going
back and forth that may or may not get in the robots way. AUTONOMUS (MODE1):
If the IR sensor (analog sensor) senses the object a certain distance in front of
it, OR the user presses the touch sensor (digital input) the robot stops and
waits for human
interaction to start the TELEOP (MODE2) by using controls/button on the
computer (Tkinter/MQTT) to move the robot to the end of the level. Hitting the
backspace button on the mindstorm brain ends the game immediately
(during AUTONOMUS)."""

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3

import robot_controller as robo
import time
sensor = ev3.InfraredSensor()
btn = ev3.Button()
tkfont = "bold"

def main():
    print("Let the games begin!")
    #ev3.Sound.speak("Starting Frogger Game").wait()

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
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
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
            if btn.backspace:
                robot.stop_robot()
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
                ev3.Sound.speak("Game Over").wait()
                break
            time.sleep(0.01)

        robot.stop_robot()
        robot = robo.Snatch3r()
        mqtt_client = com.MqttClient(robot)
        mqtt_client.connect_to_pc()
        if sensor.proximity <= 5:
            robot.stop_robot()
            ev3.Sound.speak("Game over.")

        robot.loop_forever()
        ev3.Sound.speak("You win!")

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()