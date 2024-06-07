import flet as ft


def app_page(info_crop, info_system, info_params, info_stats, width):
    return [
        ft.AppBar(title=ft.Text("EcoSense - SYSTEM ONLINE")),
        ft.ListView(
            expand=1,
            spacing=10,
            controls=[
                ft.Row(
                    controls=[info_crop, info_system],
                    alignment=ft.MainAxisAlignment.CENTER,
                    # Hacer la pagina responsiva
                    wrap=True,
                    spacing=15,
                    run_spacing=5,
                    width=width,
                ),
                ft.Row(
                    controls=[info_params, info_stats],
                    alignment=ft.MainAxisAlignment.CENTER,
                    # Hacer la pagina responsiva
                    wrap=True,
                    spacing=15,
                    run_spacing=5,
                    width=width,

                ),
            ]
        ),
    ]