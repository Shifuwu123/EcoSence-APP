# Librerías App
import flet as ft
from flet import Page

# Librerías de MQTT
import paho.mqtt.client as mqtt
import json, logging, csv, time
from datetime import datetime

# Configuración del logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="registros/app.log",
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
from config import cnt_params as parametros_values
from config import cnt_system as system_values
from config import cnts_stats_page as cnt_old

fr_row = ft.Row(
    controls=[
        cnt_old(parametro="cultivo"),
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    wrap=True,
    spacing=15,
    run_spacing=5,
    width=None,
)

sc_row = ft.Row(
    controls = [
        parametros_values(txf_temp_value, txf_humd_value, txf_tier_value),
        cnt_old(parametro="estadísticas"),
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
    with open('database/hd38_data.csv', mode='a', newline='') as archivo_hd38:
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
        client.publish("EcoSense/plc/actualizacion", json.dumps({"feedback": True})),
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
        page.update()
        client.publish("EcoSense/plc/reles", json.dumps({"rele1": reles_values["fan"], "rele2": reles_values["extrc"]}))
        logging.info(f"## Mensaje enviado a esp32: {json.dumps({"rele1": reles_values["fan"], "rele2": reles_values["extrc"]})}")
    
    def off_reles(e):
        logging.info("## Reles apagados MANUALMENTE")
        reles_values['extrc'] = False
        reles_values['fan'] = False
        txf_extrc.value = "Apagado"
        txf_fan.value = "Apagado"
        page.update()
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
            return False

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

        # Si la aplicación esta en la pagina principal
        if page.route == "/esp32_online":
            try:
                # Procesar el mensaje
                mensaje = json.loads(msg.payload) 

            except Exception as e:
                logging.error(f"## Error al procesar el mensaje: {e}")
                return

            # Procesar el topico
            if topico == "EcoSense/esp32/sensores":
                environment_values['temp'] = float(mensaje["temp"])
                environment_values['humd'] = float(mensaje["humd"])
                environment_values['tier'] = float(mensaje["tier"])

                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                txf_tier_value.value = f"{environment_values['tier']}"
                page.update()

                registrar_sensores_csv()

            elif topico == "EcoSense/esp32/sensor/dht11":
                environment_values['temp'] = float(mensaje["temp"])
                environment_values['humd'] = float(mensaje["humd"])
                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                page.update()
                
                registrar_dht11_csv()

            elif topico == "EcoSense/esp32/sensor/hd38":
                environment_values['tier'] = float(mensaje["tier"])
                txf_tier_value.value = f"{environment_values['tier']}"
                page.update()
                
                registrar_hd38_csv()

            elif topico == "EcoSense/esp32/rele1":
                reles_values['fan'] = int(mensaje["rele1"])
                txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
                page.update()

                logging.info("# Rele1 actualizado")

            elif topico == "EcoSense/esp32/rele2":
                reles_values['extrc'] = int(mensaje["rele2"])
                txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
                page.update()

                logging.info("# Rele2 actualizado")

            elif topico == "EcoSense/esp32/feedback":
                environment_values['temp'] = float(mensaje["temp"])
                environment_values['humd'] = float(mensaje["humd"])
                environment_values['tier'] = float(mensaje["tier"])

                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                txf_tier_value.value = f"{environment_values['tier']}"

                reles_values['fan'] = int(mensaje["rele1"])
                txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
                btn_fan.tooltip = "Alternar VENTILADOR"
                btn_fan.on_click = toggle_fan

                reles_values['extrc'] = int(mensaje["rele2"])
                txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
                btn_extrc.tooltip = "Alternar EXTRUSOR"
                btn_extrc.on_click = toggle_extrc

                page.update()

                logging.info("# Reles y sensores actualizados por feedback")

            else:
                logging.warning(f"## Topico no registrado: {topico}")
                print(f"## Topico no registrado: {topico}")

    ##############################################################################
    # Configuración del cliente MQTT ###############################################################################
    broker = "10.6.20.236"  # Dirección IP de tu computadora
    client = mqtt.Client()  # Crear un cliente MQTT
    client.on_message = on_message  # Configuración de callbacks

    mqtt_connect(client)  # Conectar al broker MQTT
    actualizar_app(None)  # Solicitar actualizaciones

    """ Fin Conexión MQTT """

    ##############################################################################
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
    )
    if txf_fan.value == "Unknown":
        btn_fan.tooltip = "Sin conexión"
    elif txf_fan.value != "Unknown":
        btn_fan.on_click = toggle_fan
        btn_fan.tooltip = txf_fan.value
        
    btn_extrc = ft.IconButton(
        icon=ft.icons.MODE_FAN_OFF_ROUNDED,
        col=3,
    )
    if txf_extrc.value == "Unknown":
        btn_extrc.tooltip = "Sin conexión"
    elif txf_extrc.value != "Unknown":
        btn_extrc.on_click = toggle_extrc
        btn_extrc.tooltip = txf_extrc.value

    btn_toggle = ft.IconButton(
        icon=ft.icons.MODE_FAN_OFF_ROUNDED,
        col=3,
        tooltip="Alternar todos los reles",
        on_click=toggle_reles
    )
    btn_off = ft.IconButton(
        icon=ft.icons.POWER_OFF,
        col=3,
        on_click=off_reles,
        tooltip="Apagar todos los reles",
    )
    btn_on = ft.IconButton(
        icon=ft.icons.POWER,
        col=3,
        tooltip="Encender todos los reles",
        on_click=on_reles
    )

    btns = {"btn_fan": btn_fan, "btn_extrc": btn_extrc}

    # Configuración de la 1RA Fila
    toggle_row.controls.append(btn_toggle)
    toggle_row.controls.append(btn_off)
    toggle_row.controls.append(btn_on)

    bts_system = ft.Container(
        content=toggle_row,
        padding=5,
        alignment=ft.alignment.center,
        border_radius=10,
    )

    fr_row.width = page.window_width
    fr_row.controls.append(system_values(btns, values, bts_system))

    # Configuración de la 2DA Fila
    sc_row.width = page.window_width

    """ Fin Variables globales de la pagina """

    ###############################################################
    # Agregar datos a la pagina ############################################################################
    # Direccionador de rutas de la aplicación
    def route_change(route):
        # CARGA DE PAGINAS
        from page.home.home import home
        from page.funcional_mqtt import conexión_mqtt

        # Configuracion de de la pagina: HOME
        home_page = home()
        appbar_home_page = home_page[0]
        btn_config_home_page = home_page[1]
        btn_config_home_page.on_click = lambda _: page.go("/configuration")

        btn_stats_home_page = home_page[2] 
        btn_stats_home_page.on_click = lambda _: print("/app")

        
        # Configuracion de la pagina: Conexión con MQTT
        app_page = conexión_mqtt()
        appbar_app_page = app_page[0]
        appbar_app_page.actions.append(
            ft.IconButton(
                icon=ft.icons.ENERGY_SAVINGS_LEAF, 
                padding=15, 
                on_click=actualizar_app,
            )
        )
        
        safearea_app_page = app_page[1]
        safearea_app_page.controls.append(fr_row)
        safearea_app_page.controls.append(sc_row)


        time.sleep(1)
        page.views.clear()
        page.views.append(ft.View(
            "/",
            controls = [
                appbar_home_page,
                btn_config_home_page,
                btn_stats_home_page,
                ft.IconButton(
                    icon=ft.icons.APP_SHORTCUT,
                    on_click=lambda _: page.go("/esp32_online"),
                )
            ]
            )
        )

        # RUTAS
        if page.route == "/esp32_online":
            page.views.append(
                ft.View(
                    route="/app",
                    appbar=appbar_app_page,
                    controls=safearea_app_page
                )
            )

        # ACTUALIZAR PAGINA
        page.update()

    # Cambio de ventana
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    
    # CARGA DE PAGINAS
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    
    #page.add(appbar, safearea)
    
    """ Fin Agregar datos a la pagina """


###############################################################################
# Lanzamiento de la aplicación ###############################################################################
ft.app(target=main)