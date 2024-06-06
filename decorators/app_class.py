import flet as ft

class txf_sensor(ft.TextField):
    def __init__(self, value: str, label: str):
        super().__init__()
        self.text_size=13
        self.read_only=True
        self.multiline=True
        self.col=3
        self.text_align=ft.TextAlign.CENTER
        self.value=value
        self.label=label

class txf_rele(ft.TextField):
    def __init__(self, value: str, label: str):
        super().__init__()
        self.read_only=True
        self.col=7
        self.text_align=ft.TextAlign.CENTER
        self.label=label
        self.value=value

class containers_app_page(ft.Container):
    def __init__(self, content: ft.Control):
        super().__init__()
        self.bgcolor = ft.colors.BLUE_GREY_600
        self.padding = 10
        self.margin = 10
        self.border_radius = 10
        self.alignment = ft.alignment.center
        self.content = content

class dpbx_graficos(ft.Dropdown):
    def __init__(self, on_change):
        super().__init__()
        self.on_change = on_change
        self.options = [
            ft.dropdown.Option("Temperatura"),
            ft.dropdown.Option("Humedad"),
            ft.dropdown.Option("Tierra"),
            ft.dropdown.Option("Luz"),
            ft.dropdown.Option("Agua"),
        ]
        self.text_size = 14
        self.content_padding = 10

class cnt_stats(ft.Container):
    def __init__(self, on_change):
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
                                    content=dpbx_graficos(on_change),
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
                    ft.Container(content=chart, adaptive=True, padding=10),
                ],
            ),
            padding=10,
        )
        self.bgcolor = ft.colors.BLUE_GREY_600
        self.border_radius = 10