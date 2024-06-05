import flet as ft, typing as t
from database.data.data import *
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
            ft.Icon(name=icono, size=25),
            ft.Text(
                value=titulo,
                width=210,
                size=15,
                text_align=ft.TextAlign.CENTER,
                no_wrap=True,
            ),
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.width = 350
        self.height = 40
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER


class rrw_cnt_params(ft.ResponsiveRow):
    def __init__(
        self,
        param: t.Literal["temp", "humd", "tier", "lgt_qlty"],
        txf_value: ft.TextField,
    ):
        if param == "temp":
            parametro = "Temperatura: "
            tipo_dato = "°C"

        elif param == "humd":
            parametro = "Humedad: "
            tipo_dato = "%"

        elif param == "tier":
            parametro = "Humedad de la tierra: "
            tipo_dato = "%"

        # Inicializamos la fila responsiva
        super().__init__()
        self.controls = [
            ft.TextField(
                value=parametro,
                text_align=ft.TextAlign.CENTER,
                text_size=16,
                multiline=True,
                read_only=True,
                disabled=True,
                col=6,
                border_width=0,
                color=ft.colors.WHITE,
            ),  # Parametro
            txf_value,  # Valor REAL del parametro
            ft.TextField(
                value=f"20 {tipo_dato}",
                label="Ideal",
                text_size=13,
                multiline=True,
                read_only=True,
                col=3,
                text_align=ft.TextAlign.CENTER,
            ),  # Valor IDEAL del parametro
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.col = 4
        self.width = 380
        self.columns = 12


class rrw_cnt_system(ft.ResponsiveRow):
    def __init__(
        self,
        rele,
        button: ft.ElevatedButton,
    ):
        # Inicializamos la fila responsiva
        super().__init__()
        self.controls = [
            # Actuador
            rele,
            # Estado del actuador e icono animado
            button,
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.width = 380
        self.height = 60
        self.columns = 12


""" Fin Filas de Contenedores de Sistema """
##################################################################################
""" Contenedor de Estadísticas """


class cnt_crop(ft.Container):
    """Contenedor con información del cultivo seleccionado.

    Este contenedor se encarga de mostrar la información correspondiente al
    cultivo seleccionado por el usuario en la sección de estadísticas.

    Attributes:
        crop_name (str): Nombre del cultivo seleccionado.
        week (int): Número de la semana del cultivo.
        phase (str): Fase del cultivo [vegetativa, florecimiento, maduración,
            recolección].
    """

    """FALTA POR AGREGAR LAS DEPENDENCIAS CORRECTAS PARA EL NOMBRE DEL CULTIVO,
    LA FASE, EL NÚMERO DE LA SEMANA, EL TIEMPO RESTANTE, LA FRECUENCIA DE RIEGO,
    ENTRE OTRAS COSAS SEGÚN LA BASE DE DATOS DE CADA CULTIVO."""

    def __init__(self, crop_name: str, week: int, phase: str):
        super().__init__()
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    # Nombre del cultivo
                    ft.TextField(
                        crop_name,
                        label="Crop Name:",
                        read_only=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    # Semana del cultivo
                    ft.TextField(
                        f"{week} week",
                        label="Crop Week:",
                        read_only=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    # Fase del cultivo
                    ft.TextField(
                        phase.capitalize(),
                        label="Crop Phase:",
                        read_only=True,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    # POR AGREGAR :
                    # - tiempo restante
                    # - frecuencia de riego
                    # - tiempo de recolección
                    # - timelines tipo "pop-up"
                    # - gasto energético
                    # - calcular huella de carbono por cultivo
                ],
            ),
            padding=10,
        )


class cnt_params(ft.Container):
    def __init__(self, temp_value, humd_value, tier_value):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=rw1_cnt_gral_stats(
                        titulo="Información de los parámetros",
                        icono=ft.icons.SATELLITE_SHARP,
                    ),
                    padding=10,
                    bgcolor=ft.colors.BLUE_GREY_800,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ResponsiveRow(
                                controls=[
                                    rrw_cnt_params(param="temp", txf_value=temp_value),
                                    rrw_cnt_params(param="humd", txf_value=humd_value),
                                    rrw_cnt_params(param="tier", txf_value=tier_value),
                                ],
                                columns=4,
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ],
                        width=350,
                    ),
                    padding=10,
                    bgcolor=ft.colors.BLUE_GREY_800,
                    border_radius=10,
                ),
            ]
        )
        self.bgcolor = ft.colors.GREEN_600
        self.padding = 20
        self.border_radius = 10


class cnt_system(ft.Container):
    def __init__(self, buttons: dict, values: dict, botones):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=rw1_cnt_gral_stats(
                        titulo="Información del sistema",
                        icono=ft.icons.BUILD,
                    ),
                    padding=10,
                    bgcolor=ft.colors.BLUE_GREY_800,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Column(
                        # Contenedor responsivo de los parámetros
                        controls=[
                            rrw_cnt_system(values["fan"], buttons["btn_fan"]),
                            rrw_cnt_system(values["extrc"], buttons["btn_extrc"]),
                            botones,
                        ],
                        width=350,
                    ),
                    padding=10,
                    bgcolor=ft.colors.BLUE_GREY_800,
                    border_radius=10,
                ),
            ]
        )
        self.bgcolor = ft.colors.GREEN_600
        self.padding = 20
        self.border_radius = 10


class cnt_stats(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    # 1ra fila con titulo y menu de gráficos
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
                                # Menu de gráficos
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
                    # 2da fila con el gráfico
                    ft.Container(content=chart, adaptive=True, height=270, padding=10),
                ],
            ),
            padding=10,
        )
        self.bgcolor = ft.colors.BLUE_GREY_600
        self.border_radius = 10


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
        current=None,
    ):
        # Definimos el título, el icono y el contenido correspondiente
        if parametro == "cultivo":
            titulo = "Información del cultivo"
            icono = ft.icons.CROP
            ctn_contenido = cnt_crop("Tomates", 1, "Vegetativa")

        elif parametro == "sistema":
            titulo = "Información del sistema"
            icono = ft.icons.BUILD
            ctn_contenido = cnt_system()

        elif parametro == "estadísticas":
            titulo = "Información de las Estadísticas"
            icono = ft.icons.SATELLITE_SHARP
            ctn_contenido = cnt_stats()

        # Establecemos el color de fondo del contenedor del contenido
        if ctn_contenido is not None:
            ctn_contenido.width = 380
            ctn_contenido.padding = 10
            ctn_contenido.border_radius = 10
            ctn_contenido.alignment = ft.alignment.center
            ctn_contenido.bgcolor = ft.colors.BLUE_GREY_800
            ctn_contenido.adaptive = True

        # Inicializamos el contenedor
        super().__init__()
        self.content = ft.Column(
            controls=[
                # Fila con el icono y el titulo
                ft.Container(
                    content=rw1_cnt_gral_stats(titulo, icono),
                    bgcolor=ft.colors.BLUE_GREY_800,
                    border_radius=10,
                ),
                # Contenido correspondiente
                ctn_contenido,
            ],
            adaptive=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Establecemos las propiedades del contenedor
        self.width = 400
        self.height = 470
        self.alignment = ft.alignment.center
        self.padding = 20
        self.border_radius = 10
        self.bgcolor = ft.colors.GREEN_600
        self.adaptive = True
        self.margin = 10
        self.col = 1


""" Fin Contenedor de Estadísticas """
###############################################################################
""" Variables globales """
menu_graficos = dpbx_graficos()
