import flet as ft, typing as t
from data import *
from graph_config import *

################################################################################
""" Configuración Menus """


def toggle_data(e):
    parametro = menu_graficos.value
    chart.data_series = grafico[parametro]
    chart.update()


class dpbx_graficos(ft.Dropdown):
    def __init__(self):
        super().__init__()
        self.on_change = toggle_data
        self.options = [
            ft.dropdown.Option("Temperatura"),
            ft.dropdown.Option("Humedad"),
            ft.dropdown.Option("Tierra"),
            ft.dropdown.Option("Luz"),
            ft.dropdown.Option("Agua"),
        ]
        self.text_size = 14
        self.content_padding = 10


""" Fin configuración Menus """
################################################################################
""" Filas de Contenedores de Sistema """


class rw1_cnt_gral_stats(ft.Row):
    def __init__(
        self,
        titulo: t.Literal[
            "Información del sistema",
            "Información del cultivo",
            "Información de los parámetros",
            "Información de las estadísticas",
        ],
        icono,
    ):
        # Definimos el título, el icono y el contenido correspondiente
        super().__init__()
        self.controls = [
            # Icono y titulo del contenedor de Estadísticas Generales
            ft.Icon(name=icono, size=28),
            ft.Text(
                value=titulo,
                size=15,
                text_align=ft.TextAlign.CENTER,
            ),
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.height = 55
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER


""" Fin Filas de Contenedores de Sistema """
##################################################################################
""" Contenedor de Estadísticas """


class cnt_stats(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Column(
            controls=[
                # 1ra fila con titulo y menu de graficos
                ft.Container(
                    content=ft.ResponsiveRow(
                        controls=[
                            # Titulo
                            ft.Text(
                                "Estadísticas: ",
                                size=20,
                                weight="bold",
                                col=1,
                            ),
                            # Menu de graficos
                            ft.Container(
                                content=menu_graficos,
                                adaptive=True,
                                col=1,
                            ),
                        ],
                        columns=2,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        height=55,
                    )
                ),
                # 2da fila con el grafico
                ft.Container(
                    content=chart,
                    adaptive=True,
                    height=300,
                    padding=10,
                ),
            ],
        )
        self.bgcolor = ft.colors.LIGHT_GREEN_600


class cnts_stats_page(ft.Container):
    """Contenedor que se encarga de mostrar la información correspondiente a la
    sección seleccionada en la página de Estadísticas.

    Attributes:
        parametro (str): Parámetro que se va a mostrar en la sección correspondiente.
            Los posibles valores son:
                - "cultivo": Información del cultivo.
                - "sistema": Información del sistema.
                - "parámetros": Información de los parámetros.
                - "estadísticas": Información de las estadísticas.
        ctn_contenido (ft.Container): Contenedor que se encarga de mostrar la
            información correspondiente a la sección seleccionada.
    """

    def __init__(
        self,
        parametro: t.Literal["cultivo", "sistema", "parámetros", "estadísticas"],
        ctn_contenido=None,
    ):
        # Definimos el título, el icono y el contenido correspondiente
        if parametro == "estadísticas":
            titulo = "Información de las Estadísticas"
            icono = ft.icons.SATELLITE_SHARP
            ctn_contenido = cnt_stats()

        # Establecemos el color de fondo del contenedor del contenido
        if ctn_contenido is not None:
            ctn_contenido.padding = 10
            ctn_contenido.border_radius = 10
            ctn_contenido.alignment = ft.alignment.center
            ctn_contenido.bgcolor = ft.colors.GREEN_600

        # Inicializamos el contenedor
        super().__init__()
        self.content = ft.Column(
            controls=[
                # 1ra fila con el icono y el titulo
                ft.Container(
                    content=rw1_cnt_gral_stats(titulo, icono),
                    bgcolor=ft.colors.GREEN_600,
                    border_radius=10,
                ),
                # 2da fila con el contenido correspondiente
                ctn_contenido,
            ],
            adaptive=True,
        )

        # Establecemos las propiedades del contenedor
        self.height = 650
        self.alignment = ft.alignment.center
        self.padding = 15
        self.border_radius = 10
        self.bgcolor = ft.colors.BLUE
        self.adaptive = True
        self.margin = 10


""" Fin Contenedor de Estadísticas """
###############################################################################
""" Variables globales """
menu_graficos = dpbx_graficos()
