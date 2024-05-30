def home():
    return [
        ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.ENERGY_SAVINGS_LEAF,
                icon_color=ft.colors.TEAL_600,
                padding=ft.padding.all(10),
            ),
            title=ft.Text("EcoSence"),
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.TEAL_ACCENT_400),
        ),
        ft.ElevatedButton(
            "Configuración", on_click=lambda _: print("Configuración")
        ),
        ft.ElevatedButton(
            "Estadísticas", on_click=lambda _: print("Estadísticas")
        ),
    ]
