import RPi.GPIO as GPIO
import time

JS_U_PIN = 6  #Joystick Up
JS_D_PIN = 19 #Joystick Down
JS_L_PIN = 5  #Joystick Left
JS_R_PIN = 26 #Joystick Right
JS_P_PIN = 13 #Joystick Pressed
BTN1_PIN = 21
BTN2_PIN = 20
BTN3_PIN = 16


# init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(JS_U_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_D_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_L_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_R_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_P_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

def click_b1(input):
    print('Pressed button 1')
def click_b2(input):
    print('Pressed button 2')
def click_b3(input):
    print('Pressed button 3')

def joy_left(input):
    print('Pressed Joystick Left')
def joy_right(input):
    print('Pressed Joystick Right')
def joy_up(input):
    print('Pressed Joystick Up')
def joy_down(input):
    print('Pressed Joystick Down')


# Add Events
GPIO.add_event_detect(BTN1_PIN, GPIO.RISING, callback=click_b1, bouncetime=200)
GPIO.add_event_detect(BTN2_PIN, GPIO.RISING, callback=click_b2, bouncetime=200)
GPIO.add_event_detect(BTN3_PIN, GPIO.RISING, callback=click_b3, bouncetime=200)
GPIO.add_event_detect(JS_L_PIN, GPIO.RISING, callback=joy_left, bouncetime=200)
GPIO.add_event_detect(JS_R_PIN, GPIO.RISING, callback=joy_right, bouncetime=200)
GPIO.add_event_detect(JS_U_PIN, GPIO.RISING, callback=joy_up, bouncetime=200)
GPIO.add_event_detect(JS_D_PIN, GPIO.RISING, callback=joy_down, bouncetime=200)

try:
    while True:
        time.sleep(1)
except:
    GPIO.cleanup()
