import flet as ft
from pages.connections.verificar_wifi import get_network_ssid

ssid = get_network_ssid()

def mqtt_page(mqtt_configuration, btn_next):
    return [
        ft.AppBar(title=ft.Text("Wifi Configuration")),
        ft.ResponsiveRow(
            columns=2,
            controls=[
                # Wifi Configuration
                ft.Column(
                    col=1,
                    controls=[
                        ft.Text("Wifi Configuration"),
                        ft.TextField(label="SSID", value=ssid, read_only=True),
                    ],
                    
                ),
                mqtt_configuration,
            ],
            
        ),
        btn_next,
    ]
