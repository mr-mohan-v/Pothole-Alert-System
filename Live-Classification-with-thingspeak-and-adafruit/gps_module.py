import serial
import string
import re
import geocoder

def dmm_to_dd(dmm):
    degrees = int(dmm)
    minutes = (dmm - degrees) * 100
    decimal_degrees = degrees + minutes / 60
    return decimal_degrees

def get_gps():
    val = []
    while len(val)==0:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        newdata=ser.readline()
        newdata = str(newdata)
        result = re.compile("\d{4}\.\d{5}\,N\,\d{5}\.\d{5}\,E")
        val=result.findall(newdata)    
    lat = round(float(val[0][0:10])/100,6)
    lng = round(float(val[0][14:24])/100,6)
    lat = round(dmm_to_dd(lat),6) # Degrees and decimal minutes (DMM)
    lng = round(dmm_to_dd(lng),6) # Decimal degrees (DD)
    print(lat,lng)
    return lat,l











