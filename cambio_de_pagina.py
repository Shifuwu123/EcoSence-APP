import flet as ft
from flet import Page

import paho.mqtt.client as mqtt

import json, time

################################################################################################
# Configuración del cliente MQTT ###############################################################################
broker = "192.168.93.90"
topic = "EcoSense/esp32/#"
client = mqtt.Client()

try:
    from pages.connections.verificacion_mqtt import mqtt_connect

    mqtt_connect(client, broker, topic)

except Exception as e:
    print(e)

#################################################################################################################
# Variables globales ###############################################################################################
from decorators.app_class import txf_sensor, txf_rele

# - Sincronización
app_sync = False
btn_sync = ft.TextButton(
    text="Connect",
    icon=ft.icons.ROUTER,
    tooltip="Ir a APP",
    disabled=not app_sync,
)
snackbar_esp32_offline = ft.SnackBar(
    content=ft.Text("ESP32 Desconectado!", color=ft.colors.BLACK),
    bgcolor=ft.colors.RED,
)

# - Valores de los sensores
environment_values = {"temp": None, "humd": None, "tier": None}
txf_temp_value = txf_sensor(value=f"{None} °C", label="Real")
txf_humd_value = txf_sensor(value=f"{None} %", label="Real")
txf_tier_value = txf_sensor(value=f"{None}", label="Real")

# - Valores de los Reles
reles_values = {"fan": 0, "extrc": 0}
txf_fan = txf_rele(label="Ventilador", value="Unknown")
txf_extrc = txf_rele(label="Extractor", value="Unknown")


