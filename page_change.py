import flet as ft


def main(page: ft.Page):
    page.title = "EcoSence"
    page.adaptive = True
    
    def route_change(route):
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
                        ft.TextField(
                            value="aqui iria la info del cultivo",
                        ),
                        ft.TextField(
                            value="aqui iria la info del sistema",
                        ),

                    ],
                    width=page.window_width,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    wrap=True,
                    spacing=5,
                    run_spacing=5,
                    controls=[
                        ft.TextField(
                            value="aqui iria la info de los parametros",
                        ),
                        ft.TextField(
                            value="aqui iria la info de las estadisticas",
                        ),
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
        from page.home.home_page import home_page as home

        page.views.clear()
        page.views.append(ft.View("/", home()))

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
