import flet as ft
from components.appbar import appbar as appbar
from components.login import login as login

def main(page: ft.Page):
    page.title = "EcoSense"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_min_width = 720
    page.window_width = 720
    page.window_always_on_top = True
    page.theme = ft.Theme(color_scheme_seed="green")
    page.update()

    page.add(login)

ft.app(target=main, assets_dir="assets")