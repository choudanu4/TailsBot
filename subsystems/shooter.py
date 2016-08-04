from subsystems.subsystem import Subsystem
import ev3dev.ev3 as ev3

class Shooter(Subsystem):
    def __init__(self):
        super(Shooter, self).__init__()
        self.motors = ev3.LargeMotor(ev3.OUTPUT_B), ev3.LargeMotor(ev3.OUTPUT_C)
        self.motors[0].polarity = "inversed"

    def calc_setpoint(self):
        """Derives duty_cycle for motors from desired flatwheel RPM"""
        if self.setpoint:
            self.ouput = 100
        else:
            self.output = 0

    def feedback(self):
        """Updates position and velocity readouts"""
        self.position = None #We don't care'
        self.velocity = self.motors[0].speed / self.motors[0].count_per_rot
