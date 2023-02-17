from machine import Pin, Timer

led = Pin(0, Pin.OUT) #connect Pin 0 to an LED
LED_state = True
tim = Timer()

def tick(timer):
    global led, LED_state
    LED_state = not LED_state
    print(LED_state)
    led.value(LED_state)

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)