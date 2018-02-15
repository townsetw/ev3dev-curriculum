"""Final Project: Maze Runner:

The Robot will drive in a straight line until hitting a black line on the
floor. The user will then be prompted to pick a direction to turn. The robot
will then turn either left right or backward based on user input,
and continue forward. Once the robot reaches the middle of the maze the user
can press a button to pick  up the "treasure" in the middle of the maze.
There will then be a return to beginning button which the user can press to
have the robot automatically return to the start, hence leaving the maze
with the treasure."""

import tkinter
from tkinter import ttk
import tkinter as tk
import mqtt_remote_method_calls as com

def main():
    mqtt_client = com.MqttClient
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Maze Runner Controller: Click the start button to begin, '
               'and when robot stops press button to turn it left right or '
               'backwards. When the Treasure is found, Press the Treasure '
               'found button.')

    mainframe = ttk.Frame(root, padding=30, relief='raised')
    mainframe.grid

    forward =