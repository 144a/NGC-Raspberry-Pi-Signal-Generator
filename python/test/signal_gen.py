#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch54
from lib import LCD_1inch3
from PIL import Image,ImageDraw,ImageFont

import RPi.GPIO as GPIO
import subprocess

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 

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

# Horizontal input must be a multiple of 8
def change_resolution(n, m, framerate):
    mode = f'{n}x{m}_{framerate}.00'
    cvt_data = f'{n} {m} {framerate}'

    print(mode)
    print(cvt_data)


    try:
        output = subprocess.check_output('xrandr -s ' + mode, shell=True)
    except:

        print('Resolution Does Not Exist!! Adding new Resolution')
        output = subprocess.check_output(f'cvt {cvt_data}'.encode('utf-8'), shell=True)
        output = output.decode('utf-8')

        modeline = output.split('\n')[1]
        modeline = modeline[(modeline.index('ine')+4):(len(modeline))]

        print(modeline)
        output = subprocess.check_output('xrandr --newmode ' + modeline, shell=True)
        output = output.decode('utf-8')

        output = subprocess.check_output('xrandr --addmode HDMI-1 ' + mode, shell=True)
        output = output.decode('utf-8')

        output = subprocess.check_output('xrandr -s ' + mode, shell=True)
        output = output.decode('utf-8')

    time.sleep(5)

    output = subprocess.check_output('xrandr -s 1600x1200 -r 60', shell=True)
    output = output.decode('utf-8')

# Cursor State (-1 for view, 1 for edit)
cur_state = -1

# Resolution info array:
res_info = [640, 480, 60]
cur_id = 0

# Swap Between Edit and View States
def click_b1(input):
    global res_info, cur_state
    cur_state *= -1
    print('Pressed button 1')
def click_b2(input):
    global res_info
    print('Pressed button 2')
# Execute Resolution Change
def click_b3(input):
    global res_info
    print('Pressed button 3')
    change_resolution(res_info[0], res_info[1], res_info[2])

def joy_left(input):
    global res_info, cur_state, cur_id
    print('Pressed Joystick Left')
    res_info[cur_id] -= [8, 10, 5][cur_id]
def joy_right(input):
    global res_info, cur_state, cur_id
    print('Pressed Joystick Right')
    res_info[cur_id] += [8, 10, 5][cur_id]
def joy_up(input):
    global res_info, cur_state, cur_id
    if cur_id > 0:
        cur_id -= 1
    print('Pressed Joystick Up')
def joy_down(input):
    global res_info, cur_state, cur_id
    if cur_id < len(res_info) - 1:
        cur_id += 1
    print(cur_id)
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
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    # disp = LCD_1inch3.LCD_1inch3(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch3.LCD_1inch3()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)

    cnt = 0

    while True:

        # Create blank image for drawing.
        image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)

        Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
        Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
        Font3 = ImageFont.truetype("../Font/Font02.ttf",20)

        draw.text((5, 10), 'NoClue Games Portable', fill = "BLACK",font=Font3)
        draw.text((5, 30), 'Variable Signal Generator', fill ="BLACK",font=Font3)
        draw.text((5, 50), f'Horizontal: {str(res_info[0])}', fill = ["BLACK", "BLUE"][cur_id == 0],font=Font3)
        draw.text((5, 70), f'Vertical: {str(res_info[1])}', fill = ["BLACK", "BLUE"][cur_id == 1],font=Font3)
        draw.rectangle([(5,90),(150,150)],fill = "WHITE")
        draw.text((5, 90), f'Framerate: {str(res_info[2])}', fill = ["BLACK", "BLUE"][cur_id == 2],font=Font3)


        im_r=image1.rotate(0)
        disp.ShowImage(im_r)

    disp.module_exit()
except KeyboardInterrupt:
    disp.module_exit()
    GPIO.cleanup()
    exit()
