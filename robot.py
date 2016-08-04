"""This module is the top-level robot."""

import threading
from controller import Controller

from subsystems.shooter import Shooter

class FeedbackThread(threading.Thread):
    """Updates sensor and motor values in a separate thread"""
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot #pass by reference, not compute intensive

    def run(self):
        while True:
            if self.robot.enabled:
                for system in self.robot.subsystems:
                    system.feedback()

class OutputThread(threading.Thread):
    """Runs motors and output value"""
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot

    def run(self):
        while True:
            if self.robot.enabled:
                for system in self.robot.subsystems:
                    system.calc_setpoint()
                    system.update()

class Robot(object):
    def __init__(self):
        self.enabled = False
        self.subsystems = [
            Shooter(), #Ejector(), Elevator(),
        ]

        self.output = OutputThread(self)
        self.output.setDaemon(True)
        self.output.start()
        self.feedback = FeedbackThread(self)
        self.feedback.setDaemon(True)
        self.feedback.start()

    def enable(self, enabled):
        """Enables and disables the robot and subsystems"""
        self.enabled = enabled
        for subsystem in self.subsystems:
            subsystem.enabled = enabled

if __name__ == "__main__":
    tails_bot = Robot()
    operator = Controller(tails_bot)
    operator.map_input()
