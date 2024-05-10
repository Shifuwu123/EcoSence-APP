import flet as ft
from data import data_humedad as data_parametros
from graph_config import *

grafico = ft.Container(
    graph_major(data_series=data_parametros),
    padding=ft.Padding(15, 10, 30, 10),
    bgcolor=ft.colors.GREEN_900,
    width=360,
)


def main(page: ft.Page):
    page.window_always_on_top = True
    page.add(
        ft.Container(
            content=grafico,
            padding=10,
            bgcolor=ft.colors.GREEN_600,
        )
    )


ft.app(target=main)
