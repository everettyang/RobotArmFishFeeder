import RPi.GPIO as GPIO
import time

class Controller:

    """controls the mearm with variable PWM increments"""
    def __init__(self,  left_start = 7,  \
                    right_start = 4, \
                    claw_start = 7, \
                    base_start = 7.3,\
                    increment = .1,\
                    left_pin = 22, \
                    right_pin = 12,\
                    claw_pin = 16,\
                    base_pin = 18): 
                   
        """sets up PWM and starts them"""

        self.claw_status = False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(left_pin, GPIO.OUT)
        GPIO.setup(right_pin, GPIO.OUT)
        GPIO.setup(claw_pin, GPIO.OUT)
        GPIO.setup(base_pin, GPIO.OUT)

        self.left = GPIO.PWM(left_pin, 50) 
        self.right = GPIO.PWM(right_pin, 50) 
        self.claw = GPIO.PWM(claw_pin, 50) 
        self.base = GPIO.PWM(base_pin, 50) 

        self.left_start = left_start
        self.claw_start = claw_start
        self.right_start = right_start
        self.base_start = base_start
        self.increment = increment

        self.left.start(left_start)
        self.right.start(right_start)
        self.claw.start(claw_start)
        self.base.start(base_start)

    def change_increment(self, x):
            self.increment = x

    def make_neutral(self):
        
        self.left_start = 9    
        self.right_start = 2
        self.claw_start = 6.5
        self.base_start = 7  

        self.left.ChangeDutyCycle(self.left_start)
        self.right.ChangeDutyCycle(self.right_start)
        self.claw.ChangeDutyCycle(self.claw_start)
        self.base.ChangeDutyCycle(self.base_start)

        time.sleep(0.5)

    def claw_toggle(self, open_pwm = 4, close_pwm = 8):
        if not self.claw_status:
            self.claw.ChangeDutyCycle(open_pwm)
            self.claw_status = True
            time.sleep(.2)
            print "Claw opened"
        
        else:
            self.claw.ChangeDutyCycle(close_pwm)
            self.claw_status = False
            time.sleep(.2)
            print "Claw closed"

    def left_up(self):
        if self.left_start > 2:
            self.left.ChangeDutyCycle(self.left_start - self.increment)
            self.left_start -= self.increment
            print "Left: " + str(self.left_start)

    def left_down(self):

        if self.left_start < 11:
            self.left.ChangeDutyCycle(self.left_start + self.increment)
            self.left_start += self.increment
            print "Left: " + str(self.left_start)

    def right_up(self):
        if self.right_start > 2:
            self.right.ChangeDutyCycle(self.right_start - self.increment)
            self.right_start -= self.increment
            print "Right: " + str(self.right_start)

    def right_down(self):
        if self.right_start < 10:
            self.right.ChangeDutyCycle(self.right_start + self.increment)
            self.right_start += self.increment
            print "Right: " + str(self.right_start)

    def base_right(self):
        if self.base_start > 2:
            self.base.ChangeDutyCycle(self.base_start - self.increment)
            self.base_start -= self.increment
            print "Base: " + str(self.base_start)

    def base_left(self):
        if self.base_start < 12:
            self.base.ChangeDutyCycle(self.base_start + self.increment)
            self.base_start += self.increment
            print "Base: " + str(self.base_start)

    def manual_control(self):

        options = {'w': self.left_up, 's': self.left_down, \
                    'r': self.claw_toggle, 'a': self.right_up, 'd': self.right_down, \
                    'z': self.base_right, 'x': self.base_left, 'n': self.make_neutral}

        while True:

            command = raw_input() 
            function = options.get(command)
            if function:
                function()

    # sets duty cycles and allows for speed adjustment
    def set_left(self, x, speed = None, precision = .1):
        #convert to int (lose or gain negligible value in most cases)
        if x > 0 and x < 100 and not speed:
            self.left_start = x
            self.left.ChangeDutyCycle(x)
            time.sleep(.5)

        #speed and precision adjustment
        diff = self.left_start - x
        print "Difference: " + str(diff)

        if speed:
            if diff < 0:
                while self.left_start < x:
                    self.left.ChangeDutyCycle(self.left_start + precision)
                    time.sleep(speed)
                    self.left_start += precision
            else:
                while self.left_start > x:
                    self.left.ChangeDutyCycle(self.left_start - precision)
                    time.sleep(speed)
                    self.left_start -= precision
                
    def set_right(self, x, speed = None, precision = .1):
        if x > 0 and x < 100 and not speed:
            self.right_start = x
            self.right.ChangeDutyCycle(x)
            time.sleep(.5)

        diff = self.right_start - x
        print "Difference: " + str(diff)

        #speed and precision adjustment
        if speed:
            if diff < 0:

                while self.right_start < x:
                    self.right.ChangeDutyCycle(self.right_start + precision)
                    time.sleep(speed)
                    self.right_start += precision
            else:

                while self.right_start > x:
                    self.right.ChangeDutyCycle(self.right_start - precision)
                    time.sleep(speed)
                    self.right_start -= precision

    def set_claw(self, x, speed = None):
        self.claw_start = x
        if x > 0 and x < 100:
            self.claw.ChangeDutyCycle(x)

    def set_base(self, x, speed = None, precision = .1):

        if x > 0 and x < 100 and not speed:
            self.base_start = x
            self.base.ChangeDutyCycle(x)
            time.sleep(.5)

        diff = self.base_start - x

        if speed:
            if diff < 0:
                while self.base_start < x:
                    self.base.ChangeDutyCycle(self.base_start + precision)
                    time.sleep(speed)
                    self.base_start += precision
            else:
                while self.base_start > x:
                    self.base.ChangeDutyCycle(self.base_start - precision)
                    time.sleep(speed)
                    self.base_start -= precision


    def __del__(self):
        self.left.stop()
        self.right.stop()
        self.claw.stop()
        self.base.stop()
        GPIO.cleanup()
