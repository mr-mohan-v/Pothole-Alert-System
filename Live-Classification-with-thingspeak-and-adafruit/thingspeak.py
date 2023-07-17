import http.client as httplib
import urllib
import threading, os, time

key =  # Thingspeak Write API Key

# This Function will upload Latitude and Longitude values to the Thingspeak channel
def upload_cloud(lat,lon):
        params = urllib.parse.urlencode({'field1': lat,'field2': lon, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept" : "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except:
            print("connection failed")

