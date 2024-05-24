
def enviar_datos(id_red,id_estacion,dato,valor):

    from machine import Pin
    import time, urandom as random
    from lora.lora import SX1276

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

    channels2Hopping = [868_500_000] # 914~916 MHz

    LoRa_id = 1
    lora = SX1276(LoRa_RST_Pin, LoRa_CS_Pin, SPI_CH, LoRa_SCK_Pin, LoRa_MOSI_Pin, LoRa_MISO_Pin,
                LoRa_DIO0_Pin, LoRa_DIO1_Pin, LoRa_id, channels2Hopping, debug=False)


    payload = str(id_red) + str(id_estacion) + str(dato) + str(valor)
    
    print('[Sending]', payload)
    lora.send(dst_id=3, msg=payload, pkt_type=lora.PKT_TYPE['BRD']) # A broadcast request. Do not expect respond.
    time.sleep(3)