#################################################################################################
def main(page: Page):
    def offline():
        page.snack_bar = snackbar_esp32_offline
        page.snack_bar.open = True

    def toggle_fan(e):
        reles_values["fan"] = not reles_values["fan"]
        txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
        client.publish("EcoSense/plc/rele1", json.dumps({"fan": reles_values["fan"]}))
        
        page.update()
        print(f"toggle Fan: {reles_values['fan']}")
    
    def toggle_extrc(e):
        reles_values["extrc"] = not reles_values["extrc"]
        txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
        client.publish("EcoSense/plc/rele2", json.dumps({"extrc": reles_values["extrc"]}))
        page.update()
        print(f"toggle Extractor: {reles_values['extrc']}")

    def on_message(client, userdata, msg):
        def sync(mensaje):
            mensaje = {"temp": 30, "humd": 50, "tier": 50, "rele1": 1, "rele2": 0}

            # Parametros del cultivo
            environment_values["temp"] = float(mensaje["temp"])
            environment_values["humd"] = float(mensaje["humd"])
            environment_values["tier"] = float(mensaje["tier"])

            # Estado de los Reles (sistema)
            reles_values["fan"] = int(mensaje["rele1"])
            reles_values["extrc"] = int(mensaje["rele2"])

            print("# Estados de los Reles y Valores de los sensores actualizados")

        def feedback(mensaje):
            txf_temp_value.value = f"{environment_values['temp']} °C"
            txf_humd_value.value = f"{environment_values['humd']} %"
            txf_tier_value.value = f"{environment_values['tier']}"

            txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
            txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"

            btn_fan.tooltip = "Alternar VENTILADOR"
            btn_extrc.tooltip = "Alternar EXTRUSOR"
            btn_fan.disabled = False
            btn_extrc.disabled = False

            page.update()
            print("# Reles y sensores actualizados en la pagina APP")
        
        ################################################################################
        # Procesar el topico y mensaje
        topico = msg.topic
        mensaje = json.loads(msg.payload)         
        
        # Evaluamos el topico y el mensaje
        if topico == "EcoSense/esp32/sync":
            global app_sync
            app_sync = bool(mensaje["sync"])
            if mensaje:    
                app_sync = True
                client.publish("EcoSense/plc/feedback", json.dumps({"feedback": True}))
                print(f"Mensaje de actualizacion {json.dumps({"feedback": True})} enviado a 'EcoSense/plc/actualizacion'")
                if page.route == "/":
                    global btn_ecosense
                    btn_ecosense.disabled = not app_sync
                    
                elif page.route == "/mqtt_page":
                    global btn_connect
                    btn_connect.text = "Conectado"
                    btn_connect.disabled = not app_sync

            else:
                offline()
                app_sync = False
                btn_connect.text = "Desconectado"
                btn_connect.disabled = not app_sync
                btn_ecosense.disabled = not app_sync
                view_pop(None)

            page.update()

        # Si la aplicación esta en la pagina principal
        if app_sync:
            try:
                mensaje = json.loads(msg.payload)
            except Exception as e:
                print(f"## Error al procesar el mensaje: {e}")

            # Procesar el topico
            if topico == "EcoSense/esp32/feedback":
                sync(mensaje)
                feedback(mensaje)
            
            elif topico == "EcoSense/esp32/sync":
                pass

            elif topico == "EcoSense/esp32/sensores":
                environment_values["temp"] = float(mensaje["temp"])
                environment_values["humd"] = float(mensaje["humd"])
                environment_values["tier"] = float(mensaje["tier"])

                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                txf_tier_value.value = f"{environment_values['tier']}"
                page.update()

            elif topico == "EcoSense/esp32/sensor/dht11":
                environment_values["temp"] = float(mensaje["temp"])
                environment_values["humd"] = float(mensaje["humd"])
                txf_temp_value.value = f"{environment_values['temp']} °C"
                txf_humd_value.value = f"{environment_values['humd']} %"
                page.update()

            elif topico == "EcoSense/esp32/sensor/hd38":
                environment_values["tier"] = float(mensaje["tier"])
                txf_tier_value.value = f"{environment_values['tier']}"
                page.update()

            elif topico == "EcoSense/esp32/rele1":
                reles_values["fan"] = int(mensaje["rele1"])
                txf_fan.value = "Encendido" if reles_values["fan"] else "Apagado"
                page.update()

                print("# Rele1 actualizado")

            elif topico == "EcoSense/esp32/rele2":
                reles_values["extrc"] = int(mensaje["rele2"])
                txf_extrc.value = "Encendido" if reles_values["extrc"] else "Apagado"
                page.update()

                print("# Rele2 actualizado")

                
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
    client.on_message = on_message

    ###############################################################
    # Variables globales de la pagina #############################
    # - Variables globales de Reles
    btn_fan = ft.IconButton(icon=ft.icons.LIGHT_MODE, col=3, on_click=toggle_fan)
    if txf_fan.value == "Unknown":
        btn_fan.tooltip = "Sin conexión"
        btn_fan.disabled = True
    elif txf_fan.value != "Unknown":
        btn_fan.disabled = False

    btn_extrc = ft.IconButton(icon=ft.icons.MODE_FAN_OFF_ROUNDED, col=3, on_click=toggle_extrc)
    if txf_extrc.value == "Unknown":
        btn_extrc.tooltip = "Sin conexión"
        btn_extrc.disabled = True
    elif txf_extrc.value != "Unknown":
        btn_extrc.disabled = False

    ###########################################################################
    # Función para actualizar la informacion de la pagina
    def route_change(route):
        from pages.home.home_page import home_page as home
        from pages.app.app import app_page as app
        from pages.components.mqtt import mqtt_page as mqtt
        from pages.components.cultivo import crop_info
        from pages.components.sistema import system_info
        from pages.components.parametros import params_info
        from pages.components.estadisticas import stats_info

        page.views.clear()

        ################################################################################
        # HOME_PAGE ###################################################################
        global home_page
        home_page = home()
        btn_mqtt = ft.TextButton(
            text="MQTT",
            icon=ft.icons.PRIVATE_CONNECTIVITY,
            on_click=lambda _: page.go("/mqtt_page"),
            col=1,
        )
        global btn_ecosense
        btn_ecosense = ft.TextButton(
            text="EcoSense",
            icon=ft.icons.ENERGY_SAVINGS_LEAF_OUTLINED,
            on_click=lambda _: page.go("/app_page"),
            col=1,
            disabled=not app_sync,
        )
        home_page.append(
            ft.ResponsiveRow(
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                columns=2,
                controls=[btn_mqtt, btn_ecosense],
            )
        )
        
        global btn_connect
        btn_connect = ft.TextButton(
            text="Conectado" if app_sync else "Desconectado",
            icon=ft.icons.ROUTER,
            tooltip="MQTT",
            disabled=not app_sync,
            on_click=lambda _: page.go("/mqtt_page"),
        )
        
        # Agregamos el home_page a la pagina principal
        page.views.append(ft.View("/", home_page))

        # MQTT_PAGE ###########################################################
        if page.route == "/mqtt_page":
            # Cargamos la informacion de MQTT
            mqtt_values = ft.Column(
                controls=[
                    ft.Text("Broker MQTT"),
                    ft.TextField(label="Broker", value=broker, read_only=True),
                    ft.TextField(label="Topic", value=topic, read_only=True),
                ],
                col=1,
            )
            mqtt_page = mqtt(
                mqtt_values,
                app_sync,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[btn_connect],
                )
            )
            
            # Agregamos el mqtt_page a la pagina principal
            page.views.append(ft.View("/mqtt_page", mqtt_page))

        # APP_PAGE ############################################################
        elif page.route == "/app_page":
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

            crop = crop_info(crop_name, crop_week, crop_phase)

            # Creamos el objeto de informacion del sistema
            system = system_info(txf_fan, btn_fan, txf_extrc, btn_extrc)

            # Cargamos informacion de los parametros
            params = params_info(txf_temp_value, txf_humd_value, txf_tier_value)

            # Cargamos informacion de las estadisticas
            stats = stats_info()

            # Cargamos la pagina de la aplicación
            app_page = app(crop, system, params, stats)
            page.views.append(ft.View("/app_page", app_page))

        page.update()
        print(f"## Route change terminado a {page.route}")
    ##########################################################################
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # CARGA DE PAGINAS
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    client.publish("EcoSense/plc/sync", json.dumps({"sync": True}))
    print("## APP cargada y solicitud de actualizacion enviada")

    page.go(page.route)


ft.app(target=main)
