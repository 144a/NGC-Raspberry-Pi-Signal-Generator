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

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
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

        logging.info("draw text")
        Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
        Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
        Font3 = ImageFont.truetype("../Font/Font02.ttf",20)

        draw.text((5, 10), 'NoClue Games Portable', fill = "BLACK",font=Font3)
        draw.text((5, 30), 'Variable Video Generator', fill ="BLACK",font=Font3)
        draw.text((5, 50), 'Horizontal: 640', fill ="BLACK",font=Font3)
        draw.text((5, 70), 'Vertical: 480', fill = "BLACK",font=Font3)
        draw.rectangle([(5,90),(150,150)],fill = "WHITE")
        draw.text((5, 90),str(cnt), fill = "BLUE",font=Font3)
        im_r=image1.rotate(0)
        disp.ShowImage(im_r)

        cnt += 1
    
    disp.module_exit()
    logging.info("quit:")
    
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
