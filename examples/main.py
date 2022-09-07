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

                
fonts = [glcdfont,tt14,tt24,tt32]
text = 'Hello Raspberry Pi Pico'


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
display.set_font(tt24)
display.set_color(color565(255, 0, 0), color565(150, 150, 150))
display.print("\nPico Breadboard kit:")
display.print("Pico Breadboard kit show")
time.sleep(1)
for i in range(170):
    display.scroll(1)
    time.sleep(0.01)
    
time.sleep(1)
for i in range(170):
    display.scroll(-1)
    time.sleep(0.01)

time.sleep(0.5)
display.erase()



while True:
    for x in range(0, 320, 20):
        display.set_pos(0,0)
        display.set_color(color565(255, 255, 0), color565(150, 150, 150))
        display.print("New: \n")
        display.print("52Pi Pico Screen Show")
        display.print("Have a nice day!!!")
        time.sleep(1)
        display.erase()
        
        display.set_pos(20, x)
        display.set_color(color565(randint(0,255), randint(0,255), randint(0,255)), color565(randint(0,255), randint(0,255), randint(0,255)))
        display.print("www.52pi.com")
        time.sleep(1)
        display.erase()
             
       
print('-bye -')