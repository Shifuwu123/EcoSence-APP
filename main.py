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
""" Text Fields con valores de los sensores """
# Reles
reles_values = {
    "fan": 0,
    "extrc": 0,
}

# Sensores
environment_values = {
    "temp": None,
    "humd": None,
    "tier": None,
}

# Text Fields con valores de los sensores
txf_temp_value = ft.TextField(
    value=f"{None} °C",
    label="Real",
    text_size=13,
    read_only=True,
    multiline=True,
    col=3,
    text_align=ft.TextAlign.CENTER,
)

txf_humd_value = ft.TextField(
    value=f"{None} %",
    label="Real",
    text_size=13,
    read_only=True,
    multiline=True,
    col=3,
    text_align=ft.TextAlign.CENTER,
)

txf_tier_value = ft.TextField(
    value=f"{None}",
    label="Real",
    text_size=13,
    read_only=True,
    multiline=True,
    col=3,
    text_align=ft.TextAlign.CENTER,
)

# TextFields de los Reles
txf_fan = ft.TextField(
    label="Ventilador",
    value="Encendido" if reles_values["fan"] else "Apagado",
    read_only=True,
    col=9,
    text_align=ft.TextAlign.CENTER,
)
txf_extrc = ft.TextField(
    label="Extractor",
    value="Encendido" if reles_values["extrc"] else "Apagado",
    read_only=True,
    col=9,
    text_align=ft.TextAlign.CENTER,
)

""" Filas de Contenedores de Sistema """
from config import cnts_stats_page
from config_test import cnt_params as parametros_values
from config_test import cnt_system as system_values

""" fr_row = ft.Row(
    controls=[
        cnts_stats_page("cultivo"),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    wrap=True,
    spacing=15,
    run_spacing=5,
    width=None,
)

sc_row = ft.Row(
    controls=[
        parametros_values(txf_temp_value, txf_humd_value, txf_tier_value),
        cnts_stats_page("estadísticas"),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    wrap=True,
    spacing=15,
    run_spacing=5,
    width=None,
) """

fr_row = ft.Row(
    controls=[
        parametros_values(txf_temp_value, txf_humd_value, txf_tier_value),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    wrap=True,
    spacing=15,
    run_spacing=5,
    width=None,
)
""" 
Fin Variables globales 
"""


################################################################################
# Paginas de la aplicación #############################################################################
def main(page: Page):
    def mqtt_connect(client):
        try:
            client.connect(broker)

        except Exception as e:
            logging.error(f"ERROR al conectar al broker MQTT: {e}")
            exit(1)

        # Suscribirse a todos los tópicos bajo 'EcoSense/esp32/'
        topic = "EcoSense/esp32/#"
        client.subscribe(topic)

        # Iniciar el loop de MQTT en segundo plano
        client.loop_start()
        msg = f"Conectado al broker MQTT al topic: {topic}"
        logging.info(msg)
        print(msg)
        return client

    # Función de callback cuando se recibe un mensaje
    def on_message(client, userdata, msg):
        mensaje = json.loads(msg.payload)
        topico = msg.topic
        
        logging.info(f"### Mensaje recibido en {topico}: {mensaje}")
        print(f"### Mensaje recibido en {topico}: {mensaje}")

        if topico == "EcoSense/esp32/sensores":
            try:
                environment_values['temp'] = float(mensaje["temp"])
                environment_values['humd'] = float(mensaje["humd"])
                environment_values['tier'] = float(mensaje["tier"])

                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                txf_tier_value.value = f"{environment_values['tier']} %"
                txf_tier_value.update()
                txf_temp_value.update()
                txf_humd_value.update()

                logging.info(f"# Sensores actualizados en la pagina")

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje '{e}' del topico '{topico}'")

        elif topico == "EcoSense/esp32/sensor/dht11":
            try:
                environment_values['temp'] = float(mensaje["temp"])
                environment_values['humd'] = float(mensaje["humd"])
                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                txf_temp_value.update()
                txf_humd_value.update()

                logging.info(f"# Sensor DHT-11 actualizado")

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje '{e}' del topico '{topico}'")

        elif topico == "EcoSense/esp32/sensor/hd38":
            try:
                environment_values['tier'] = float(mensaje["tier"])
                txf_tier_value.value = f"{environment_values['tier']} %"
                txf_tier_value.update()

                logging.info(f"# Sensor DHT-11 actualizado")

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje '{e}' del topico '{topico}'")

        elif topico == "EcoSense/esp32/reles":
            try:
                # Actualizamos diccionario de reles globales
                reles_values['fan'] = bool(mensaje["rele1"])
                reles_values['extrc'] = bool(mensaje["rele2"])

                # Actualizar los valores de la interfaz gráfica
                txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
                txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
                txf_fan.update()
                txf_extrc.update()

                # Registrar la actualización en el archivo de registro
                logging.info(f"# Reles actualizados")

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje '{e}' del topico '{topico}'")

        else:
            logging.warning(f"## Topico no registrado: {topico}")
            print(f"## Topico no registrado: {topico}")

    def toggle_fan(e):
        logging.info(f"## Rele de VENTILADOR alternado MANUALMENTE a: {reles_values['fan']}")
        reles_values["fan"] = not reles_values["fan"]
        txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"     
        txf_fan.update()
        client.publish("EcoSense/plc/rele1", json.dumps({"rele1": reles_values["fan"]}))
        logging.info(f"## Mensaje enviado a esp32: {json.dumps({'rele1': reles_values['fan']})}")

    def toggle_extrc(e):
        logging.info(f"## Rele de EXTRUSOR alternado MANUALMENTE a: {reles_values['extrc']}")
        reles_values['extrc'] = not reles_values['extrc']
        txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
        txf_extrc.update()
        client.publish("EcoSense/plc/rele2", json.dumps({"rele2": reles_values["extrc"]}))
        logging.info(f"## Mensaje enviado a esp32: {json.dumps({'rele2': reles_values['extrc']})}")

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
    page.theme = ft.Theme(color_scheme_seed="green")
    page.window_always_on_top = True

    ###############################################################
    # Variables globales de la pagina #############################################################################

    # Variables globales de Reles
    values = {"fan": txf_fan, "extrc": txf_extrc}
    btn_fan = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        col=3,
        on_click=toggle_fan,
    )
    btn_extrc = ft.IconButton(
        icon=ft.icons.MODE_FAN_OFF_ROUNDED,
        col=3,
        on_click=toggle_extrc,
    )
    btns = {"btn_fan": btn_fan, "btn_extrc": btn_extrc}

    # Configuración de la 1RA Fila
    fr_row.width = page.window_width
    fr_row.controls.append(system_values(btns, values))

    # Configuración de la 2DA Fila
    # sc_row.width = page.window_width

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
            controls=[
                fr_row,
                # sc_row,
            ],
            expand=1,
            spacing=10,
        ),
    )
    """ Fin Agregar datos a la pagina """


###############################################################################
# Lanzamiento de la aplicación ###############################################################################
ft.app(target=main)
