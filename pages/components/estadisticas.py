import flet as ft
from decorators.app_class import containers_app_page as container
from pages.components.grafico import grafico


def stats_info() -> ft.Container:
    graph = container(grafico())
    graph.padding = 20

    card = ft.Card(
        color=ft.colors.GREEN_ACCENT_400,
        margin=10,
        elevation=2.0,
        col=1,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                container(ft.Text("Estadisticas")),
                graph
            ],
        ),
    )

    return card
