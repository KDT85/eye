#import libraries
from machine import Pin, PWM
from time import sleep

#set up pins
eye = PWM(Pin(0))
lid = PWM(Pin(1))

eye.freq(50)
lid.freq(50)

left = 2000
right = 7500
middle = 5000

opn = 6000
clsd = 4000

#servo functions
def setEyeCycle(position):
    eye.duty_u16(position)
    sleep(0.01)
    
def setLidCycle(position):
    lid.duty_u16(position)
    sleep(0.01)
    
def look(direction):
    eye.duty_u16(direction)
    sleep(0.01)
    
def eye_lid(opnclsd):
    lid.duty_u16(opnclsd)
    sleep(0.01)

    
while True:
    
    #eye left right
    for i in range(2):
        for pos in range(middle, right, 50):
            setEyeCycle(pos)
        for pos in range(right, left, -50):
            setEyeCycle(pos)
        for pos in range(left, middle, 50):
            setEyeCycle(pos)
    
    #lid bink
    for pos in range(clsd, opn, 50):
        setLidCycle(pos)
    for pos in range(opn, clsd, -50):
        setLidCycle(pos)
