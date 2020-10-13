""" module AQI """
class Aqi:
    """ AQI class has data and methods for converting between AQI and raw/adjusted
        particle measurements. The AQI class contains a piecewise linear
        interpolation table as a lookup for converting raw readings from a
        Plantower particle size sensor in ug/m^3 to the EPA standard for
        Air Quality Index (AQI). """

    def __init__(self):
        """ creates the piecewise linear interpolation table if it doesn't exist
            returns an Aqi object for accessing the methods that use the table. """
        self.raw_value = 0
        self.adjusted_value = 0
        self.size = "NA"
        self.adjust = "NA"
        self.aqi_value = 0
        self.category = "NA"
        self.colorname = "NA"
        self.colorcode = 0x000000
        self.r_code = 0
        self.g_code = 0
        self.b_code = 0
        self.pli_table = {
                "Good" :
                    {"pm25lo" : 0.0,
                    "pm25hi" : 12.0,
                    "pm10lo" : 0.0,
                    "pm10hi" : 55.0,
                    "aqilo" : 0,
                    "aqihi" : 50,
                    "colorname" : "Green",
                    "colorcode" : 0x00E400,
                    "r" : 0,
                    "g" : 228,
                    "b" : 0},
                "Moderate" :
                    {"pm25lo" : 12.0,
                    "pm25hi" : 35.5,
                    "pm10lo" : 55.0,
                    "pm10hi" : 155.0,
                    "aqilo" : 50,
                    "aqihi" : 100,
                    "colorname" : "Yellow",
                    "colorcode" : 0xFFFF00,
                    "r" : 255,
                    "g" : 255,
                    "b" : 0},
                "Unhealthy for Sensitive Groups" :
                    {"pm25lo" : 35.5,
                    "pm25hi" : 55.5,
                    "pm10lo" : 155.0,
                    "pm10hi" : 255.0,
                    "aqilo" : 100,
                    "aqihi" : 150,
                    "colorname" : "Orange",
                    "colorcode" : 0xFF7E00,
                    "r" : 255,
                    "g" : 126,
                    "b" : 0},
                "Unhealthy" :
                    {"pm25lo" : 55.5,
                    "pm25hi" : 150.5,
                    "pm10lo" : 255.0,
                    "pm10hi" : 355.0,
                    "aqilo" : 150,
                    "aqihi" : 200,
                    "colorname" : "Red",
                    "colorcode" : 0xFF0000,
                    "r" : 255,
                    "g" : 0,
                    "b" : 0},
                "Very Unhealthy" :
                    {"pm25lo" : 150.5,
                    "pm25hi" : 250.5,
                    "pm10lo" : 355.0,
                    "pm10hi" : 425.0,
                    "aqilo" : 200,
                    "aqihi" : 300,
                    "colorname" : "Purple",
                    "colorcode" : 0x8F3F97,
                    "r" : 143,
                    "g" : 63,
                    "b" : 141},
                "Hazardous" :
                    {"pm25lo" : 250.5,
                    "pm25hi" : 500.5,
                    "pm10lo" : 425.0,
                    "pm10hi" : 604.0,
                    "aqilo" : 300,
                    "aqihi" : 500,
                    "colorname" : "Maroon",
                    "colorcode" : 0x7E0023,
                    "r" : 126,
                    "g" : 0,
                    "b" : 35},
                    }

    def sensor_to_aqi(self, raw, adjust, size):
        """ takes a raw measure in ug/m^3 from sensor and converts to EPA Air Quality Index (AQI)
            parameters:
            raw: integer
            adjust: None, LRAPA, AQ+U   The adjustments made to the raw measure before indexing.
            size: 2.5, 10.0             The particle sizes handled by this class.
            adjusts ug/m^3 raw measure. Uses the adjusted measure to look up piecewise boundaries
            for the measure and the corresponding AQI index, and uses the boundaries and the
            adjusted measure to interpolate the AQI that corresponds to the adjusted measure. """
        # check adjust parameter for valid values and exit if not valid
        if adjust not in ("None", "LRAPA", "AQ+U"):
            return "Error: Adjust %s is not None, LRAPA or AQ+U" % adjust

        # check size parameter for valid values and exit if not valid
        if size not in ("2.5", "10.0"):
            return "Error: Size %s is not 2.5 or 10.0" % size

        # if size is 10.0, ignore adjustment and continue convert
        # if size is 2.5, adjust raw to LRAPA or AQ+U via linear conversion
        adjusted_raw = raw
        if size == "2.5":
            if adjust == "LRAPA":
                adjusted_raw = round(0.5 * raw - 0.66)
            else:
                if adjust == "AQ+U":
                    adjusted_raw = round(0.77 * raw + 2.6)

        # keep the current raw and adjusted values in the class
        # and keep the input parameters
        self.raw_value = raw
        self.adjusted_value = adjusted_raw
        self.size = size
        self.adjust = adjust

        if size == "2.5":
            plo = "pm25lo"
            phi = "pm25hi"
        else:
            if size == "10.0":
                plo = "pm10lo"
                phi = "pm10hi"
            else:
                return "Error: size must be 2.5 or 10.0"

        # lookup adjusted_measure in pli_table and return upper/lower bounds
        # for measure and AQI by particle size
        for category in self.pli_table:
            if adjusted_raw >= self.pli_table[category][phi]:
                continue
            aqi_category = category
            break
        measure_lo = self.pli_table[aqi_category][plo]
        measure_hi = self.pli_table[aqi_category][phi]
        aqi_lo = self.pli_table[aqi_category]["aqilo"]
        aqi_hi = self.pli_table[aqi_category]["aqihi"]

        # update class variables with table entries for this aqi_category
        self.category = aqi_category
        self.colorname = self.pli_table[aqi_category]["colorname"]
        self.colorcode = self.pli_table[aqi_category]["colorcode"]
        self.r_code = self.pli_table[aqi_category]["r"]
        self.g_code = self.pli_table[aqi_category]["g"]
        self.b_code = self.pli_table[aqi_category]["b"]

        # compute the linear interpolation between the bounds
        self.aqi_value = round((aqi_hi - aqi_lo)/(measure_hi - measure_lo) *\
            (adjusted_raw - measure_lo) + aqi_lo)

        return self.aqi_value
