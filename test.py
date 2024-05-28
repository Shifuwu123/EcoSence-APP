# Librerías App
import flet as ft, typing as t
from flet import Page

# Librerías de MQTT
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import logging

# Configuración del logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="log/app.log",
    filemode="a",
)

################################################################################
# Variables globales APP ###############################################################################
crop_environment = {
    "temp": None,
    "humd": None,
    "tier": None,
    "lgt_qlty": None,
    "fan": None,
    "extrc": None,
    "wtr": None,
    "lgt": None,
}

""" Fin Variables globales """


################################################################################
# Paginas de la aplicación #############################################################################
from config_test import cnt_params as parametros_values
from config import cnts_stats_page

def main(page: Page):
    def mqtt_connect(client):
        try:
            client.connect(broker)
            logging.info("Conectado al broker MQTT")
            print("### Conectado al broker MQTT")
        except Exception as e:
            logging.error(f"ERROR al conectar al broker MQTT: {e}")
            exit(1)

        # Suscribirse a todos los tópicos bajo 'sensor/'
        client.subscribe("EcoSense/sensor/#")

        # Iniciar el loop de MQTT en segundo plano
        client.loop_start()
        return client

    # Función de callback cuando se recibe un mensaje
    def on_message(client, userdata, msg):
        mensaje = json.loads(msg.payload)
        topico = msg.topic
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        logging.info(
            f"### Mensaje recibido: {mensaje}\n### Tópico: {topico}\n### Fecha: {timestamp}"
        )

        if topico == "EcoSense/sensor/DHT11":
            try:
                value = {
                    "temp": float(mensaje["temp"]),
                    "humd": float(mensaje["humd"]),
                }

                # Actualizar los valores de la interfaz gráfica
                txf_temp_value.value = f"{value['temp']} °C"
                txf_humd_value.value = f"{value['humd']} %"
                page.update()
                logging.info(f"# Pagina actualizada")
                print(f"# Pagina actualizada")

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje: {e}")

        elif topico == "EcoSense/sensor/HD38":
            try:
                txf_tier_value.value = f"{float(mensaje['tier'])}"

                page.update()
                logging.info(f"# Pagina actualizada")
                print(f"# Pagina actualizada")

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje: {e}")

        else:
            logging.warning(f"## Topico no registrado: {topico}")
            print(f"## Topico no registrado: {topico}")

    ###############################################################
    # Configuración del cliente MQTT ###############################################################################
    broker = "192.168.137.1"  # Dirección IP de tu computadora
    client = mqtt.Client()  # Crear un cliente MQTT
    client.on_message = on_message  # Configuración de callbacks
    mqtt_connect(client)  # Conectar al broker MQTT
    """ Fin Conexión MQTT """

    ###############################################################
    # Aspectos generales de la pagina ###############################################################################
    page.title = "EcoSense"
    page.adaptive = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_min_width = 720
    page.window_width = 720
    page.theme = ft.Theme(color_scheme_seed="green")
    page.window_always_on_top = True

    ###############################################################
    # Variables globales de la pagina #############################################################################
    txf_temp_value = ft.TextField(
        value=f"{crop_environment['temp']} °C",
        label="Real",
        text_size=13,
        read_only=True,
        multiline=True,
        col=3,
        text_align=ft.TextAlign.CENTER,
    )

    txf_humd_value = ft.TextField(
        value=f"{crop_environment['humd']} %",
        label="Real",
        text_size=13,
        read_only=True,
        multiline=True,
        col=3,
        text_align=ft.TextAlign.CENTER,
    )

    txf_tier_value = ft.TextField(
        value=f"{crop_environment['tier']}",
        label="Real",
        text_size=13,
        read_only=True,
        multiline=True,
        col=3,
        text_align=ft.TextAlign.CENTER,
    )
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
            parametros_values(txf_temp_value, txf_humd_value, txf_tier_value),
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

    """ Fin Variables globales de la pagina """

    ###############################################################
    # Agregar datos a la pagina ############################################################################
    

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
# Lanzamiento de la aplicación ###############################################################################
ft.app(target=main)
