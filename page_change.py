def main(page: ft.Page):
    page.title = "EcoSence"
    page.adaptive = True
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.TEAL_ACCENT_700,
            on_primary=ft.colors.GREEN_ACCENT_700,
            secondary=ft.colors.TEAL_ACCENT_400,
            on_secondary=ft.colors.GREEN_ACCENT_400,
        )
    )

    def route_change(route):
        # BOTONES ###############################################################

        # PAGINAS ##############################################################
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
                    "Configuración", on_click=lambda _: page.go("/configuration")
                ),
                ft.ElevatedButton(
                    "Estadísticas", on_click=lambda _: page.go("/statistics")
                ),
            ]

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

        def configuracion():
            return [
                ft.AppBar(title=ft.Text("Configuration")),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(
                                    "Go Home", on_click=lambda _: page.go("/")
                                ),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(
                                    "Go Statistics",
                                    on_click=lambda _: page.go("/statistics"),
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]

        ##################################################
        # CARGA DE PAGINAS
        page.views.clear()
        page.views.append(ft.View("/", home()))

        # TEMA
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                background=ft.colors.TEAL_ACCENT_400,
                on_background=ft.colors.TEAL_50,
                primary=ft.colors.TEAL_ACCENT_700,
                on_primary=ft.colors.TEAL_50,
                secondary=ft.colors.TEAL_ACCENT_200,
                on_secondary=ft.colors.TEAL_50,
            )
        )

        # RUTAS
        if page.route == "/configuration":
            page.views.append(ft.View("/configuration", configuracion()))

        if page.route == "/statistics":
            page.views.append(ft.View("/statistics", estadisticas()))

        # ACTUALIZAR PAGINA
        page.update()

    ##########################################################################
    # Cambio de ventana
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # CARGA DE PAGINAS
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
