"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

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

        self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=value)

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

    def drive_left(self, left_speed_entry, right_speed_entry):
        """Moves the robot left at the specified speed"""
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def drive_right(self, left_speed_entry, right_speed_entry):
        """Moves the robot right at the specified speed"""
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def stop_robot(self):
        """Stops the motors from running"""
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        self.arm_motor.stop(stop_action='brake')

    def seek_beacon(self):
        """Look for the IR beacon"""
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.drive_forward(turn_speed, -turn_speed)
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance == 0:
                        self.stop_robot()
                    else:
                        self.drive_forward(forward_speed, forward_speed)

                elif math.fabs(current_heading) < 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        self.drive_forward(-turn_speed, turn_speed)
                    else:
                        self.drive_forward(turn_speed, -turn_speed)
            time.sleep(0.2)

        print("Abandon ship!")
        self.stop_robot()
        return False
