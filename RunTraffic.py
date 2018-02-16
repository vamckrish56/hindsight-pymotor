import RPi.GPIO as GPIO
import time
import signal
import sys
import requests

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


# Turn off all lights when user ends demo
def allLightsOff(signal, frame):
    lightsOff()
    GPIO.cleanup()
    sys.exit(0)


def lightsOff():
    GPIO.output(9, False)   # RED
    GPIO.output(10, False)  # YELLOW
    GPIO.output(11, False)  # GREEN
    GPIO.output(16, False)  # GREEN
    GPIO.output(20, False)  # RED
    GPIO.output(21, False)  # YELLOW


signal.signal(signal.SIGINT, allLightsOff)

# Loop forever
while True:
    print 'hello'
    resp = requests.get('http://localhost:5000/app/teamcity/builds/buildType:(id:uds),branch:develop')
    uat_resp = requests.get('http://localhost:5000/app/teamcity/builds/buildType:(id:uds),branch:uat')

    state = resp.text
    uat_state = uat_resp.text

    lightsOff()

    print state
    print uat_state

    # Red
    if state == 'RED':
        GPIO.output(10, False)
        GPIO.output(11, False)
        GPIO.output(9, True)

    # Green
    if state == 'GREEN':
        GPIO.output(9, False)
        GPIO.output(10, False)
        GPIO.output(11, True)

    # Amber
    if state == 'YELLOW':
        GPIO.output(11, False)
        GPIO.output(9, False)
        GPIO.output(10, True)

    # Red
    if uat_state == 'RED':
        GPIO.output(21, False)
        GPIO.output(20, True)
        GPIO.output(16, False)

    # Green
    if uat_state == 'GREEN':
        GPIO.output(21, False)
        GPIO.output(20, False)
        GPIO.output(16, True)



    time.sleep(5)
