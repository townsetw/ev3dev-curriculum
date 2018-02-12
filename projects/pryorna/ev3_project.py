"""Final Project Idea: Frogger
Having the robot follow a line (black/white) with obstacles slowly going
back and forth that may or may not get in the robots way.
If the IR sensor (analog) senses the object a certain distance in front of
it, the robot stops and waits for human interaction to 'continue?' and the user either
clicks the 'okay' button on python (Tkinter) OR the 'up' button on the
mindstorm brain attached to the robot (MQTT) OR by pressing the touch sensor on the
robot (digital input).Hitting the backspace button on the mindstorm brain ends the game
immediately."""
import ev3dev.ev3 as ev3

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

    left_motor.run_forever(speed_sp = 600)
    right_motor.run_forever(speed_sp= 600)

    left_motor.stop()
    right_motor.stop(stop_action="brake")

    arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running

    btn = ev3.Button()
    if btn.up:
        print("up")
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)

    touch_sensor = ev3.TouchSensor()
    if touch_sensor.is_pressed:
