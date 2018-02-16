import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3

import robot_controller as robo
import time
sensor = ev3.InfraredSensor()
btn = ev3.Button()