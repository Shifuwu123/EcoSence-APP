def estadisticas():
    return [
        # Barra superior
        ft.AppBar(
            title=ft.Text("Statistics"),
            actions=[
                ft.IconButton(
                    icon=ft.icons.ENERGY_SAVINGS_LEAF,
                    padding=ft.padding.all(10),
                    on_click=lambda _: page.go("/"),
                ),
            ],
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.TEAL_ACCENT_400),
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            wrap=True,
            spacing=5,
            run_spacing=5,
            controls=[
                InfoCropContainer(),
                InfoSystemContainer(),
            ],
            width=page.window_width,
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            wrap=True,
            spacing=5,
            run_spacing=5,
            controls=[
                InfoSystemContainer(),
                InfoCropContainer(),
            ],
            width=page.window_width,
        ),
    ]
