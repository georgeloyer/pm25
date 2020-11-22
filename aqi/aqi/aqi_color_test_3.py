"""
presents 125 graded colors to test the Clue display
cycles through 5 sets of 25 variations
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
MAXWIDTH = 120
MAXHEIGHT = 120
INCWIDTH = MAXWIDTH/5
INCHEIGHT = MAXHEIGHT/5
rects = []
rgb_increments = (0x00, 0x40, 0x80, 0xc0, 0xff)

for rect in range(25):
    x = (rect % 5) * INCWIDTH
    y = (rect % 5) * INCHEIGHT
    w = INCWIDTH -1
    h = INCHEIGHT -1
    rects.append( Rect(x, y, w, h) )
    group.append(rects[rect])

display.show(group)
time.sleep(0.01)

while True:
    time.sleep(1)

    for green in rgb_increments:
        rects_index = 0
        for blue in rgb_increments:
            for red in rgb_increments:
                colorcode = blue + 0x100 * green + 0x10000 * red
                rects[rects_index].fill(colorcode)
                rects_index += 1
        time.sleep(10)
