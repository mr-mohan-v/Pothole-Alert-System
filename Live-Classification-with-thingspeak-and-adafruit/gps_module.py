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
    #lat = round(float(val[0][0:10])/100,6)
    #lng = round(float(val[0][14:24])/100,6)
    lat = round(float(val[0][0:10])/100,6)
    lng = round(float(val[0][14:24])/100,6)
    lat = round(dmm_to_dd(lat),6) # Degrees and decimal minutes (DMM)
    lng = round(dmm_to_dd(lng),6) # Decimal degrees (DD)
    print(lat,lng)
    """
    #lat = lng = 0 
    #while lat == 0 and lng==0:
        #g = geocoder.ip('me')
        #lat , lng = g.latlng
    """    
    #return lat,lng 
    #return 10.9036700, 76.8986555
    #10.903786,76.898649 
    #return 10.903773, 76.898808
    #return 10.903737, 76.898492










