import json





def web_page():

    with open("config/GENERAL.json") as f:
        config = json.load(f)


    html = """
    <p>&nbsp;</p>
    <h3 style="text-align: center; color: #3f7320;"><span style="border-bottom: 4px solid #c82828;">AVAMET Xarxa LoRa</span></h3>
    <p><span style="border-bottom: 4px solid #c82828;"></span></p>
    <p style="text-align: center;"><strong><span style="border-bottom: 4px solid #c82828;">UBICACION:</span></strong></p>
    <!-- Este comentario es visible solo en el editor fuente -->
    <p><strong>Nombre de la localidad = """+str(config["nombre de la estacion"]["nombre de la localidad"])+"""<br /></strong></p>
    <p><strong>Nombre de la entidad menor = """+str(config["nombre de la estacion"]["nombre de la entidad menor"])+"""</strong></p>
    <p><strong>Nombre de la partida = """+str(config["nombre de la estacion"]["nombre de la partida"])+"""<br /></strong></p>
    <p><strong>Nombre de la estacion = """+str(config["nombre de la estacion"]["nombre de la estacion"])+"""</strong></p>
    <p><strong>Ubicacion de la estacion = """+str(config["nombre de la estacion"]["coordenadas de la ubicacion en grados decimales"]["latitud"])+""","""+str(config["nombre de la estacion"]["coordenadas de la ubicacion en grados decimales"]["longitud"])+"""</strong></p>
    <p><strong><span style="border-bottom: 4px solid #c82828;"></span></strong></p>
    <p style="text-align: center;"><strong><span style="border-bottom: 4px solid #c82828;">IDENTIFICACION:</span></strong></p>
    <p><strong>Id de la estacion = """+str(config["id estacion"])+"""<br /></strong></p>
    <p><strong>Id de la red = """+str(config["id red"])+"""</strong></p>
    <p><strong>Password de la red = """+str(config["password de red"])+"""</strong></p>
    <p><strong><span style="border-bottom: 4px solid #c82828;"></span></strong></p>
    <p style="text-align: center;"><strong><span style="border-bottom: 4px solid #c82828;">SENSORES DISPONIBLES:</span></strong></p>
    <p><strong>Termometro = """+str(config["sensores disponibles"]["termometro"])+"""</strong></p>
    <p><strong>Higrometro = """+str(config["sensores disponibles"]["higrometro"])+"""</strong></p>
    <p><strong>Pluviometro = """+str(config["sensores disponibles"]["pluviometro"])+"""</strong></p>
    <p><strong>Anemometro = """+str(config["sensores disponibles"]["anemometro"])+"""</strong></p>
    <p><strong>Veleta = """+str(config["sensores disponibles"]["veleta"])+"""</strong></p>
    <p><strong>Barometro = """+str(config["sensores disponibles"]["barometro"])+"""</strong></p>
    <p><strong>Periodo entre actualizaciones = """+str(config["frecuencia de envio de datos en segundos"])+"""</strong></p>
    <p><strong>Modo de desarrollo = """+str(config["modo de desarrollo"])+"""<br /></strong></p>
    <p><strong>&nbsp;</strong></p>
    <p></p>
    <p></p>
    """

    return html


def run_server():

    import socket

    import network

    import esp
    esp.osdebug(None)

    import gc
    gc.collect()



    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="MXO", password="1234")

    while ap.active() == False:
        pass

    print('Connection successful')
    print(ap.ifconfig())


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
        response = web_page()
        conn.send(response)
        conn.close()