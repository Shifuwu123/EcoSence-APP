import paho.mqtt.client as mqtt
import json
import os
import csv
from datetime import datetime


# Función de callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    try:
        datos = json.loads(msg.payload)
        topico = msg.topic
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Crear el nombre del archivo según el tópico
        if topico == "sensor/DHT11":
            archivo = "datos_DHT11.csv"
            encabezado = ["Fecha", "Hora", "Temperatura", "Humedad"]
        elif topico == "sensor/HD38":
            archivo = "datos_HD38.csv"
            encabezado = ["Fecha", "Hora", "Humedad"]
        else:
            return

        # Escribir datos en el archivo CSV correspondiente
        escribir_csv(archivo, encabezado, timestamp, datos, topico)

        print(f"Datos recibidos y guardados en {archivo}: {datos}")

    except Exception as e:
        print(f"Error al recibir mensaje:{msg}")


# Función para escribir datos en CSV
def escribir_csv(archivo, encabezado, timestamp, datos, topico):
    if not os.path.isfile(archivo):
        with open(archivo, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(encabezado)

    with open(archivo, "a", newline="") as f:
        writer = csv.writer(f)
        if topico == "sensor/DHT11":
            writer.writerow(
                [
                    timestamp.split(" ")[0],
                    timestamp.split(" ")[1],
                    datos["temperatura"],
                    datos["humedad"],
                ]
            )
        elif topico == "sensor/HD38":
            writer.writerow(
                [
                    timestamp.split(" ")[0],
                    timestamp.split(" ")[1],
                    datos["humedad_tierra"],
                ]
            )


# Función para enviar comandos MQTT para controlar LEDs
def enviar_comando_led(topico, estado):
    mensaje = json.dumps({"estado": estado})
    client.publish(topico, mensaje)


# Función para el menú interactivo
def menu():
    while True:
        print("\nMenú de control de LEDs")
        print("1. Encender LED rojo")
        print("2. Apagar LED rojo")
        print("3. Encender LED amarillo")
        print("4. Apagar LED amarillo")
        print("5. Parpadear LED rojo")
        print("6. Parpadear LED amarillo")
        print("7. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            enviar_comando_led("control/led_rojo", 1)
        elif opcion == "2":
            enviar_comando_led("control/led_rojo", 0)
        elif opcion == "3":
            enviar_comando_led("control/led_amarillo", 1)
        elif opcion == "4":
            enviar_comando_led("control/led_amarillo", 0)
        elif opcion == "5":
            enviar_comando_led("control/parpadeo_led_rojo", 1)
        elif opcion == "6":
            enviar_comando_led("control/parpadeo_led_amarillo", 1)
        elif opcion == "7":
            print("Saliendo...")
            client.loop_stop()
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")


# Configuración del cliente MQTT
broker = "192.168.117.90"  # Dirección IP de tu computadora
client = mqtt.Client()

# Configuración de callbacks
client.on_message = on_message

try:
    client.connect(broker)
    print("Conectado al broker MQTT")
except Exception as e:
    print(f"ERROR al conectar al broker MQTT: {e}")
    exit(1)

# Suscribirse a todos los tópicos bajo 'sensor/'
client.subscribe("sensor/#")

# Iniciar el loop de MQTT en segundo plano
client.loop_start()

# Ejecutar el menú en el hilo principal
menu()
