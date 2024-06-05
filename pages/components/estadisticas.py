import flet as ft
from config import cnt_stats as grafico
from decorators.app_class import containers_app_page as container


def stats_info() -> ft.Container:
    card = ft.Card(
        color=ft.colors.GREEN_ACCENT_400,
        margin=10,
        elevation=2.0,
        col=1,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                container(
                    ft.Text("Estadisticas")
                ),
                grafico(),
            ],
        ),
    )

    return card
