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
        