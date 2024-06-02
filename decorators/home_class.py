import flet as ft

class elements(ft.Container):
    def __init__(self, color, content):
        super().__init__()  
        self.bgcolor = color
        self.content = content
        self.padding = 10
        self.alignment = ft.alignment.center