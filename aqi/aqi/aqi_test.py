""" unit test for Aqi class """
from aqi import Aqi

print ("Starting...")
my_aqi = Aqi()
for adjust in ("None", "LRAPA", "AQ+U"):
    for size in ("2.5", "10.0"):
        print ("Adjust: %s  Size: %s" % (adjust, size))
        for raw in range(0, 501, 5):
            aqi_value = my_aqi.sensor_to_aqi(raw, adjust, size)
            print ("Category: %s Raw: %d Adjusted: %d    AQI: %d" % \
                 (my_aqi.category, raw, my_aqi.adjusted_value, aqi_value))
