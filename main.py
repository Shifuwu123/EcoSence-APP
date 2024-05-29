# Librerías App
import flet as ft, typing as t
from flet import Page

# Librerías de MQTT
import paho.mqtt.client as mqtt
import json, time, logging, csv
from datetime import datetime

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
# Diccionario de los Reles
reles_values = {
    "fan": 0,
    "extrc": 0,
}

# Diccionario de los Sensores
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
    value='Unknown',
    read_only=True,
    col=9,
    text_align=ft.TextAlign.CENTER,
)
txf_extrc = ft.TextField(
    label="Extractor",
    value='Unknown',
    read_only=True,
    col=9,
    text_align=ft.TextAlign.CENTER,
)

""" Filas de Contenedores de Sistema """
from config_test import cnt_params as parametros_values
from config_test import cnt_system as system_values

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

toggle_row = ft.Row(
    alignment=ft.MainAxisAlignment.CENTER,
    wrap=True,
    spacing=15,
    run_spacing=5,
    width=None,
)


################################################################################
""" Funciones de Registro CSV"""
def registrar_dht11_csv():
    # Registrar valores del sensor DHT11
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("database/dht11_data.csv", mode='a', newline='') as archivo_dht11:
        escritor_dht11 = csv.writer(archivo_dht11)
        escritor_dht11.writerow([ahora, environment_values['temp'], environment_values['humd']])
        logging.info('Se ha registrado un nuevo valor en dht11_data.csv')

def registrar_hd38_csv():
    # Registrar valores del sensor HD38
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('hd38_data.csv', mode='a', newline='') as archivo_hd38:
        escritor_hd38 = csv.writer(archivo_hd38)
        escritor_hd38.writerow([ahora, environment_values['tier']])
        logging.info('Se ha registrado un nuevo valor en hd38_data.csv')

def registrar_sensores_csv():
    registrar_dht11_csv()
    registrar_hd38_csv()
    logging.info('Se han registrado todos los valores en archivos CSV')
    
################################################################################
# Paginas de la aplicación #############################################################################
def main(page: Page):
    ################################################################################
    # Funciones auxiliares
    def actualizar_app(e):
        client.publish("EcoSense/plc/actualizacion", json.dumps({"feedback": True}))
        logging.info(f"## Mensaje enviado a esp32: {json.dumps({'feedback': True})}")

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

    def toggle_reles(e):
        logging.info("## Reles alternados MANUALMENTE")
        reles_values['extrc'] = not reles_values['extrc']
        reles_values['fan'] = not reles_values['fan']
        txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
        txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
        txf_extrc.update()
        txf_fan.update()
        client.publish("EcoSense/plc/reles", json.dumps({"rele1": reles_values["fan"], "rele2": reles_values["extrc"]}))
        logging.info(f"## Mensaje enviado a esp32: {json.dumps({"rele1": reles_values["fan"], "rele2": reles_values["extrc"]})}")
    
    def off_reles(e):
        logging.info("## Reles apagados MANUALMENTE")
        reles_values['extrc'] = False
        reles_values['fan'] = False
        txf_extrc.value = "Apagado"
        txf_fan.value = "Apagado"
        txf_extrc.update()
        txf_fan.update()
        client.publish("EcoSense/plc/reles", json.dumps({"rele1": reles_values["fan"], "rele2": reles_values["extrc"]}))
        logging.info(f"## Mensaje enviado a esp32: {json.dumps({"rele1": reles_values["fan"], "rele2": reles_values["extrc"]})}")

    def on_reles(e):
        logging.info("## Reles encendidos MANUALMENTE")
        reles_values['extrc'] = True
        reles_values['fan'] = True
        txf_extrc.value = "Encendido"
        txf_fan.value = "Encendido"
        txf_extrc.update()
        txf_fan.update()
        client.publish("EcoSense/plc/reles", json.dumps({"rele1": reles_values["fan"], "rele2": reles_values["extrc"]}))
        logging.info(f"## Mensaje enviado a esp32: {json.dumps({"rele1": reles_values["fan"], "rele2": reles_values["extrc"]})}")

    ################################################################################
    # Funciones MQTT
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
        
    def on_message(client, userdata, msg):
        topico = msg.topic
        logging.info(f"### Mensaje recibido en {topico}: {msg.payload}")

        # Procesar el mensaje
        try:
            mensaje = json.loads(msg.payload)
        except Exception as e:
            logging.error(f"## Error al procesar el mensaje: {e}")
            exit(1)

        # Procesar el topico
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

                registrar_sensores_csv()

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
                
                registrar_dht11_csv()

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje '{e}' del topico '{topico}'")

        elif topico == "EcoSense/esp32/sensor/hd38":
            try:
                environment_values['tier'] = float(mensaje["tier"])
                txf_tier_value.value = f"{environment_values['tier']} %"
                txf_tier_value.update()
                
                registrar_hd38_csv()

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje '{e}' del topico '{topico}'")

        elif topico == "EcoSense/esp32/rele1":
            # Actualizamos diccionario de reles globales
            reles_values['fan'] = int(mensaje["rele1"])
            
            # Actualizar los valores de la interfaz gráfica
            txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
            txf_fan.update()

            # Registrar la actualización en el archivo de registro
            logging.info(f"# Rele1 actualizado")

        elif topico == "EcoSense/esp32/rele2":
            # Actualizamos diccionario de reles globales
            reles_values['extrc'] = int(mensaje["rele2"])

            # Actualizar los valores de la interfaz gráfica
            txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
            txf_extrc.update()

            # Registrar la actualización en el archivo de registro
            logging.info(f"# Rele2 actualizado")

        else:
            logging.warning(f"## Topico no registrado: {topico}")
            print(f"## Topico no registrado: {topico}")

    ###############################################################
    # Configuración del cliente MQTT ###############################################################################
    broker = "192.168.0.9"  # Dirección IP de tu computadora
    client = mqtt.Client()  # Crear un cliente MQTT
    client.on_message = on_message  # Configuración de callbacks
    mqtt_connect(client)  # Conectar al broker MQTT
    actualizar_app(None)  # Solicitar actualizaciones

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

    btn_toggle = ft.IconButton(
        icon=ft.icons.MODE_FAN_OFF_ROUNDED,
        col=3,
        on_click=toggle_reles,
    )
    btn_off = ft.IconButton(
        icon=ft.icons.POWER_OFF,
        col=3,
        on_click=off_reles,
    )
    btn_on = ft.IconButton(
        icon=ft.icons.POWER,
        col=3,
        on_click=on_reles,
    )
    
    btns = {"btn_fan": btn_fan, "btn_extrc": btn_extrc}

    # Configuración de la 1RA Fila
    fr_row.width = page.window_width
    fr_row.controls.append(system_values(btns, values))

    # Configuración de la 2DA Fila
    # sc_row.width = page.window_width

    # Configuración de la 3RA Fila
    toggle_row.width = page.window_width
    toggle_row.controls.append(btn_toggle)
    toggle_row.controls.append(btn_off)
    toggle_row.controls.append(btn_on)

    """ Fin Variables globales de la pagina """

    ###############################################################
    # Agregar datos a la pagina ############################################################################

    page.add(
        # Appbar de la pagina principal
        ft.AppBar(
            title=ft.Text("Estadísticas 🗃️"),
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.TEAL_ACCENT_400),
            actions=[
                ft.IconButton(
                    icon=ft.icons.ENERGY_SAVINGS_LEAF,
                    padding=15,
                    on_click=actualizar_app,
                ),
            ],
            ),
        # Vista de la pagina principal
        ft.ListView(
            controls=[
                fr_row,
                toggle_row,
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
