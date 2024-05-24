    
"""
Devices

"""

import sys
sys.path.append('sensores')

from time import sleep
import json
import machine


with open("config/GENERAL.json") as f:
    config = json.load(f)




"""
Definiendo clases de los sensores

"""

class Termometro():

    def __init__(self):

        import onewire
        from ds18x20 import DS18X20
        import binascii
  
        sensor = onewire.OneWire(machine.Pin(4))
        sensor = DS18X20(sensor)
        direcciones = sensor.scan()

        # adjudicamos valor por defecto.
        self.valor = None

        print("- Comprobando sensores de temperatura: ")
        valores = []
        for n in range(1): # Realiza n mediciones para mas fiabilidad si fuese necesario
            for idx in direcciones: # Recorre todos los sensores de temperatura y extrae el valor
                idHex = binascii.hexlify(bytearray(idx)) 
                idHex = (str(idHex))

                try: # Un sensor puede ser escaneado y luego perderse su señal en la lectura
                    sensor.convert_temp()
                    sleep(1)
                    valor = sensor.read_temp(idx)
                    print(idHex + ": " + str(valor) + "ºC ")
                    valores.append(valor)
                except:
                    print("Perdida de sensor durante la lectura: "+str(idHex))
        
        # si existen valores halla la media de ellos
        if valores:
            suma = 0
            for valor in valores:
                suma = suma + valor
            valor = suma/len(valores)
            self.valor = valor
        else:
            self.valor = None
            print("\nPerdida de sensor/es de temperatura")

        print("----------------------")


class Higrometro():

    def __init__(self):

        import machine
        import BME280

        # Pin assignment
        i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=10000)

        print("- Comprobando sensor de humedad: ")
        try:
            bme = BME280.BME280(i2c=i2c)
            temp = bme.temperature
            hum = bme.humidity
            hum = hum.replace("%","")
            hum = float(hum)
            pres = bme.pressure
            #print('Temperature: ', temp)
            print('Humedad: ', hum)
            #print('Pressure: ', pres)
            self.valor = hum
        except:
            self.valor = None
            print("\nPerdida de sensor de humedad")

        print("----------------------")
        

class Barometro():

    def __init__(self):


        import BME280
        # Pin assignment
        i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=10000)

        print("- Comprobando sensor de presión: ")
        try:
            bme = BME280.BME280(i2c=i2c)
            temp = bme.temperature
            hum = bme.humidity
            pres = bme.pressure
            pres = pres.replace("hPa","")
            pres = float(pres)
            #print('Temperature: ', temp)
            #print('Humidity: ', hum)
            print('Presión: ', pres)
            self.valor = pres
        except:
            self.valor = None
            print("\nPerdida de sensor de presión")
        
        print("----------------------")


