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
        self.pli_table = (
            ("Good", 0.0, 12.0, 0.0, 55.0, 0, 50,
                "Green", 0x00E400, 0, 228, 0),
            ("Moderate", 12.0, 35.5, 55.0, 155.0, 50, 100,
                "Yellow", 0xFFFF00, 255, 255, 0),
            ("Unhealthy for Sensitive Groups", 35.5, 55.5, 155.0, 255.0, 100, 150,
                "Orange", 0xFF7E00, 255, 126, 0),
            ("Unhealthy", 55.5, 150.5, 255.0, 355.0, 150, 200,
                "Red", 0xFF0000, 255, 0, 0),
            ("Very Unhealthy", 150.5, 250.5, 355.0, 425.0, 200, 300,
                "Purple", 0x8F3F97, 143, 63, 141),
            ("Hazardous", 250.5, 500.5, 425.0, 604.0, 300, 500,
                "Maroon", 0x7E0023, 126, 0, 35))
        self.pli_index = {
            "CATNAME" : 0,
            "PM25LO" : 1,
            "PM25HI" : 2,
            "PM10LO" : 3,
            "PM10HI" : 4,
            "AQILO" : 5,
            "AQIHI" : 6,
            "COLORNAME" : 7,
            "COLORCODE" : 8,
            "RCODE" : 9,
            "GCODE" : 10,
            "BCODE" : 11}

    def _get_list(self, key):
        ret_list = []
        for i in range(len(self.pli_table)):
            ret_list.append(self.pli_table[i][key])
        return ret_list

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
                if adjusted_raw < 0:
                    adjusted_raw = 0
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
            plo = self.pli_index["PM25LO"]
            phi = self.pli_index["PM25HI"]
        else:
            if size == "10.0":
                plo = self.pli_index["PM10LO"]
                phi = self.pli_index["PM10HI"]
            else:
                return "Error: size must be 2.5 or 10.0"

        # lookup adjusted_measure in pli_table and return upper/lower bounds
        # for measure and AQI by particle size
        category = 0
        for upper_bound in self._get_list(phi):
            if adjusted_raw >= upper_bound:
                category = category + 1
                continue
            aqi_category = category
            break
        measure_lo = self.pli_table[aqi_category][plo]
        measure_hi = self.pli_table[aqi_category][phi]
        aqi_lo = self.pli_table[aqi_category][self.pli_index["AQILO"]]
        aqi_hi = self.pli_table[aqi_category][self.pli_index["AQIHI"]]

        # update class variables with table entries for this aqi_category
        self.category = aqi_category
        self.colorname = self.pli_table[aqi_category][self.pli_index["COLORNAME"]]
        self.colorcode = self.pli_table[aqi_category][self.pli_index["COLORCODE"]]
        self.r_code = self.pli_table[aqi_category][self.pli_index["RCODE"]]
        self.g_code = self.pli_table[aqi_category][self.pli_index["GCODE"]]
        self.b_code = self.pli_table[aqi_category][self.pli_index["BCODE"]]

        # compute the linear interpolation between the bounds
        self.aqi_value = round((aqi_hi - aqi_lo)/(measure_hi - measure_lo) *\
            (adjusted_raw - measure_lo) + aqi_lo)

        return self.aqi_value

    def all_color_codes(self):
        """ test method: returns all color_codes for display testing """
        return self._get_list(self.pli_index["COLORCODE"])
