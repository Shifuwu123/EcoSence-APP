# Librerías App
import flet as ft
from flet import Page

from data import *
from config import *

# Librerías de MQTT
import paho.mqtt.client as mqtt
import json, os, csv
from datetime import datetime

################################################################################
""" Funciones MQTT"""
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


###############################################################################
""" Variables globales MQTT"""
# Configuración del cliente MQTT
broker = "192.168.117.90"  # Dirección IP de tu computadora
client = mqtt.Client()

# Configuración de callbacks
client.on_message = on_message

"""Variables globales APP"""
# Appbar de la pagina principal
appbar_main = ft.AppBar(
    title=ft.Text("Estadísticas 🗃️"),
    actions=[ft.IconButton(icon=ft.icons.ENERGY_SAVINGS_LEAF, padding=15)],
    bgcolor=ft.colors.with_opacity(0.04, ft.colors.TEAL_ACCENT_400),
)

filas = ft.Row(
    alignment=ft.MainAxisAlignment.SPACE_AROUND,
    # Hacer la pagina responsiva
    wrap=True,
    spacing=10,
    run_spacing=10,
)

""" Fin Variables globales """
###############################################################################
""" Paginas de la aplicación """


def main(page: Page):
    ###############################################################
    """Aspectos generales de la pagina"""
    page.title = "EcoSense"
    page.adaptive = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_min_width = 720
    page.window_width = 720
    page.theme = ft.Theme(color_scheme_seed="green")
    page.window_always_on_top = True

    """ Fin aspectos generales de la pagina """
    """
    
    """
    ###############################################################
    """ Agregar datos a la pagina """
    page.add(
        appbar_main,  # Appbar de la pagina
        ft.ListView(
            controls=[
                # 1ra fila
                ft.Row(
                    controls=[
                        cnts_stats_page("cultivo"),
                        cnts_stats_page("sistema"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    # Hacer la pagina responsiva
                    wrap=True,
                    spacing=15,
                    run_spacing=5,
                    width=page.window_width,
                ),
                # 2da Fila
                ft.Row(
                    controls=[
                        cnts_stats_page("parámetros"),
                        cnts_stats_page("estadísticas"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    # Hacer la pagina responsiva
                    wrap=True,
                    spacing=15,
                    run_spacing=5,
                    width=page.window_width,
                ),
            ],
            expand=1,
            spacing=10,
        ),
    )
    """ Fin Agregar datos a la pagina """

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

ft.app(target=main)
