from ili934xnew import ILI9341, color565
from machine import Pin, SPI
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
import time
from random import randint

class button:
    def __init__(self):
        self.count = 0
        self.pushed_flag = False
        
    def pressButton(self, push):
        if push != True and self.pushed_flag == False:
            self.count += 1
            self.pushed_flag = True
            
        if push == True and self.pushed_flag == True:
            self.pushed_flag = False
            
        return self.count

#Setup display stuff
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

print(os.uname())
TFT_CLK_PIN = const(6)
TFT_MOSI_PIN = const(7)
TFT_MISO_PIN = const(4)

TFT_CS_PIN = const(13)
TFT_RST_PIN = const(14)
TFT_DC_PIN = const(15)


spi = SPI(
    0,
    baudrate=40000000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))
print(spi)

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

display.erase()
display.set_pos(0,0)
display.set_font(tt32)
display.set_color(color565(255, 0, 0), color565(150, 150, 150))
display.erase()
display.set_pos(0,0)

count = 0
countTitle = "Count: "
countTitleSize = len(countTitle)

display.chars(countTitle, 0, 0)

addPin = Pin(17, Pin.IN)
subtractPin = Pin(16, Pin.IN)
addButton = button()
subtractButton = button()

while True:
    addC = addButton.pressButton(addPin.value())
    subtractC = subtractButton.pressButton(subtractPin.value())
    display.chars(" " + str(addC-subtractC) + " ", 100, 0)
    
        