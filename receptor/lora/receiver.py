import machine
import time, urandom as random
from lora.lora import SX1276

id_red_local = "0000"


# Heltec WiFi LoRa 32 V2
LoRa_MISO_Pin = 19
LoRa_MOSI_Pin = 27
LoRa_SCK_Pin  =  5
LoRa_CS_Pin   = 18
LoRa_RST_Pin  = 14
LoRa_DIO0_Pin = 26
LoRa_DIO1_Pin = 35
LoRa_DIO2_Pin = 34
SPI_CH        =  1


channels2Hopping = [868_500_000] # Fijo para emisor y receptor

LoRa_id = 0

lora = SX1276(LoRa_RST_Pin, LoRa_CS_Pin, SPI_CH, LoRa_SCK_Pin, LoRa_MOSI_Pin, LoRa_MISO_Pin,
              LoRa_DIO0_Pin, LoRa_DIO1_Pin, LoRa_id, channels2Hopping, debug=False)
    

lora.brd_packet_handler = lambda self, data, SNR, RSSI: print(data)

lora.mode = 'RXCONTINUOUS'


paquete = None
lista_de_estaciones = []

# Cuando lora no esta recibiendo paquetes
while not lora.is_available:
    #print("waiting...")
    # Comprobamos que hay cambios en los datos, por lo que, un paquete nuevo ha entrado antes de dejar de recibir paquetes.
    if paquete != lora.datos:
        paquete = lora.datos

        #payload_ejemplo = "00001111locaSueca"
        payload = str(paquete[0])
        id_red_remoto = str(payload[2:6])
        id_estacion = str(payload[6:10])
        dato = str(payload[10:14])
        valor = str(payload[14:])
        snr = paquete[1]
        rssi = paquete[2]
        print("paquete correcto: ")
        print(" SNR: "+str(paquete[1])+"     RSSI: "+str(paquete[2]))

        # Comprobamos que el paquete entrante pertenece a la id de nuestra red
        pertenece_a_la_red = False
        if id_red_remoto == id_red_local:
            pertenece_a_la_red = True

        # Comprobamos si ya tenemos la estacion en la lista de estaciones
        existe = False
        for estacion in lista_de_estaciones:
            if id_estacion in estacion["id_estacion"]:
                # Si tenemos la id en alguna estacion de la lista de estaciones existe porque ya hemos recibido un paquete anteriormente
                existe = True 

        # Si no tenemos la estación, la creamos en la lista
        if pertenece_a_la_red and not existe:
            lista_de_estaciones.append({"id_estacion":id_estacion})
            existe = True # Se ha creado y por lo tanto ya existe

        # Le damos los valores que nos proporcionan los paquetes a los valores del diccionario
        if pertenece_a_la_red and existe:
            for estacion in lista_de_estaciones:
                if estacion["id_estacion"] == id_estacion:
                    if dato == "loca":
                        estacion["localidad"] = valor
                    if dato == "enti":
                        estacion["entidadMenor"] = valor
                    if dato == "part":
                        estacion["partida"] = valor
                    if dato == "nomb":
                        estacion["nombre"] = valor
                    if dato == "coor":
                        estacion["coordenadas"] = valor
                    if dato == "temp":
                        estacion["temperatura"] = valor
                    if dato == "hume":
                        estacion["humedad"] = valor
                    if dato == "prec":
                        estacion["precipitacion"] = valor
                    if dato == "vvel":
                        estacion["vientoVelocidad"] = valor
                    if dato == "vdir":
                        estacion["vientoDireccion"] = valor
                    if dato == "pres":
                        estacion["presion"] = valor

        # Comprobamos si alguna de las estaciones de la lista tiene todos los valores
        for estacion in lista_de_estaciones:
            #print(estacion)
            led = machine.Pin(12, machine.Pin.OUT)
            led.value(1)
            time.sleep(0.1)
            led.value(0)
            try:
                if estacion["localidad"] and estacion["entidadMenor"] and estacion["partida"] and estacion["nombre"] and estacion["coordenadas"] and estacion["temperatura"] and estacion["humedad"] and estacion["precipitacion"] and estacion["vientoVelocidad"] and estacion["vientoDireccion"] and estacion["presion"]:

                    # Si la tiene se manda fuera del módulo para ser consumido por otro modulo y se borra de aqui
                    print(estacion)
                    lista_de_estaciones.remove(estacion)
                    # Blink de led que confirma recepción de todos los paquetes de una estacion
                    led = machine.Pin(12, machine.Pin.OUT)
                    led.value(1)
                    time.sleep(1)
                    led.value(0)
            except KeyError: pass






    time.sleep(1)

