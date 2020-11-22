"""
colorcode test with clue display hardware
"""

# pylint: disable=unused-import
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_pm25
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle

from aqi import Aqi

my_aqi = Aqi()      # initialize Aqi class

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False

# arial12 = bitmap_font.load_font("/fonts/Arial-12.bdf")
arial16 = bitmap_font.load_font("/fonts/Arial-16.bdf")
# arial24 = bitmap_font.load_font("/fonts/Arial-Bold-24.bdf")

display = board.DISPLAY

group = displayio.Group(max_size=25)
# outer_circle = Circle(120, 120, 119, outline=0xFFFFFF, stroke=30)
# group.append(outer_circle)

inner_circle = Circle(120, 120, 60, fill= 0xFFFFFF, outline=0xFFFFFF)
group.append(inner_circle)

display.show(group)
time.sleep(0.01)

while True:
    time.sleep(1)

    for colorcode in range(0xff7e00, 0xff7eff):
        inner_circle.outline = colorcode
        inner_circle.fill = colorcode
        print ("colorcode: 0x%06X" % colorcode)
        # time.sleep(1)
