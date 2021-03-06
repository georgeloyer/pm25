# Purple Air AQI Display
# for Metro M4 Airlift with RGB Matrix Shield
# or Matrix Portal
# and 64 x 32 RGB LED Matrix

import time
import board
import terminalio
import busio
from adafruit_pm25.i2c import PM25_I2C
from adafruit_matrixportal.matrixportal import MatrixPortal

def aqi_transform(val):
    aqi = pm_to_aqi(val)  # derive Air Quality Index from Particulate Matter 2.5 value
    return "AQI:%d" % aqi

def message_transform(val):  # picks message based on thresholds
    index = aqi_to_list_index(pm_to_aqi(val))
    messages = (
        "Hazardous",
        "Very Unhealthy",
        "Unhealthy",
        "Unhealthy for Sensitive Groups",
        "Moderate",
        "Good",
    )

    if index is not None:
        return messages[index]
    return "Unknown"

SENSOR_ID = 69897 # Ashbury Terrace, SF
SENSOR_REFRESH_PERIOD = 30  # seconds
DATA_SOURCE = "https://www.purpleair.com/json?show=" + str(SENSOR_ID)
SCROLL_DELAY = 0.02
DATA_LOCATION = ["results", 0, "PM2_5Value"]  # navigate the JSON response

# --- Display setup ---
matrixportal = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
    debug=True,
    url=DATA_SOURCE,
    json_path=(DATA_LOCATION, DATA_LOCATION),
)

# Create a static label to show AQI
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, 7),
    text_transform=aqi_transform,
)

# Create a scrolling label to show level message
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, 23),
    scrolling=True,
    text_transform=message_transform,
)
# pylint: disable=too-many-return-statements
def aqi_to_list_index(aqi):
    aqi_groups = (301, 201, 151, 101, 51, 0)
    for index, group in enumerate(aqi_groups):
        if aqi >= group:
            return index
    return None

def calculate_aqi(Cp, Ih, Il, BPh, BPl):  # wikipedia.org/wiki/Air_quality_index#Computing_the_AQI
    return round(((Ih - Il)/(BPh - BPl)) * (Cp - BPl) + Il)

def pm_to_aqi(pm):
    pm = float(pm)
    if pm < 0:
        return pm
    if pm > 1000:
        return 1000
    if pm > 350.5:
        return calculate_aqi(pm, 500, 401, 500, 350.5)
    elif pm > 250.5:
        return calculate_aqi(pm, 400, 301, 350.4, 250.5)
    elif pm > 150.5:
        return calculate_aqi(pm, 300, 201, 250.4, 150.5)
    elif pm > 55.5:
        return calculate_aqi(pm, 200, 151, 150.4, 55.5)
    elif pm > 35.5:
        return calculate_aqi(pm, 150, 101, 55.4, 35.5)
    elif pm > 12.1:
        return calculate_aqi(pm, 100, 51, 35.4, 12.1)
    elif pm >= 0:
        return calculate_aqi(pm, 50, 0, 12, 0)
    else:
        return None

def get_color(aqi):
    index = aqi_to_list_index(aqi)
    colors = (
        (115, 20, 37),
        (140, 26, 75),
        (234, 51, 36),
        (239, 133, 51),
        (255, 255, 85),
        (104, 225, 67),
    )
    if index is not None:
        return colors[index]
    return (150, 150, 150)

sensor_refresh = None

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False

# Create library object, use 'slow' 100KHz frequency!
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")

while True:
    if (not sensor_refresh) or (time.monotonic() - sensor_refresh) > SENSOR_REFRESH_PERIOD:
        try:
            value = matrixportal.fetch()
            print("PurpleAir response is", value[0])
            matrixportal.set_text_color(get_color(pm_to_aqi(value[0])))
            sensor_refresh = time.monotonic()
        except RuntimeError as e:
            print("Unable to read from PurpleAir, retrying...", e)
            continue
        try:
            aqdata = pm25.read()
            print("Local PlanTower PM2.5 reading is", aqdata["particles 25um"])
            matrixportal.set_text(aqi_transform(value[0]) + " " + str(pm_to_aqi(aqdata["particles 25um"])), 0)
        except RuntimeError as e:
            print("Unable to read from local sensor, retrying...", e)
        continue

    # Scroll it
    matrixportal.scroll_text(SCROLL_DELAY)