import geopy.geocoders
from geopy.geocoders import Nominatim 
from json import JSONDecoder
from geopy import distance

import ssl
import certifi
import geopy.geocoders

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(user_agent="Houmer") 
location = geolocator.reverse("42.59944444, -5.56666667") 
print(location.point)

def obtenerUbicacion(coordenada):
    print(coordenada)
    location = geolocator.reverse(coordenada) 
    print(location.point)
    #return EmployeeEncoder().encode(location.point)
    return location.point.format()

# subclass JSONEncoder
class EmployeeEncoder(JSONDecoder):
    def default(self, o):
        return o.__dict__    


class Propiedad:
    def __init__(self, nombre, operacion, coord_ini, coord_fin, houmer, fecha, hora_ini, hora_fin):
        self.nombre = nombre
        self.operacion = operacion
        self.coord_ini = coord_ini
        self.coord_fin = coord_fin
        self.houmer  = houmer 
        self.fecha = fecha 
        self.hora_ini =  hora_ini
        self.hora_fin = hora_fin
        self.propiedades = []
    
    def getTiempo(self):
        tiempo = int(self.hora_fin.split(':')[0])*60 - int(self.hora_ini.split(':')[0])*60
        tiempo = tiempo + int(self.hora_fin.split(':')[1]) - int(self.hora_ini.split(':')[1])
        return str(tiempo);        

    def getDistancia(self):
        print(self.coord_ini + " - " + self.coord_fin)
        coord_ini = self.coord_ini
        coord_fin = self.coord_fin
        print(distance.distance(coord_ini, coord_fin).kilometers)
        print(self.coord_ini + " - " + self.coord_fin)
        return str(distance.distance(coord_ini, coord_fin).kilometers);
