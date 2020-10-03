# Write your code here :-)
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.D17)
led.direction = digitalio.Direction.OUTPUT
i = 0

while True:
    print("hello")
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