class Pluviometro():

    def __init__(self):


        self.valor = 0

        # Lee el archivo de configuracion
        filename = 'config/pluviometro.json'
        with open(filename, "r") as file:
            data_pluvio = json.load(file)

        # Establece los valores necesarios
        lectura_anterior = data_pluvio["ultima lectura del peso del pluviometro"]
        pluviometro_vacio = data_pluvio["peso del pluviometro vacio"]
        pluviometro_lleno = data_pluvio["peso del pluviometro lleno"]

        """   # Pruebas con potenciometro
        #### POTENCIOMETRO ####
        if not modo_de_desarrollo:
            pin35 = machine.Pin(35)
            adc = machine.ADC(pin35)
            adc.atten(machine.ADC.ATTN_6DB)
            lectura_actual = adc.read()  
        sleep(1)#quitar en produccion
        #######################
        
        #### Pruebas con numeros aleatorios ####
        if modo_de_desarrollo:
            sleep(1)
            import random
            lectura_actual = round(random.random()*2000)
        #######################
        """

        #si la diferencia es mas negativa que valor histeresis
        if lectura_actual < (pluviometro_vacio +10) and lectura_anterior > 500:
            acumulado_actualizacion = (pluviometro_lleno-lectura_anterior)+(lectura_actual-pluviometro_vacio)
            sleep(3) #por si la primera lectura fuese en proceso de vaciado, esperar y tomar una segunda.
            lectura_actual = adc.read()

            data_pluvio["ultima lectura del peso del pluviometro"] = lectura_actual
            # 3. Write json file
            with open(filename, "w") as file:
                json.dump(data_pluvio, file)
            print("vaciado del pluvio")
            print("acumulado despues de vaciado" + str(acumulado_actualizacion))
            self.valor = acumulado_actualizacion

        else:
            acumulado_actualizacion = lectura_actual-lectura_anterior
            if acumulado_actualizacion > 20:
                data_pluvio["ultima lectura del peso del pluviometro"] = lectura_actual
                # 3. Write json file
                with open(filename, "w") as file:
                    json.dump(data_pluvio, file)

                print("acumulado actualizacion" + str(acumulado_actualizacion))

                self.valor = acumulado_actualizacion
        
            #si la diferencia es positiva, la diferencia es el acumulado
            #aplicar escalado segun diametro boca
        if self.valor < 0:
            self.valor = 0

        print("- Comprobando sensor de pluviometro: ")
        print("Nivel mínimo del pluviometro: " +str(pluviometro_vacio))
        print("Nivel del pluviometro: " +str(lectura_actual))
        print("Nivel del pluviometro lleno: " + str(pluviometro_lleno))
        print("Precipitación acumulada desde la ultima actualización: " +str(self.valor))
        print("----------------------")


    def calibrar(self):
        #leer el peso en vacio y aplicar minimo
        #leer en bucle el peso e ir sobreescribiendo el maximo
        #cuando vuelve a leer valor cerca del minimo para calibracion y led confirmacion blink
        pass

##########################################################################################################################################################
##########################################################################################################################################################


class Estacion():

    def __init__(self):

        self.localidad =        config["nombre de la estacion"]["nombre de la localidad"]
        self.entidadMenor =     config["nombre de la estacion"]["nombre de la entidad menor"]
        self.partida =          config["nombre de la estacion"]["nombre de la partida"]
        self.nombre =           config["nombre de la estacion"]["nombre de la estacion"]
        latitud =               config["nombre de la estacion"]["coordenadas de la ubicacion en grados decimales"]["latitud"]
        longitud =              config["nombre de la estacion"]["coordenadas de la ubicacion en grados decimales"]["longitud"]
        self.coordenadas =      latitud,longitud
        self.ID =               config["id estacion"]
        self.ID_RED =           config["id red"]
        self.temperatura =      config["sensores disponibles"]["termometro"]
        self.humedad =          config["sensores disponibles"]["higrometro"]
        self.precipitacion =    config["sensores disponibles"]["pluviometro"]
        self.vientoVelocidad =  config["sensores disponibles"]["anemometro"]
        self.vientoDireccion =  config["sensores disponibles"]["veleta"]
        self.presion =          config["sensores disponibles"]["barometro"]
        self.frecuencia =       config["frecuencia de envio de datos en segundos"]


    def leer_sensores(self):

        # Sensor de temperatura
        if self.temperatura == True:
            termometro = Termometro()
            self.temperatura = termometro.valor
        else: self.temperatura = None

        # Sensor de humedad
        if self.humedad == True:
            higrometro = Higrometro()
            self.humedad = higrometro.valor


        # Sensor de velocidad del viento
        if self.vientoVelocidad:
            print("anemometro")
            pass

        # Sensor dirección del viento
        if self.vientoDireccion:
            print("veleta")
            pass

        # Sensor pluviometro
        if self.precipitacion:
            pluviometro = Pluviometro()
            self.precipitacion = pluviometro.valor
            pass
        
        # Sensor pluviometro
        if self.presion:
            barometro = Barometro()
            self.presion = barometro.valor
            pass


