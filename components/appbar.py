import flet as ft

appbar = ft.AppBar(
    title=ft.Text("EcoSense"),
    bgcolor="green",
    leading=ft.IconButton(
        icon =ft.icons.ENERGY_SAVINGS_LEAF,
        tooltip="Inicio",
        on_click=lambda _: print("Leading"),
    ),
    center_title=True,
    actions=[
        ft.IconButton(
            icon=ft.icons.EDIT,
            tooltip="Edit",
            on_click=lambda _: print("Edit"),
        ),
        ft.IconButton(
            icon=ft.icons.MORE_VERT,
            tooltip="More",
            on_click=lambda _: print("More"),
        ),
    ],
)
