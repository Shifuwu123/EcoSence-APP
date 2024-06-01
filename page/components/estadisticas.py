import flet as ft
from config import cnt_stats as grafico

def stats_info() -> ft.Container:
    return ft.Container(
        bgcolor=ft.colors.GREEN,
        padding=10,
        alignment=ft.alignment.center,
        col=1,
        content=ft.Column(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_600,
                    padding=15,
                    border_radius=10,
                    alignment=ft.alignment.center,
                    content=ft.Text("Estadisticas", color=ft.colors.WHITE),
                ),
                grafico()
            ]
        ),
    )
