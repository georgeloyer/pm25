"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
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
outer_circle = Circle(120, 120, 119, outline=0xFFFFFF, stroke=60)
inner_circle = Circle(120, 120, 60, fill= 0xFFFFFF, outline=0xFFFFFF)
group.append(outer_circle)
group.append(inner_circle)

title = label.Label(font=arial16, x=15, y=25, text="", color=0x000000, max_glyphs=30)
group.append(title)

level1 = label.Label(font=arial16, x=15, y=50, text="", color=0x000000, max_glyphs=30)
group.append(level1)

level2 = label.Label(font=arial16, x=15, y=75, text="", color=0x000000, max_glyphs=30)
group.append(level2)

level3 = label.Label(font=arial16, x=15, y=100, text="", color=0x000000, max_glyphs=30)
group.append(level3)

level4 = label.Label(font=arial16, x=100, y=125, text=" ", color=0x000000, max_glyphs=30)
group.append(level4)

level5 = label.Label(font=arial16, x=15, y=150, text="", color=0x000000, max_glyphs=30)
group.append(level5)

level6 = label.Label(font=arial16, x=15, y=175, text="", color=0x000000, max_glyphs=30)
group.append(level6)

level7 = label.Label(font=arial16, x=100, y=200, text="", color=0x000000, max_glyphs=30)
group.append(level7)

display.show(group)
time.sleep(0.01)

# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = adafruit_pm25.PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")

while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    raw_25 = aqdata["pm25 env"]
    raw_10 = aqdata["pm100 env"]
    aqi_25 = my_aqi.sensor_to_aqi(raw_25, "None", "2.5")
    category_25 = my_aqi.category
    colorname_25 = my_aqi.colorname
    colorcode_25 = my_aqi.colorcode
    aqi_10 = my_aqi.sensor_to_aqi(raw_10, "None", "10.0")
    category_10 = my_aqi.category
    colorname_10 = my_aqi.colorname
    colorcode_10 = my_aqi.colorcode
    outer_circle.outline = colorcode_10
    inner_circle.outline = colorcode_25
    inner_circle.fill = colorcode_25
#    level1.text = "PM 2.5 AQI:   " + str(aqi_25)
#    level2.text = category_25
#    level3.text = colorname_25
    level4.text = str(aqi_25)
#    level5.text = "PM 10.0 AQI:  " + str(aqi_10)
#    level6.text = category_10
#    level7.text = colorname_10
    level7.text = str(aqi_10)
    print("10.0: %X   2.5: %X" % (colorcode_10, colorcode_25))
