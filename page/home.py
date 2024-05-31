import flet as ft

def home():
    appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.icons.ENERGY_SAVINGS_LEAF,
            icon_color=ft.colors.TEAL_600,
            padding=ft.padding.all(10),
        ),
        title=ft.Text("EcoSense"),
        bgcolor=ft.colors.with_opacity(0.04, ft.colors.TEAL_ACCENT_400),
    )
    btn_configuracion = ft.ElevatedButton(
        "Configuración"
    )
    btn_estadisticas = ft.ElevatedButton(
        "Estadísticas"
    )

    return [appbar, btn_configuracion, btn_estadisticas]
    
