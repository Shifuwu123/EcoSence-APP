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
                width=200,
                size=15,
                text_align=ft.TextAlign.CENTER,
            ),
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.width = 380
        self.height = 55
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER


class rrw_cnt_system(ft.ResponsiveRow):
    def __init__(
        self,
        # Parámetros
        actuador: t.Literal[
            "luces",
            "ventilador",
            "extractor",
            "bomba",
        ],
        estado: bool,
        icono: type = ft.icons.CHECK,
    ):
        # Inicializamos la fila responsiva
        super().__init__()
        self.controls = [
            # Actuador
            ft.TextField(
                label=actuador,
                value="Activado" if estado else "Desactivado",
                read_only=True,
                col=9,
                text_align=ft.TextAlign.CENTER,
            ),
            # Estado del actuador e icono animado
            ft.Container(
                content=ft.Icon(
                    name=icono,
                ),
                col=3,
                height=60,
            ),
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_EVENLY
        self.width = 380
        self.columns = 12


class rrw_cnt_params(ft.ResponsiveRow):
    """Contenedor con un parámetro y su valor.

    Este contenedor se encarga de mostrar un parámetro y su valor correspondiente.
    Los parámetros aceptados son:
        - luz: se muestra como un porcentaje
        - humedad: se muestra como un porcentaje
        - tierra: se muestra como un porcentaje
        - temperatura: se muestra en grados Celsius
    """

    def __init__(
        self,
        # Parámetros
        parametro: t.Literal["luz", "humedad", "tierra", "temperatura"],
        dato: float,
    ):
        # Definimos el título, el icono y el contenido correspondiente
        if parametro == "luz":
            parametro = "Calidad de luz: "
            tipo_dato = "%"

        elif parametro == "humedad":
            parametro = "Humedad: "
            tipo_dato = "%"

        elif parametro == "tierra":
            parametro = "Humedad de la tierra: "
            tipo_dato = "%"

        elif parametro == "temperatura":
            parametro = "Temperatura: "
            tipo_dato = "°C"

        # Inicializamos la fila responsiva
        super().__init__()
        self.controls = [
            # Parametro
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
            ),
            # Valor REAL del parametro
            ft.TextField(
                value=f"{dato} {tipo_dato}",
                label="Real",
                text_size=13,
                multiline=True,
                read_only=True,
                col=3,
                text_align=ft.TextAlign.CENTER,
            ),
            # Valor IDEAL del parametro
            ft.TextField(
                value=f"{dato} {tipo_dato}",
                label="Ideal",
                text_size=13,
                multiline=True,
                read_only=True,
                col=3,
                text_align=ft.TextAlign.CENTER,
            ),
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.col = 4
        self.width = 380
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


class cnt_system(ft.Container):
    """Contenedor con información de los dispositivos de control asociados al
    cultivo.

    Este contenedor se encarga de mostrar la información correspondiente al
    estado de los dispositivos de control asociados al cultivo seleccionado por
    el usuario en la sección de estadísticas.

    Attributes:
        None.
    """

    def __init__(self):
        super().__init__()
        self.content = ft.Container(
            content=ft.Column(
                # Contenedor responsivo de los parámetros
                controls=[
                    rrw_cnt_system("Luces:", True, ft.icons.LIGHT_MODE),
                    rrw_cnt_system("Ventilador:", False, ft.icons.MODE_FAN_OFF_ROUNDED),
                    rrw_cnt_system("Extractor:", True, ft.icons.AIR),
                    rrw_cnt_system("Bomba:", False, ft.icons.WATER_DROP),
                ],
                width=350,
            ),
            padding=10,
        )


class cnt_params(ft.Container):
    """Contenedor con información de los parámetros del cultivo.

    Este contenedor se encarga de mostrar información sobre los parámetros
    del cultivo:
        - Temperatura
        - Humedad del aire
        - Humedad del suelo
        - Nivel de tierra

    Attributes:
        None.
    """

    def __init__(self):
        super().__init__()
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    # Contenedor responsivo de los parámetros
                    ft.ResponsiveRow(
                        controls=[
                            rrw_cnt_params("temperatura", 25),
                            rrw_cnt_params("humedad", 50),
                            rrw_cnt_params("tierra", 50),
                            rrw_cnt_params("luz", 50),
                        ],
                        columns=4,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                width=350,
            ),
            padding=10,
        )


class cnt_stats(ft.Container):
    def __init__(self, fg_grafico):
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
                    ft.Container(
                        content=fg_grafico,
                        adaptive=True,
                        height=270,
                    ),
                ],
                width=350,
            ),
            padding=10,
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
        chart: ft.LineChart = None,
        ctn_contenido=None,
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

        elif parametro == "parámetros":
            titulo = "Información de los Parámetros"
            icono = ft.icons.LIST_ALT
            ctn_contenido = cnt_params()

        elif parametro == "estadísticas":
            titulo = "Información de las Estadísticas"
            icono = ft.icons.SATELLITE_SHARP
            ctn_contenido = cnt_stats(chart)

        # Establecemos el color de fondo del contenedor del contenido
        if ctn_contenido is not None:
            ctn_contenido.width = 380
            ctn_contenido.padding = 10
            ctn_contenido.border_radius = 10
            ctn_contenido.alignment = ft.alignment.center
            ctn_contenido.bgcolor = ft.colors.GREEN_600

        # Inicializamos el contenedor
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=rw1_cnt_gral_stats(titulo, icono),
                    bgcolor=ft.colors.GREEN_600,
                    border_radius=10,
                ),
                # Fila con el icono y el titulo
                # Contenido correspondiente
                ctn_contenido,
            ],
            adaptive=True,
        )

        # Establecemos las propiedades del contenedor
        self.width = 400
        self.alignment = ft.alignment.center
        self.padding = 15
        self.border_radius = 10
        self.bgcolor = ft.colors.BLUE
        self.adaptive = True
        self.margin = 10


""" Fin Contenedor de Estadísticas """
###############################################################################
""" Variables globales """

chart = graph_major(data_series=data_temperatura)
menu_graficos = dpbx_graficos()
