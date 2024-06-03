import flet as ft
from pages.connections.verificar_wifi import get_network_ssid

ssid = get_network_ssid()


def mqtt_page(mqtt_configuration, sync_on, btn_sync):
    return [
        ft.AppBar(title=ft.Text("Wifi Configuration")),
        ft.ResponsiveRow(
            columns=2,
            controls=[
                mqtt_configuration,
                ft.Column(
                    col=1,
                    controls=[
                        ft.Text("ESP32 Configuration"),
                        ft.TextField(
                            label="Connection",
                            value=str(sync_on).upper(),
                            text_align=ft.TextAlign.CENTER,
                            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                            read_only=True,
                        ),
                        btn_sync,
                    ],
                ),
            ],
        ),
    ]
