import flet as ft
import typing as t
from decorators.app_class import containers_app_page as container

class rrw_cnt_params(ft.ResponsiveRow):
    def __init__(
        self,
        param: t.Literal["temp", "humd", "tier"],
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
        self.columns = 12

def params_info(temp_value, humd_value, tier_value):
    card = ft.Card(
        color=ft.colors.GREEN_ACCENT_400,
        margin=10,
        elevation=2.0,
        col=1,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                # Title
                container(
                    ft.Text("Parametros")
                ),
                container(
                    ft.Column(
                        controls=[
                            rrw_cnt_params(param="temp", txf_value=temp_value),
                            rrw_cnt_params(param="humd", txf_value=humd_value),
                            rrw_cnt_params(param="tier", txf_value=tier_value),
                        ]
                    )
                )
            ]
        )
    )
    
    return card
