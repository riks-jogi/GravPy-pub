import requests, json
from numpy import sqrt, cos, sin, pi

#get this from https://developer.mapquest.com/
#This project only uses the free geocoding and elevation apis so credit card .etc not needed :)
API_KEY = ""

def geocode(location):
    """Takes an address and returns (lat, lon), for better results use "street number, city" for the query"""
    with requests.Session() as sess:
        resp = sess.get(f"http://open.mapquestapi.com/geocoding/v1/address?key={API_KEY}&location={location}&thumbMaps=false&maxResults=1")
    raw = resp.text
    presp = json.loads(raw)
    coords = (presp["results"][0]["locations"][0]["latLng"]["lat"], presp["results"][0]["locations"][0]["latLng"]["lng"])
    return coords

def elevation(coords):
    """Takes coordinates as a tuple and returns elevation as an int"""
    with requests.Session() as sess:
        resp = sess.get(f"http://open.mapquestapi.com/elevation/v1/profile?key={API_KEY}&shapeFormat=raw&latLngCollection={coords[0]},{coords[1]}")
    raw = resp.text
    presp = json.loads(raw)
    elev = presp["elevationProfile"][0]["height"]
    return elev

def gravity(lat, h):
    #Calculates the Gravitational forces based on latitude and elevation
    G = 6.67e-11 #Nm^2/kg^2 Gravitational constant.
    m = 5.972e+24 #kg Mass of the Earth.
    r_e = 6378.137 #km, Equatorial radius of the earth.
    r_p = 6356.752 #km, Polar radius of the earth.
    g_p=9.832 #g at the poles.
    g_45=9.806 #g at 45°.
    g_e=9.780 #g at the equator.
    #Calculates the Earth's radius at sea-level from the latitude.
    r0 = sqrt( ((r_e**2 * cos(lat))**2 + (r_p**2 * sin(lat))**2) / ( (r_e * cos(lat))**2 + (r_p * sin(lat))**2 ))
    g0 = g_45 - 1/2 * (g_p - g_e) * cos(2*lat*pi/180)
    g = (r0**2 * g0) / (r0**2 + 2*h*r0 + h**2)
    return g

#Combining and pretty print
def grav_from_address(address):
    lat_lng = geocode(address)
    h = elevation(lat_lng)
    grav = gravity(lat_lng[0], h)
    print(f"Gravitational forces at address: {address}\nat an elevation of {h} \nare {grav}")
