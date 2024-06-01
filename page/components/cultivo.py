import flet as ft


def crop_info(nombre_cultivo, semana_cultivo, fase_cultivo):
    return ft.Container(
        bgcolor=ft.colors.GREEN,
        padding=10,
        alignment=ft.alignment.center,
        col=1,
        content=ft.Column(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_600,
                    padding=10,
                    border_radius=10,
                    alignment=ft.alignment.center,
                    content=ft.Text("Crop"),
                ),
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_600,
                    padding=10,
                    border_radius=10,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            nombre_cultivo,
                            semana_cultivo,
                            fase_cultivo,
                        ]
                    ),
                ),
            ]
        ),
    )
