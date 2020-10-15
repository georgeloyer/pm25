""" color tests with names and codes """
from aqi import Aqi

my_aqi = Aqi()

for code1 in my_aqi.all_color_codes():
    for code2 in my_aqi.all_color_codes():
        print("0x%08X   0x%08X" % (code1, code2))
