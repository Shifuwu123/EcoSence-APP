import flet as ft
from decorators.app_class import containers_app_page as container

def crop_info(nombre_cultivo, semana_cultivo, fase_cultivo):
    card = ft.Card(
        color=ft.colors.GREEN_ACCENT_400,
        margin=10,
        elevation=2.0,
        col=1,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                # Titulo
                container(
                    ft.Text("Cultivo"),
                ),
                # Información
                container(
                    ft.Column(
                        controls=[
                            nombre_cultivo,
                            semana_cultivo,
                            fase_cultivo,
                        ]
                    )
                ),
            ],
        ),
    )

    return card
