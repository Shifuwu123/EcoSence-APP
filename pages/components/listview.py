import flet as ft

def EcoSense(cultivo, sistema, parametros, estadisticas):
    return ft.ListView(
        expand=1,
        spacing=10,
        controls=[
            ft.ResponsiveRow(
                columns=2,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                run_spacing=15,
                controls=[
                    cultivo,
                    sistema
                ]
            ),
            ft.ResponsiveRow(
                columns=2,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                run_spacing=15,
                controls=[
                    parametros,
                    estadisticas
                ]
            ),
        ],
    )