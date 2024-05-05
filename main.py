import flet as ft
from flet import Page

from data import *
from config import *

###############################################################################
""" Variables globales """

# Appbar de la pagina principal
appbar_main = ft.AppBar(
    title=ft.Text("Estadísticas 🗃️"),
    actions=[ft.IconButton(icon=ft.icons.ENERGY_SAVINGS_LEAF, padding=15)],
    bgcolor=ft.colors.with_opacity(0.04, ft.colors.TEAL_ACCENT_400),
)

""" Fin Variables globales """
###############################################################################
""" Paginas de la aplicación """


def main(page: Page):
    ###############################################################
    """Aspectos generales de la pagina"""
    page.title = "EcoSense"
    page.adaptive = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_min_width = 380
    page.window_width = 400
    page.theme = ft.Theme(color_scheme_seed="green")
    page.window_always_on_top = True

    """ Fin aspectos generales de la pagina """

    ###############################################################
    """ Agregar datos a la pagina """
    page.add(
        appbar_main,  # Appbar de la pagina
        ft.ListView(
            controls=[
                ft.Row(
                    controls=[
                        cnts_stats_page("cultivo"),
                        cnts_stats_page("sistema"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    # Hacer la pagina responsiva
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    width=page.window_width,
                ),
                ft.Row(
                    controls=[
                        cnts_stats_page("parámetros"),
                        cnts_stats_page(
                            "estadísticas",
                            chart=chart,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    # Hacer la pagina responsiva
                    wrap=True,
                    spacing=5,
                    run_spacing=5,
                    width=page.window_width,
                ),
            ],
            expand=1,
            spacing=10
        ),
    )
    """ Fin Agregar datos a la pagina """


ft.app(target=main)
