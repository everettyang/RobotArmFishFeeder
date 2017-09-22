#!/usr/bin/python
import controller_class as cc
import time

def speed_return(speed):
    p.claw_toggle()
    p.set_left(9.0, speed)
    p.set_right(2.0, speed)
    p.set_base(7, speed)

p = cc.Controller(9.0,2)
speed = .05
grab_reach = 2.8 
deposit_reach = 5.5

p.claw_toggle()
#fetching config
p.set_left(9, speed)
p.set_right(grab_reach, speed)
p.set_left(7.9, speed)


p.claw_toggle()

time.sleep(.05)

#goes to deposit load
p.set_left(9, speed)
p.set_right(2, speed)
p.set_base(12, speed)
p.set_right(deposit_reach, speed)

time.sleep(.5)
p.claw_toggle()
time.sleep(.5)

speed_return(speed)

print "Done"
