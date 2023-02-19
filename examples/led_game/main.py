from ili934xnew import ILI9341, color565
from machine import Pin, SPI, PWM
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
import time
from random import randint

#Setup display stuff
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
#SCR_ROT = const(2)
SCR_ROT = const(3)
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

class buzzer:
    def __init__(self, pin):
        self.buzzerPin = PWM(Pin(pin))
        self.buzzerPin.freq(500)
        
        
    def shortBeep(self):
        self.buzzerPin.freq(5000)
        self.buzzerPin.duty_u16(100000)
        time.sleep(2)
        self.buzzerPin.duty_u16(0)
        
    def startPlayingNote(self, note,volume):
        self.buzzerPin.freq(note)
        self.buzzerPin.duty_u16(volume)
        
    def stopPlayingNote(self):
        self.buzzerPin.duty_u16(0)

class ledButton:
    def __init__(self, buttonPinNum, ledPinNum, buzzer, note, volume):
        self.buttonPin = Pin(buttonPinNum, Pin.IN)
        self.ledPin = Pin(ledPinNum, Pin.OUT)
        self.buzzer = buzzer
        self.note = note
        self.volume = volume
        
        
    def checkPress(self):
        pushed = not self.buttonPin.value()
        self.ledPin.value(pushed)
        return pushed
    
    def checkFullPress(self):
        pushed = not self.buttonPin.value()
        if(pushed):
            self.ledPin.value(True)
            self.buzzer.startPlayingNote(self.note, self.volume)
            while True:
                notPushed = self.buttonPin.value()
                if(notPushed):
                    self.ledPin.value(False)
                    self.buzzer.stopPlayingNote()
                    return True
        else:
            return False
    
    def unPress(self):
        self.ledPin.value(False)
        
    def blink(self):
        self.ledPin.value(True)
        self.buzzer.startPlayingNote(self.note, self.volume)
        time.sleep(1)
        self.ledPin.value(False)
        self.buzzer.stopPlayingNote()
        
class gameEngine:
    def __init__(self, display, button0, button1, button2, button3, buzzer):
        self.display = display
        self.sequence = [0,1,2,3]
        self.userSequenceIndex = 0
        self.sequenceIndex = 0
        self.buttons = [button0, button1, button2, button3]
        self.buzzer = buzzer
        self.blinkFlag = True
        
    def run(self):
        if(self.blinkFlag):
            self.blinkSequence()
        else:
            self.collectUserSequence()
    
    def blinkSequence(self):
        print(str(self.sequenceIndex) + " " + str(self.blinkFlag))
        display.chars(" " + str(len(self.sequence) - self.sequenceIndex) + " ", 100, 0)
        if(self.sequenceIndex >= len(self.sequence)):
            self.blinkFlag = False
            self.sequenceIndex = 0
        else:
            currentSeq = self.sequence[self.sequenceIndex]
            self.buttons[currentSeq].blink()
            self.sequenceIndex += 1
            
    def collectUserSequence(self):
        indexPressed = 0
        for button in self.buttons:
            if(button.checkFullPress()):
                expectedIndex = self.sequence[self.userSequenceIndex]
                print("Index pressed: " + str(indexPressed) + ", expected index: " + str(expectedIndex))
                if(expectedIndex != indexPressed):
                    self.buzzer.shortBeep()
                    self.blinkFlag = True
                    self.userSequenceIndex = 0
                    return
                if(self.userSequenceIndex+1 == len(self.sequence)):
                    self.blinkFlag = True
                    self.userSequenceIndex = 0
                    return
                self.userSequenceIndex += 1
            else:
                indexPressed += 1
        

#f = open("count.txt")
#print(f.read())
#f.close()

count = 0
countTitle = "Count: "
countTitleSize = len(countTitle)

display.chars(countTitle, 0, 0)
buzz = buzzer(18)
button1 = ledButton(0,1, buzz, 750, 14000)
button2 = ledButton(2,3, buzz, 600, 11000)
button3 = ledButton(16,17, buzz, 500, 9500)
button4 = ledButton(10,11, buzz, 400, 80000)

engine = gameEngine(display, button1, button2, button3, button4, buzz)

while True:
    engine.run()
    #button1.checkPress()
    #button2.checkPress()
    #button3.checkPress()
    #button4.checkPress()
    
        