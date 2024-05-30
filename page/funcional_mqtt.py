import flet as ft


def conexión_mqtt():
    appbar = ft.AppBar(
        title=ft.Text("Estadísticas 🗃️"),
        bgcolor=ft.colors.with_opacity(0.04, ft.colors.TEAL_ACCENT_400),
    )

    # Vista de la pagina principal
    safearea = ft.ListView(
        expand=1,
        spacing=10,
    )

    return [appbar, safearea]
