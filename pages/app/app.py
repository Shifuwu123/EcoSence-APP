import flet as ft


def app_page(info_crop, info_system, info_params, info_stats):
    return [
        ft.AppBar(title=ft.Text("EcoSense - SYSTEM ONLINE")),
        ft.ListView(
            expand=1,
            spacing=10,
            controls=[
                ft.ResponsiveRow(
                    columns=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[info_crop, info_system],
                ),
                ft.ResponsiveRow(
                    columns=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[info_params, info_stats],
                ),
            ],
            auto_scroll=True,
        ),
    ]