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
        self.position = 0 #add motor reset

    def update(self):
        for motor in self.motors:
            motor.duty_cycle_sp = self.output
            motor.run_direct()

    @abstractmethod
    def calc_setpoint(self):
        self.output = self.setpoint #shouldn't be the case

    @abstractmethod
    def feedback(self):
        pass

