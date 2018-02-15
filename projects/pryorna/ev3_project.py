"""Final Project Idea: Frogger 2.0

Having the robot follow a line (black/white) with obstacles slowly going
back and forth that may or may not get in the robots way. AUTONOMUS (MODE1):
If the IR sensor (analog sensor) senses the object a certain distance in front of
it, OR the user presses the touch sensor (digital input) the robot stops and
waits for human
interaction to start the TELEOP (MODE2) by using controls/button on the
computer (Tkinter/MQTT) to move the robot to the end of the level. Hitting the
backspace button on the mindstorm brain ends the game immediately."""

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3

import robot_controller as robo
import time
sensor = ev3.InfraredSensor()
btn = ev3.Button()


def main():
    """Speaks at the beginning and goes into the main_follow_the_line
    function."""
    print("Let the games begin!")
    ev3.Sound.speak("Starting Frogger 2.0 Game").wait()

    main_follow_the_line()


def main_follow_the_line():
    """Waits for the user to press either the 's' or 'q' keys, and goes to
    the follow_the_line function if 's' is pressed."""

    black_level = 3
    robot = robo.Snatch3r()

    while True:
        command_to_run = input(
            "Enter 's' to start the game or 'q' to quit: ")
        if command_to_run == 's':
            print("Lets begin! Good luck!")
            follow_the_line(robot, black_level)
        elif command_to_run == 'q':
            break
        else:
            print(command_to_run, "--Please enter either 's' or 'q'--")

    print("Game over!")


def follow_the_line(robot, black_level):
        """
        Follows the black line until either an object gets a certain
        distance in front of it or the touch sensor is pressed or the
        backspace button on the lego mindstorm brain is pressed.
        """
        x = 2
        while x == 2:
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            if robot.color_sensor.reflected_light_intensity > black_level + 20:
                robot.turn_degrees(10, 900)
            else:
                robot.drive_forward(900, 900)
            if sensor.proximity <= 15:
                robot.stop_robot()
                break
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

        #if sensor.proximity <= 5:
        #    robot.stop_robot()
        #    ev3.Sound.speak("Game over.")

        #robot.loop_forever()
        #ev3.Sound.speak("Game over")


main()
