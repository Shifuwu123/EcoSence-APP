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
    page.window_min_width = 300
    page.window_width = 550
    page.theme = ft.Theme(color_scheme_seed="green")
    page.window_always_on_top = True

    """ Fin aspectos generales de la pagina """

    ###############################################################
    """ Agregar datos a la pagina """
    page.add(
        appbar_main,  # Appbar de la pagina
        cnts_stats_page("estadísticas"),
    )
    """ Fin Agregar datos a la pagina """


ft.app(target=main)
