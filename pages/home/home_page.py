import flet as ft
from decorators.home_class import elements


def home_page():
    cultivo = elements(color=ft.colors.AMBER, content=ft.Text("Cultivo", color=ft.colors.BLACK))
    sistema = elements(color=ft.colors.GREEN_200, content=ft.Text("Sistema", color=ft.colors.BLACK))
    parametros = elements(color=ft.colors.CYAN_200, content=ft.Text("Parametros", color=ft.colors.BLACK))
    estadisticas = elements(
        color=ft.colors.RED_ACCENT_200, content=ft.Text("Estadisticas", color=ft.colors.BLACK)
    )

    return [
        ft.AppBar(title=ft.Text("EcoSense APP")),
        ft.Container(
            bgcolor=ft.colors.GREEN,
            padding=20,
            margin=10,
            alignment=ft.alignment.center,
            content=ft.Card(
                color=ft.colors.BLUE_GREY_600,
                content=ft.Container(
                    padding=10,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Text(
                                "EcoSense APP",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "   Esta es una aplicación para la gestión de tus cultivos. Podrás gestionar tus cultivos de forma sencilla monitorizando los siguientes elementos:",
                                size=15,
                            ),
                            ft.Row(
                                controls=[cultivo, sistema, parametros, estadisticas],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                    )
                )
            ),
        ),
    ]
