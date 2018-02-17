import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
robot = robo.Snatch3r()
mqtt_client = com.MqttClient(robot)
mqtt_client.connect_to_pc()


returnlist = []


def drive_forward(speed_entry):
    while robot.color_sensor.color != ev3.ColorSensor.COLOR_BLACK:
        robot.drive_forward(speed_entry, speed_entry)
    returnlist.append('forward')


def stop_robot():
    robot.stop_robot()


def turn_around(speed_entry):
    robot.turn_degrees(180, speed_entry)


def turn_left(speed_entry):
    robot.turn_degrees(90, speed_entry)
    returnlist.append('right')


def turn_right(speed_entry):
    robot.turn_degrees(-90, speed_entry)
    returnlist.append('left')


def arm_up():
    robot.arm_up()
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.AMBER)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.AMBER)


def return_to_start(speed_entry):
    for k in range(len(returnlist), -1):
        if returnlist[k] == 'forward':
            drive_forward(speed_entry)
        if returnlist[k] == 'left':
            turn_left(speed_entry)
        if returnlist[k] == 'right':
            turn_right(speed_entry)


def quit_program():
    robot.shutdown()
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
