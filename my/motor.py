#######
# Orig Author: James Poole
# Date: 23 April 2016
# modified for CamJam EduKit 3 Worksheet 4
#by F.Sofras
# my.py
#######

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  ")

#import RPi.GPIO as GPIO # Import the GPIO Library
from time import sleep # Import the Time library

#print('Set the GPIO modes')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#sleep(2)

#print(' Set variables for the GPIO motor pins')
pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7
#sleep(2)

#print(' Set the GPIO Pin mode')
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)
sleep(1)

# How many times to turn the pin on and off each second
Frequency = 20
# How long the pin stays on each cycle, as a percent (here, it's 30%)
# Setting the duty cycle to 0 means the motors will not turn
DutyCycleA = 0
DutyCycleB = 0

#print('Set the GPIO to software PWM at ' ,Frequency, ' Hertz')
pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, Frequency)
pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)
#sleep(1)

#print('start with motors stopped')
pwmMotorAForwards.start(0)
pwmMotorABackwards.start(0)
pwmMotorBForwards.start(0)
pwmMotorBBackwards.start(0)
#sleep(2)


def Motor_dc(lf,rf,lb,rb):
    pwmMotorAForwards.ChangeDutyCycle(lf)
    pwmMotorBForwards.ChangeDutyCycle(rf)
    pwmMotorABackwards.ChangeDutyCycle(lb)
    pwmMotorBBackwards.ChangeDutyCycle(rb)
          

'''
Motor_dc(70,70,0,0)
sleep (5)

GPIO.cleanup()
'''