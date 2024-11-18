import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Steer:
    def __init__(self, servo_pin: int):
        GPIO.setup(servo_pin, GPIO.OUT)
        self._pwm = GPIO.PWM(servo_pin, 100)
        self._pwm.start(15)

    def set_angle(self, angle):
        angle = max(50, min(130, angle))

        duty: float = 5.85 + angle / 9
        self._pwm.ChangeDutyCycle(duty)

    def cleanup(self):
        self._pwm.stop()


class Motor:
    def __init__(self, in1_pin, in2_pin, en_pin):
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.en_pin = en_pin
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.en_pin, 200)
        self.pwm.start(0)
        self.backward_flag: bool = False
        self.forward_flag: bool = False

    def set_speed(self, speed):
        speed = max(0, min(100, speed))
        self.pwm.ChangeDutyCycle(speed)

    def forward(self):
        self.forward_flag = True
        self.backward_flag = False
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)

    def backward(self):
        self.backward_flag = True
        self.forward_flag = False
        GPIO.output(self.in2_pin, GPIO.HIGH)
        GPIO.output(self.in1_pin, GPIO.LOW)

    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)
        self.backward_flag = False
        self.forward_flag = False

    def cleanup(self):
        self.pwm.stop()


class IR:
    def __init__(self, ir_pin):
        self._ir_pin = ir_pin
        GPIO.setup(self._ir_pin, GPIO.IN)

    def get_value(self):
        return GPIO.input(self._ir_pin) == 0


def cleanup():
    GPIO.cleanup()
