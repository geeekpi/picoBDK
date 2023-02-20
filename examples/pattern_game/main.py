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

#Classes to run the game
class buzzer:
    def __init__(self, pin):
        self.buzzerPin = PWM(Pin(pin))
        self.buzzerPin.freq(500)
        
    def startPlayingNote(self, note,volume):
        self.buzzerPin.freq(note)
        self.buzzerPin.duty_u16(volume)
        
    def stopPlayingNote(self):
        self.buzzerPin.duty_u16(0)

class LEDButton:
    def __init__(self, buttonPinNum, ledPinNum, buzzer, note, volume):
        self.buttonPin = Pin(buttonPinNum, Pin.IN)
        self.ledPin = Pin(ledPinNum, Pin.OUT)
        self.buzzer = buzzer
        self.note = note
        self.volume = volume
    
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
    
    def ledOff(self):
        self.ledPin.value(False)
    
    def ledOn(self):
        self.ledPin.value(True)
        
    def blink(self):
        self.ledPin.value(True)
        self.buzzer.startPlayingNote(self.note, self.volume)
        time.sleep(.5)
        self.ledPin.value(False)
        self.buzzer.stopPlayingNote()
        
class Sequence:
    def __init__(self):
        self.sequence = []
        self.increaseSequence()
        self.increaseSequence()
        self.increaseSequence()
        self.currentIndex = 0
        
    def checkComplete(self):
        return (self.currentIndex >= len(self.sequence))
    
    def resetCurrentIndex(self):
        self.currentIndex = 0
        
    def nextIndex(self):
        nextIndex = self.sequence[self.currentIndex]
        self.currentIndex += 1
        return nextIndex
    
    def checkUserInput(self, indexPressed):
        expectedIndex = self.nextIndex()
        print("Index pressed: " + str(indexPressed) + ", expected index: " + str(expectedIndex))
        return indexPressed == expectedIndex
    
    def remaining(self):
        return len(self.sequence) - self.currentIndex
    
    def increaseSequence(self):
        newSeq = randint(0,3)
        self.sequence.append(newSeq)
        self.resetCurrentIndex()
        
    def currentSize(self):
        return len(self.sequence)
        
        
class gameEngine:
    def __init__(self, display, button0, button1, button2, button3, buzzer):
        self.display = display
        self.sequence = Sequence()
        self.buttons = [button0, button1, button2, button3]
        self.buzzer = buzzer
        self.blinkFlag = True
        self.pauseFlag = True
        f = open("highscore")
        self.highscore = int(f.read())
        f.close()
        display.chars("Current Highscore: " + str(self.highscore), 0, 0)
        display.chars("Ready?               ", 0, 30)
        display.chars("Remaining: ", 0, 90)
        
    def run(self):
        if(self.pauseFlag):
            for button in self.buttons:
                if(button.checkFullPress()):
                    self.pauseFlag = False
                    display.chars("                 ", 0, 60)
                    time.sleep(1)
        else:
            if(self.blinkFlag):
                self.blinkSequence()
            else:
                self.collectUserSequence()
        
    def blinkSequence(self):
        display.chars(" " + str(self.sequence.remaining()) + " ", 150, 90)
        if(self.sequence.checkComplete()):
            self.blinkFlag = False
            self.sequence.resetCurrentIndex()
        else:
            currentSeq = self.sequence.nextIndex()
            self.buttons[currentSeq].blink()
            
    def collectUserSequence(self):
        if(self.sequence.checkComplete()):
            # completed sequence correctly!
            display.chars("Nice!                            ", 0, 30)
            self.blinkFlag = True
            self.sequence.increaseSequence()
        else:
            display.chars(" " + str(self.sequence.remaining()) + " ", 150, 90)
            indexPressed = 0
            for button in self.buttons:
                if(button.checkFullPress()):
                    if(not self.sequence.checkUserInput(indexPressed)):
                        score = self.sequence.currentSize() - 1
                        if(score > self.highscore):
                            display.chars("New Highscore! " + str(score), 0, 30)
                            display.chars("Current Highscore: " + str(score), 0, 0)
                            f = open("highscore", "w")
                            f.write(str(score))
                            f.close()
                        else:
                            display.chars("Game over, score: " + str(score) + "                 ", 0, 30)
                        display.chars("Try again?             ", 0, 60)
                        self.wrongGuess()
                        
                        return
                else:
                    indexPressed += 1
                    
    def wrongGuess(self):
        i = 0
        while (i < 4):
            i+=1
            if(i < 2):
                self.buzzer.startPlayingNote(500,10000)
            else:
                self.buzzer.startPlayingNote(300,10000)
                
            time.sleep(.2)
            for button in self.buttons:
                button.ledOn()
            time.sleep(.2)
            for button in self.buttons:
                button.ledOff()
                
        self.buzzer.stopPlayingNote()
                
        self.blinkFlag = True
        self.pauseFlag = True
        del self.sequence
        self.sequence = Sequence()
                    
#Wiring information
#To use the code as is follow the comments
buzz = buzzer(18)                             #Pin 18 to Beep
button1 = LEDButton(0,1, buzz, 750, 14000)    #Pin 0 to k4 and Pin 1 to LED1
button2 = LEDButton(2,3, buzz, 600, 11000)    #Pin 2 to k3 and Pin 3 to LED2
button3 = LEDButton(16,17, buzz, 500, 9500)   #Pin 16 to k2 and Pin 17 to LED3
button4 = LEDButton(10,11, buzz, 400, 80000)  #Pin 10 to k1 and Pin 11 to LED4

engine = gameEngine(display, button1, button2, button3, button4, buzz)

while True:
    engine.run()
        