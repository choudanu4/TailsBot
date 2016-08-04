"""Subsystem Abstract Class"""

from abc import ABC, abstractmethod

class Subsystem(ABC, object):
    """Class that subsystems inherit from"""
    def __init__(self):
        self.setpoint = 0 #subsystem specific
        self.enabled = False
        self.position = 0
        self.velocity = 0
        self.output = 0 #motor duty cycle
        self.motors = []

    def reset(self):
        """Resets motor and sensor readings"""
        self.position = 0 #add motor reset

    def update(self):
        """Pushes ouput to motors"""
        for motor in self.motors:
            motor.run_direct(duty_cycle_sp=self.output)

    @abstractmethod
    def calc_setpoint(self):
        """Infers a output from a setpoint"""
        if self.enabled:
            self.output = self.output #shouldn't be the case
        else:
            self.output = 0

    @abstractmethod
    def feedback(self):
        """Sends feedback such as motor position and sensor values"""
        pass

