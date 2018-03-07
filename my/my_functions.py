#myfunctions.py    
    
############################

import RPi.GPIO as GPIO 
import time 

################################

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 17 
ECHO = 18
LedPin = 25   


GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output

GPIO.output(TRIG, False)
GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led
#print ("Waiting For Sensor To Settle")

#-----------------------------------
def distance_detected(tdist=[]):
    pulse_start = 0
    pulse_end = 0

    for cntr in range(1, 10):
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
          pulse_start = time.time()
          #print (pulse_start)

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        tdist.append(pulse_duration * 34300/2)

    return int(median(tdist))

#--------------------------------------
def median(thelist):
    sorted_list = sorted(thelist)
    length = len(sorted_list)
    center = length // 2
    #print ('length',length)
    if length == 1:
        return sorted_list[0]
    elif length % 2 == 0:
        return sum(sorted_list[center - 1: center + 1]) / 2.0
    else:
        return sorted_list[center]

################################

def blink(on_off):
    if on_off=='on':
        GPIO.output(LedPin, GPIO.HIGH)  # led on
        time.sleep(1)
        GPIO.output(LedPin, GPIO.LOW) # led off
        time.sleep(1)
    else:
        GPIO.output(LedPin, GPIO.LOW)   # led off


    
