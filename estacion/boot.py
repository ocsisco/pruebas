from time import sleep
import json

with open("config/GENERAL.json") as f:
    config = json.load(f)


def selector_menu():
    """ Pulsador de programacion para que no entre en deepsleep.
        Cuando se envien archivos al ESP32, mantener pulsado en todo momento.
    """

    import machine

    led = machine.Pin(12, machine.Pin.OUT)
    led.value(0)

    pulsador = machine.Pin(33, machine.Pin.IN)
    estado_pulsador = pulsador.value()
    sleep(1)

    if estado_pulsador == True:
        while 1:
            led.value(1)
            sleep(0.1)
            led.value(0)
            sleep(0.1)
            print("Programming...")
            estado_pulsador = pulsador.value()
            if not estado_pulsador:
                captar_pulsaciones = True
                break
    if captar_pulsaciones:
        pass


def modo_servidor_web():

    import web.webserver as webserver
    print("iniciando")
    webserver.run_server()


selector_menu()

#modo_servidor_web()


