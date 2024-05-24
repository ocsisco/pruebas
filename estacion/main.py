print("")
print("")
print("   █████████  █████   █████ █████████  ██████   ████████████████ ███████████                    ")
print("  ███░░░░░███░░███   ░░███ ███░░░░░███░░██████ ██████░░███░░░░░█░█░░░███░░░█                    ")
print(" ░███    ░███ ░███    ░███░███    ░███ ░███░█████░███ ░███  █ ░ ░   ░███  ░                     ")
print(" ░███████████ ░███    ░███░███████████ ░███░░███ ░███ ░██████       ░███                        ")
print(" ░███░░░░░███ ░░███   ███ ░███░░░░░███ ░███ ░░░  ░███ ░███░░█       ░███                        ")
print(" ░███    ░███  ░░░█████░  ░███    ░███ ░███      ░███ ░███ ░   █    ░███                        ")
print(" █████   █████   ░░███    █████   ██████████     ██████████████████ █████                       ")
print("░░░░░   ░░░░░     ░░░    ░░░░░   ░░░░░░░░░░     ░░░░░░░░░░░░░░░░███░░░░░                        ")
print(" █████ █████  ██████  ████████  █████ █████  ██████            ░███   ██████  ████████  ██████  ")
print("░░███ ░░███  ░░░░░███░░███░░███░░███ ░░███  ░░░░░███ ██████████░███  ███░░███░░███░░███░░░░░███ ")
print(" ░░░█████░    ███████ ░███ ░░░  ░░░█████░    ███████░░░░░░░░░░ ░███ ░███ ░███ ░███ ░░░  ███████ ")
print("  ███░░░███  ███░░███ ░███       ███░░░███  ███░░███           ░███ ░███ ░███ ░███     ███░░███ ")
print(" █████ █████░░█████████████     █████ █████░░████████          █████░░██████  █████   ░░████████")
print("░░░░░ ░░░░░  ░░░░░░░░░░░░░     ░░░░░ ░░░░░  ░░░░░░░░          ░░░░░  ░░░░░░  ░░░░░     ░░░░░░░░ ")
print("")
print("")
#########################################################################################################


"""
Librerias

"""

from time import sleep
import json
import machine
from classes.estacion import Estacion
from lora.sender import enviar_datos

# Extrae las configuraciones del json
with open("config/GENERAL.json") as f:
    config = json.load(f)


###############################################################
"""
Programa

"""


while 1:


    led = machine.Pin(12, machine.Pin.OUT)
    led.value(1)

    print("")
    print("----------------------")

    estacion = Estacion()

    estacion.leer_sensores()

    print("")
    print("Localidad: " + str(estacion.localidad) + "  -Id estacion: " + str(estacion.ID) + "  -Id red: " + str(estacion.ID_RED))
    print("Entidad menor: " + str(estacion.entidadMenor))
    print("Partida: " + str(estacion.partida))
    print("Nombre: " + str(estacion.nombre))
    print(estacion.coordenadas)
    print(str(estacion.temperatura)+ "ºC  " +str(estacion.humedad)+ "%  " +str(estacion.vientoVelocidad) + "km/h  " +str(estacion.vientoDireccion) + "º  " +str(estacion.precipitacion) + "mm  " + str(estacion.presion) + "hpa ")
    print("")


    enviar_datos(estacion.ID_RED,estacion.ID,"loca",estacion.localidad)
    enviar_datos(estacion.ID_RED,estacion.ID,"enti",estacion.entidadMenor)
    enviar_datos(estacion.ID_RED,estacion.ID,"part",estacion.partida)
    enviar_datos(estacion.ID_RED,estacion.ID,"nomb",estacion.nombre)
    enviar_datos(estacion.ID_RED,estacion.ID,"coor",estacion.coordenadas)
    enviar_datos(estacion.ID_RED,estacion.ID,"temp",estacion.temperatura)
    enviar_datos(estacion.ID_RED,estacion.ID,"hume",estacion.humedad)
    enviar_datos(estacion.ID_RED,estacion.ID,"prec",estacion.precipitacion)
    enviar_datos(estacion.ID_RED,estacion.ID,"vvel",estacion.vientoVelocidad)
    enviar_datos(estacion.ID_RED,estacion.ID,"vdir",estacion.vientoDireccion)
    enviar_datos(estacion.ID_RED,estacion.ID,"pres",estacion.presion)

    led.value(0)
    
    #########################

    if 1:
        machine.deepsleep((estacion.frecuencia)*1000)
    else:
        sleep(6)
