import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

""""This is the Ev3 portion of the final project"""
""""These are the list of imports that allow mqtt communication, 
robot control, ev3 access, and time."""


class MyDelegate(object):
    """"The MyDelegate class helps to communicate information and methods
    back to the Tkinter gui and pc portion"""
    def __init__(self):
        """"The constructor function that stores the components of the robot as
        well as asserts them to make sure that they are connected"""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.w = 1

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.color_sensor.connected
        assert self.ir_sensor.connected
        assert self.pixy.connected

        self.MAX_SPEED = 900
        self.running = True

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Moves the robot a given amount of inches at a given speed"""
        self.left_motor.run_to_rel_pos(position_sp=inches_target * 90,
                                       speed_sp=speed_deg_per_second,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.run_to_rel_pos(position_sp=inches_target * 90,
                                        speed_sp=speed_deg_per_second,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Turns the robot a given number of degrees at a given speed"""

        value = degrees_to_turn * 4.5

        self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp,
                                       position_sp=-value)

        self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp,
                                        position_sp=value)

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep().wait()

    def arm_calibration(self):
        """Calibrates the robot arm by having it move up to the top position
        and beeps, then moves the arm down to the bottom position and beeps"""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(
            position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0

    def arm_up(self):
        """Moves the arm up to the top position and beeps."""

        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):
        """Moves the arm down to the bottom position and beeps."""

        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(
            ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def shutdown(self):
        """Stops both motors and sets the left and Right LEDS to the
        green color"""
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        self.running = False

        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

        print('Goodbye')
        ev3.Sound.speak("Goodbye").wait()

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(
                0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def drive_forward(self, left_speed_entry, right_speed_entry):
        """Moves the robot forward at the specified speed"""
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def drive_backward(self, left_speed_entry, right_speed_entry):
        """Moves the robot backward at the specified speed"""
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def drive_right(self, left_speed_entry, right_speed_entry):
        """Moves the robot left at the specified speed"""
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def drive_left(self, left_speed_entry, right_speed_entry):
        """Moves the robot right at the specified speed"""
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def stop_robot(self):
        """Stops the motors from running"""
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        self.arm_motor.stop(stop_action='brake')

    def turn_on_lights(self):
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Sound.speak("Lights On").wait()
        self.w = 2

    def turn_off_lights(self):
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        ev3.Sound.speak("Lights Off").wait()
        self.w = 2


def main():
    """"Initializes the waste bot and creates communication link to the pc
    using the mqtt_client and delegate to have the tkinter gui receive
    messages. Adds button callback functions so that when a digital input on the
    brickman is selected, the robot will carry out that specific task. """
    print("--------------------------------------------")
    print(" Waste Bot Ready")
    print("--------------------------------------------")
    ev3.Sound.speak("Waste Bot Ready").wait()

    robot = robo.Snatch3r()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    robot_mqtt = com.MqttClient(robot)
    robot_mqtt.connect_to_pc()

    btn = ev3.Button()
    btn.on_up = lambda state: searching_for_radioactive_waste(state,
                                                              robot_mqtt,
                                                              robot,
                                                              "Up")
    btn.on_down = lambda state: depositing_trash(state, robot_mqtt,
                                                 robot, "Down")
    btn.on_left = lambda state: recycling(state, robot_mqtt, robot,
                                          "Left")
    btn.on_right = lambda state: depositing_radioactive_waste(state,
                                                              robot_mqtt,
                                                              robot, "Right")

    while my_delegate.running:
        btn.process()
        time.sleep(0.01)


def depositing_radioactive_waste(button_state, mqtt_client, robot, button_name):
    """Deposits the radioactive waste in the respective storage bin"""
    if button_state:
        print("{} button was pressed".format(button_name))
        mqtt_client.send_message("button_pressed", ["Depositing "
                                                    "Radioactive "
                                                    "Material"])
        ev3.Sound.speak("Depositing Radioactive Material").wait()
        robot.drive_forward(100, 100)
        x = 1
        while x == 1:
            if robot.color_sensor.color == 3:
                robot.drive_forward(200, 200)
                time.sleep(4)
                robot.stop_robot()
                robot.turn_degrees(-90, 200)
                robot.arm_down()
                robot.drive_inches(-24, 300)
                robot.turn_degrees(90, 200)
                break


def searching_for_radioactive_waste(button_state, mqtt_client, robot, button_name):
    """searches for the radioactive waste in the vicinity by constantly
    turning scanning the area for the color green that was learned by the
    pixy camera. The Robot automatically adjusts based on x-coordinates of
    the picture in the camera. Once found, the IR sensor will tell when the
    radioactive material has been located."""
    if button_state:
        print("{} button was pressed".format(button_name))
        mqtt_client.send_message("button_pressed", ["Searching for "
                                                    "Radioactive "
                                                    "Material"])
        ev3.Sound.speak("Scanning").wait()

        robot.pixy.mode = "SIG1"
        turn_speed = 100
        sensor = ev3.InfraredSensor()

        x = robot.pixy.value(1)
        y = robot.pixy.value(2)

        robot.turn_degrees(20, 200)
        if x <= 150:

            while not robot.touch_sensor.is_pressed:

                print('x = ', x)
                print('y = ', y)
                print(robot.ir_sensor.proximity)
                x = robot.pixy.value(1)
                y = robot.pixy.value(2)

                if x <= 150:
                    robot.drive_forward(-turn_speed, turn_speed)
                elif x >= 170:
                    robot.drive_forward(turn_speed, -turn_speed)
                elif 150 < x < 170:
                    robot.drive_inches(3, 200)
                    robot.stop_robot()
                    if sensor.proximity <= 15:
                        ev3.Sound.beep()
                        ev3.Sound.speak("Found Radioactive Material").wait()
                        break
                time.sleep(0.25)


def depositing_trash(button_state, mqtt_client, robot, button_name):
    """Deposits the trash into the respective storage bin"""
    if button_state:
        print("{} button was pressed".format(button_name))
        mqtt_client.send_message("button_pressed", ["Trashing"])
        ev3.Sound.speak("Trashing").wait()
        robot.drive_forward(100, 100)
        x = 1
        while x == 1:
            if robot.color_sensor.color == 1:
                robot.drive_forward(200, 200)
                time.sleep(4)
                robot.stop_robot()
                robot.turn_degrees(-90, 200)
                robot.arm_down()
                robot.drive_inches(-24, 300)
                robot.turn_degrees(90, 200)
                break


def recycling(button_state, mqtt_client, robot, button_name):
    """"recycles waste into respective storage bin"""
    if button_state:
        print("{} button was pressed".format(button_name))
        mqtt_client.send_message("button_pressed", ["Recycling"])
        ev3.Sound.speak("Recycling").wait()
        robot.drive_forward(100, 100)
        x = 1
        while x == 1:
            if robot.color_sensor.color == 5:
                robot.drive_forward(200, 200)
                time.sleep(4)
                robot.stop_robot()
                robot.turn_degrees(-90, 200)
                robot.arm_down()
                robot.drive_inches(-24, 300)
                robot.turn_degrees(90, 200)
                break
        mqtt_client.send_message("button_pressed", ["Recycling Complete"])


main()
