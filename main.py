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
        if topico == "EcoSense/sensor":
            global current
            print(current)
            current["temperatura"] = datos
            print(f"Datos recibidos: {datos}")
            print(current)

        elif topico == "EcoSense/sensor/DHT11":
            archivo = "datos_DHT11.csv"
            encabezado = ["Fecha", "Hora", "Temperatura", "Humedad"]
            escribir_csv(archivo, encabezado, timestamp, datos, topico)

        elif topico == "EcoSense/sensor/HD38":
            archivo = "datos_HD38.csv"
            encabezado = ["Fecha", "Hora", "Humedad"]
            escribir_csv(archivo, encabezado, timestamp, datos, topico)

        else:
            print(f"Tópico no registrado: {topico}")
            return

        # Actualizar la interfaz gráfica
        actualizar_interfaz()

    except Exception as e:
        print(f"ERROR al recibir mensaje: {e}")


# Función para escribir datos en CSV
def escribir_csv(archivo, encabezado, timestamp, datos, topico):
    if not os.path.isfile(archivo):
        with open(archivo, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(encabezado)

    with open(archivo, "a", newline="") as f:
        writer = csv.writer(f)
        if topico == "EcoSense/sensor/DHT11":
            writer.writerow(
                [
                    timestamp.split(" ")[0],
                    timestamp.split(" ")[1],
                    datos.get("temperatura", "N/A"),
                    datos.get("humedad", "N/A"),
                ]
            )
        elif topico == "EcoSense/sensor/HD38":
            writer.writerow(
                [
                    timestamp.split(" ")[0],
                    timestamp.split(" ")[1],
                    datos.get("humedad", "N/A"),
                ]
            )


# Función para enviar comandos MQTT para controlar LEDs
def enviar_comando_led(topico, estado):
    mensaje = json.dumps({"estado": estado})
    client.publish(topico, mensaje)


# Función para actualizar la interfaz gráfica
def actualizar_interfaz():
    # Aquí puedes actualizar la interfaz gráfica con los nuevos datos de `current`
    pass


###############################################################################
""" Variables globales MQTT"""
# Configuración del cliente MQTT
broker = "10.6.20.236"  # Dirección IP de tu computadora
client = mqtt.Client()

# Configuración de callbacks
client.on_message = on_message

"""Variables globales APP"""

# Variables de los sensores
current = {
    "temperatura": None,
    "humedad": None,
    "tierra": None,
    "luz": None,
}



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

    """Aspectos generales de las filas"""
    # 1ra fila
    fr_row = ft.Row(
        controls=[
            cnts_stats_page("cultivo"),
            cnts_stats_page("sistema"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        # Hacer la pagina responsiva
        wrap=True,
        spacing=15,
        run_spacing=5,
        width=None,
    )

    # 2da Fila
    sc_row = ft.Row(
        controls=[
            cnts_stats_page("parámetros", current=current),
            cnts_stats_page("estadísticas"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        # Hacer la pagina responsiva
        wrap=True,
        spacing=15,
        run_spacing=5,
        width=None,
    )

    fr_row.width = page.window_width
    sc_row.width = page.window_width

    ###############################################################
    """ Agregar datos a la pagina """
    page.add(
        # Appbar de la pagina principal
        ft.AppBar(
            title=ft.Text("Estadísticas 🗃️"),
            actions=[
                ft.IconButton(
                    icon=ft.icons.ENERGY_SAVINGS_LEAF,
                    padding=15,
                    on_click=page.update(),
                ),
            ],
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.TEAL_ACCENT_400),
        ),
        # Vista de la pagina principal
        ft.ListView(
            controls=[fr_row, sc_row],
            expand=1,
            spacing=10,
        ),
    )
    """ Fin Agregar datos a la pagina """


###############################################################################
""" Conexión MQTT """
try:
    client.connect(broker)
    print("Conectado al broker MQTT")
except Exception as e:
    print(f"ERROR al conectar al broker MQTT: {e}")
    exit(1)

# Suscribirse a todos los tópicos bajo 'sensor/'
client.subscribe("EcoSense/sensor/#")

# Iniciar el loop de MQTT en segundo plano
client.loop_start()

""" Lanzamiento de la aplicación """
ft.app(target=main)
