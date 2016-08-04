#!/usr/bin/env python3
"""Controller"""

import evdev

__author__ = 'Anurag Choudhury'

class Controller(object):
    """Takes controller events and sets setpoints"""
    ## Some helpers ##
    @classmethod
    def scale(cls, val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.

        val: float or int
        src: tuple
        dst: tuple

        example: print scale(64, (0.0, 64.0), (-1.0, +1.0))
        """
        return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

    @classmethod
    def scale_stick(cls, value):
        return cls.scale(value, (0, 255), (-100, 100))

    def __init__(self, robot):
        self.robot = robot
        ## Initializing ##
        print("Finding ps3 controller...")
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            if device.name == 'PLAYSTATION(R)3 Controller':
                ps3dev = device.fn
        try:
            self.gamepad = evdev.InputDevice(ps3dev)
        except NameError:
            raise Exception("No Playstation Controller!")

    def map_input(self):
        """maps the input to subsystems"""
        for event in self.gamepad.read_loop():   #this loops infinitely
            #Analog Inputs
            if event.type == 3:             #A stick is moved
                if event.code == 5:         #Y axis on right stick
                    speed = self.scale_stick(event.value) #TODO: Get rid of this

            #Digital Inputs
            if event.type == 1 and event.code == 302:
                if event.value == 1:
                    self.robot.subsystems[0].setpoint = 100
                elif event.value == 0:
                    self.robot.subsystems[0].setpoint = 0
            if event.type == 1 and event.code == 291 and event.value == 1:
                self.robot.enable(not self.robot.enabled)
            if event.type == 1 and event.code == 288 and event.value == 1:
                break #shuts off program
