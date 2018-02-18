

import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    ev3.Sound.speak("Maze Runner 2.0 ").wait()
    robot.arm_calibration()
    robot.loop_forever()


main()
