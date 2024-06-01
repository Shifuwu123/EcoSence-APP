import flet as ft
from flet import Page

import paho.mqtt.client as mqtt
from page.connections.verificacion_mqtt import mqtt_connect
import json

################################################################################################
# Configuración del cliente MQTT ###############################################################################
broker = "192.168.0.9"
topic = "EcoSense/esp32/#"
client = mqtt.Client()

try:
    mqtt_connect(client, broker, topic)  # Conectar al broker MQTT

except Exception as e:
    print(e)
    exit(1)

#################################################################################################################
# Variables globales ###############################################################################################
# - Sincronización
btn_sync = ft.TextButton(
    text="Connect",
    icon=ft.icons.ROUTER,
    tooltip="Ir a APP",
    disabled=True,
)
# - Valores de los sensores
environment_values = {
    "temp": None,
    "humd": None,
    "tier": None,
}

# - Text Fields con valores de los sensores
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

# - Valores de los Reles
reles_values = {
    "fan": 0,
    "extrc": 0,
}
# - TextFields de los Reles
txf_fan = ft.TextField(
    label="Ventilador",
    value='Unknown',
    read_only=True,
    col=7,
    text_align=ft.TextAlign.CENTER,
)
txf_extrc = ft.TextField(
    label="Extractor",
    value='Unknown',
    read_only=True,
    col=7,
    text_align=ft.TextAlign.CENTER,
)

#################################################################################################
def main(page: Page):
    def on_message(client, userdata, msg):
        topico = msg.topic
        print(f"### Mensaje recibido en {topico}: {msg.payload}")

        # Si la aplicación esta en la pagina principal
        if page.route == "/app_page":
            try:
                # Procesar el mensaje
                mensaje = json.loads(msg.payload) 

            except Exception as e:
                print(f"## Error al procesar el mensaje: {e}")
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

            elif topico == "EcoSense/esp32/sensor/dht11":
                environment_values['temp'] = float(mensaje["temp"])
                environment_values['humd'] = float(mensaje["humd"])
                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                page.update()
                
            elif topico == "EcoSense/esp32/sensor/hd38":
                environment_values['tier'] = float(mensaje["tier"])
                txf_tier_value.value = f"{environment_values['tier']}"
                page.update()
                
            elif topico == "EcoSense/esp32/rele1":
                reles_values['fan'] = int(mensaje["rele1"])
                txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
                page.update()

                print("# Rele1 actualizado")

            elif topico == "EcoSense/esp32/rele2":
                reles_values['extrc'] = int(mensaje["rele2"])
                txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
                page.update()

                print("# Rele2 actualizado")

            elif topico == "EcoSense/esp32/feedback":
                btn_sync.on_click=lambda _: page.go("/app_page"),
                btn_sync.disabled=False

                environment_values['temp'] = float(mensaje["temp"])
                environment_values['humd'] = float(mensaje["humd"])
                environment_values['tier'] = float(mensaje["tier"])

                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                txf_tier_value.value = f"{environment_values['tier']}"

                reles_values['fan'] = int(mensaje["rele1"])
                txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
                btn_fan.tooltip = "Alternar VENTILADOR"
                #btn_fan.on_click = toggle_fan

                reles_values['extrc'] = int(mensaje["rele2"])
                txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
                btn_extrc.tooltip = "Alternar EXTRUSOR"
                #btn_extrc.on_click = toggle_extrc

                page.update()

                print("# Reles y sensores actualizados por feedback")

            else:
                print(f"## Topico no registrado: {topico}")
    
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
    # Variables globales de la pagina #############################
    # - Variables globales de Reles
    btn_fan = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        col=3,
    )
    if txf_fan.value == "Unknown":
        btn_fan.tooltip = "Sin conexión"
    elif txf_fan.value != "Unknown":
        btn_fan.on_click = print("toggle_fan")
        btn_fan.tooltip = txf_fan.value
        
    btn_extrc = ft.IconButton(
        icon=ft.icons.MODE_FAN_OFF_ROUNDED,
        col=3,
    )
    if txf_extrc.value == "Unknown":
        btn_extrc.tooltip = "Sin conexión"
    elif txf_extrc.value != "Unknown":
        btn_extrc.on_click = print("toggle_extrc")
        btn_extrc.tooltip = txf_extrc.value

    ###########################################################################
    def route_change(route):
        from page.home.home_page import home_page as home
        from page.app.app import app_page as app
        from page.components.cultivo import crop_info
        from page.components.sistema import system_info
        from page.components.parametros import params_info
        from page.components.estadisticas import stats_info

        ################################################################################
        # CARGA DE PAGINAS
        page.views.clear()

        # Configuracion de pagina principal
        mqtt_values = ft.Column(
            controls=[
                ft.Text("Broker MQTT"),
                ft.TextField(label="Broker", value=broker, read_only=True),
                ft.TextField(label="Topic", value=topic, read_only=True),
            ],
            col=1,
        )
        btn_next_page = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                btn_sync,
            ],
        )
        home_page = home(mqtt_values, btn_next_page)
        page.views.append(ft.View("/", home_page))

        # Rutas de la pagina
        if page.route == "/app_page":
            ###############################################################################
            # Cargamos informacion del cultivo
            crop_name = ft.TextField(
                label="Nombre:",
                value="Unknown",
                read_only=True,
            )
            crop_week = ft.TextField(
                label="Semana:",
                value="Unknown",
                read_only=True,
            )
            crop_phase = ft.TextField(
                label="Fase:",
                value="Unknown",
                read_only=True,
            )
            
            crop = crop_info(crop_name, crop_week, crop_phase)  # Creamos el objeto con la informacion del cultivo

            ###############################################################################
            # Creamos el objeto de informacion del sistema
            system = system_info(txf_fan, btn_fan, txf_extrc, btn_extrc)

            ###############################################################################
            # Cargamos informacion de los parametros
            params = params_info(txf_temp_value, txf_humd_value, txf_tier_value)

            ##############################################################################
            # Cargamos informacion de las estadisticas
            stats = stats_info()

            ##############################################################################
            # Cargamos la pagina de la aplicación
            app_page = app(crop, system, params, stats)
            page.views.append(ft.View("/app_page", app_page))

        page.update()

    # Visualización de la pagina
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # CARGA DE PAGINAS
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
