from adafruit_clue import clue
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_pm25

clue.sea_level_pressure = 1020

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False

clue_data = clue.simple_text_display(title="CLUE Sensor Data!", title_scale=2)

# Create library object, use 'slow' 100KHz frequency!
# ERROR: P19 IN USE, which is what board.SCL and board.SDA are referencing. Already set up in clue
#   library, so need to find the reference or move the example code into clue library so it can
#   reference the opened port within the scope of the library.
#
# That would make the lines here unneeded and instead just a clue_data[i] set of indexed data
#   populated by the library code that is connecting to the I2C bus and returning the parsed data.

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = adafruit_pm25.PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")


while True:
    clue_data[0].text = "Acceleration: {:.2f} {:.2f} {:.2f}".format(*clue.acceleration)
    clue_data[1].text = "Gyro: {:.2f} {:.2f} {:.2f}".format(*clue.gyro)
    clue_data[2].text = "Magnetic: {:.3f} {:.3f} {:.3f}".format(*clue.magnetic)
    clue_data[3].text = "Pressure: {:.3f}hPa".format(clue.pressure)
    clue_data[4].text = "Altitude: {:.1f}m".format(clue.altitude)
    clue_data[5].text = "Temperature: {:.1f}C".format(clue.temperature)
    clue_data[6].text = "Humidity: {:.1f}%".format(clue.humidity)
    clue_data[7].text = "Proximity: {}".format(clue.proximity)
    clue_data[8].text = "Gesture: {}".format(clue.gesture)
    clue_data[9].text = "Color: R: {} G: {} B: {} C: {}".format(*clue.color)
    clue_data[10].text = "Button A: {}".format(clue.button_a)
    clue_data[11].text = "Button B: {}".format(clue.button_b)
    clue_data[12].text = "Touch 0: {}".format(clue.touch_0)
    clue_data[13].text = "Touch 1: {}".format(clue.touch_1)
    clue_data[14].text = "Touch 2: {}".format(clue.touch_2)
    clue_data.show()

    time.sleep(1)

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

