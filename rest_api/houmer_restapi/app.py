from flask import Flask, jsonify, request

app = Flask(__name__)

from houmers import houmers
from ubicacion import obtenerUbicacion
from ubicacion import Propiedad

@app.route('/test')
def test():
    return jsonify({"mensaje": "test"})
    
@app.route('/eventos')
def getEventos():
    #return jsonify(houmers)
    return jsonify({'eventos': houmers})

@app.route('/eventos/<string:houmer_name>')
def getEvento(houmer_name):
    print(houmer_name)
    existe = [houmer for houmer in houmers if houmer['houmer'].lower() == houmer_name]
    if (len(existe)>0):
        return jsonify(existe[0])
    else:
        return jsonify({'Mensaje':'Houmer no encontrado'})
    
@app.route('/addTraslado', methods=['POST'])
def addTraslado():
    print(request.json)
    n_evento = {
        "propiedad":request.json['propiedad'], 
        "houmer":request.json['houmer'], 
        "operacion":request.json['operacion'], 
        "coor_houmer":request.json['coor_houmer'],     
        "fecha":request.json['fecha'], 
        "tiempo":request.json['tiempo']} 
    houmers.append(n_evento)
    return jsonify({"Mensaje": "evento agregado satisfactoriamente!", "evento": n_evento})

@app.route('/addInspeccion', methods=['POST'])
def addInspeccion():
    print(request.json)
    n_evento = {
        "propiedad":request.json['propiedad'], 
        "houmer":request.json['houmer'], 
        "operacion":request.json['operacion'], 
        "coor_propiedad":request.json['coor_propiedad'], 
        "fecha":request.json['fecha'], 
        "tiempo":request.json['tiempo']} 
    houmers.append(n_evento)
    return jsonify({"Mensaje": "evento agregado satisfactoriamente!", "inspeccion": n_evento})


@app.route('/propiedad/<string:houmer_name>')
def getPropiedades(houmer_name):
    print(houmer_name)
    existe = [houmer for houmer in houmers if houmer['houmer'].lower() == houmer_name]
    if(len(existe)<=0):
        return jsonify({'Mensaje':'Houmer no encontrado'})
    propiedades = []
    for houm in existe:
        print(houm)        
        prop = ""
        for p in propiedades:
            if p.operacion == 'inspeccion' and houm['propiedad'].lower() == p.nombre:
                prop = p;  
        if houm['operacion'] == 'ini traslado' or houm['operacion'] == 'fin traslado': 
             print('Es un traslado')
        else:        
            if prop == "":
                prop =  Propiedad(houm['propiedad'], 'inspeccion', houm['coor_propiedad'], houm['coor_propiedad'], 
                    houm['houmer'], houm['fecha'], houm['tiempo'], '00:00') 
                propiedades.append(prop)
            else:                
                print(houm['propiedad'])
                prop.hora_fin = houm['tiempo']            
    respuesta = []
    for prop in propiedades:
        print(prop.hora_ini+" - "+ prop.hora_fin+" " + prop.getTiempo())
        respuesta.append(prop.houmer + " visitó un "+ prop.nombre + ", el día: "+ prop.fecha +", tardó " +prop.getTiempo())
    return jsonify(respuesta)
    
@app.route('/traslados/<string:houmer_name>')
def getTraslados(houmer_name):
    print(houmer_name)
    existe = [houmer for houmer in houmers if houmer['houmer'].lower() == houmer_name]
    if(len(existe)<=0):
        return jsonify({'Mensaje':'Houmer no encontrado'})
    traslados = []
    for houm in existe:
        #print(houm)        
        trasl = ""
        for p in traslados:
            print(p.operacion +"-"+ p.nombre)
            print(houm)
            if p.operacion == 'traslado' and houm['propiedad'].lower() == p.nombre:
                trasl = p;  
        if houm['operacion'] == 'ini inspeccion' or houm['operacion'] == 'fin inspeccion': 
             print('Es una propiedad')
        else:   
            print(trasl)  
            if trasl == "":
                trasl =  Propiedad( houm['propiedad'], 'traslado', houm['coor_houmer'], '', houm['houmer'], houm['fecha'], houm['tiempo'], '00:00') 
                traslados.append(trasl)
            else:                
                print(houm['propiedad'])
                trasl.hora_fin = houm['tiempo']    
                trasl.coord_fin = houm['coor_houmer']    
    respuesta = []
    for trasl in traslados:
        print(trasl.hora_ini+" - "+ trasl.hora_fin+" " + trasl.getTiempo())
        respuesta.append(trasl.houmer + " se trasladó "+ trasl.nombre + ", el día: "+ trasl.fecha +", tardó " 
            +trasl.getTiempo() + ", distancia: "+trasl.getDistancia() + " klm")
    return jsonify(respuesta)
 
@app.route('/prueba')
def prueba():    
    punto = obtenerUbicacion("42.59944444, -5.56666667");
    return jsonify({"Punto:":punto})
    
if __name__ == '__main__':
    app.run(debug=True, port=5100)



        