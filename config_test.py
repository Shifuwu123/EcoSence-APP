import flet as ft, typing as t
from graph_config import *
from data_test import *


################################################################################
# Filas de Contenedores de Parametros
class rrw_cnt_params(ft.ResponsiveRow):
    def __init__(
        self,
        param: t.Literal["temp", "humd", "tier", "lgt_qlty"],
        txf_value: ft.TextField,
    ):
        if param == "temp":
            parametro = "Temperatura: "
            tipo_dato = "°C"

        elif param == "humd":
            parametro = "Humedad: "
            tipo_dato = "%"

        elif param == "tier":
            parametro = "Humedad de la tierra: "
            tipo_dato = "%"

        # Inicializamos la fila responsiva
        super().__init__()
        self.controls = [
            ft.TextField(
                value=parametro,
                text_align=ft.TextAlign.CENTER,
                text_size=16,
                multiline=True,
                read_only=True,
                disabled=True,
                col=6,
                border_width=0,
                color=ft.colors.WHITE,
            ),  # Parametro
            txf_value,  # Valor REAL del parametro
            ft.TextField(
                value=f"20 {tipo_dato}",
                label="Ideal",
                text_size=13,
                multiline=True,
                read_only=True,
                col=3,
                text_align=ft.TextAlign.CENTER,
            ),  # Valor IDEAL del parametro
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.col = 4
        self.width = 380
        self.columns = 12


class rrw_cnt_system(ft.ResponsiveRow):
    def __init__(
        self,
        rele,
        button: ft.ElevatedButton,
    ):
        # Inicializamos la fila responsiva
        super().__init__()
        self.controls = [
            # Actuador
            rele,
            # Estado del actuador e icono animado
            button,
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.width = 380
        self.height = 60
        self.columns = 12


# Contenedor responsivo de los parámetros
class cnt_params(ft.Container):
    def __init__(self, temp_value, humd_value, tier_value):
        super().__init__()
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            rrw_cnt_params(param="temp", txf_value=temp_value),
                            rrw_cnt_params(param="humd", txf_value=humd_value),
                            rrw_cnt_params(param="tier", txf_value=tier_value),
                        ],
                        columns=4,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                width=350,
            ),
            padding=10,
            bgcolor=ft.colors.BLUE_GREY_800,
            border_radius=10,
        )
        self.bgcolor = ft.colors.GREEN_600
        self.padding = 20
        self.border_radius = 10


class cnt_system(ft.Container):
    def __init__(self, buttons: dict, values: dict):
        super().__init__()
        self.content = ft.Container(
            content=ft.Column(
                # Contenedor responsivo de los parámetros
                controls=[
                    rrw_cnt_system(values['fan'], buttons["btn_fan"]),
                    rrw_cnt_system(values['extrc'], buttons["btn_extrc"]),
                ],
                width=350,
            ),
            padding=10,
            bgcolor=ft.colors.BLUE_GREY_800,
            border_radius=10,
        )
        self.bgcolor = ft.colors.GREEN_600
        self.padding = 20
        self.border_radius = 10
